#pragma once
// Provided: readers for KITTI raw files and for the CSV/TUM files written by `slampipe.prepare`.

#include <map>

#include "slam/estimation/eskf.hpp"
#include "slam/sensors/deskew.hpp"
#include "slam/types.hpp"

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

}  // namespace slam::io
