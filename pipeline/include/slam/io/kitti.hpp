#pragma once
// Provided: readers for KITTI raw files and for the CSV/TUM files written by `slampipe.prepare`.

#include <map>

#include "slam/estimation/eskf.hpp"
#include "slam/sensors/deskew.hpp"
#include "slam/types.hpp"
#include "slam/vision/camera.hpp"

namespace slam::io {

// Reads a KITTI velodyne .bin scan (x, y, z, intensity as float32). Intensity is dropped.
PointCloud readVelodyneBin(const std::string& path);

// One number per line (e.g. lidar_times.csv written by slampipe.prepare).
std::vector<double> readColumn(const std::string& path);

// 4x4 row-major matrix, whitespace separated.
Pose readPoseMatrix(const std::string& path);

// CSV "t,ax,ay,az,wx,wy,wz" with a header line.
std::vector<estimation::ImuSample> readImuCsv(const std::string& path);

struct PositionFix {
  double t = 0.0;
  Vec3 p = Vec3::Zero();
  Vec3 sigma = Vec3::Ones();
};
// CSV "t,x,y,z,sx,sy,sz" with a header line (local ENU, metres).
std::vector<PositionFix> readGnssCsv(const std::string& path);

// TUM trajectory format: "t tx ty tz qx qy qz qw" per line.
sensors::Trajectory readTum(const std::string& path);
void writeTum(const std::string& path, const sensors::Trajectory& traj);

// Reads "key: v1 v2 ..." calibration files (e.g. calib_imu_to_velo.txt).
std::map<std::string, std::vector<double>> readCalib(const std::string& path);

// T_to_from from a calib file containing R (row-major 3x3) and T (3 values).
Pose calibToPose(const std::map<std::string, std::vector<double>>& calib);

struct CameraCalib {
  vision::PinholeCamera cam;
  Pose T_cam_velo;  // velodyne -> rectified camera frame
};
// Rectified camera `index` (0-3) of a KITTI raw date directory (the folder with
// calib_cam_to_cam.txt and calib_velo_to_cam.txt): intrinsics from P_rect_0<index>, image size from
// S_rect_0<index>, and T_cam_velo = [K^-1 * P_rect(:, 3)] * R_rect_00 * T_cam0_velo (KITTI IJRR,
// Sections IV-B and IV-C, eq. 3-7).
CameraCalib readKittiCamera(const std::string& date_dir, int index = 0);

}  // namespace slam::io
