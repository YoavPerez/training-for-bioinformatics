#pragma once
// Module 5: scan-to-map LiDAR odometry built on the module 4 ICP.

#include "slam/registration/icp.hpp"
#include "slam/types.hpp"

namespace slam::odometry {

struct LidarOdometryConfig {
  double scan_voxel = 0.5;   // [m] downsampling of each incoming scan
  double map_voxel = 1.0;    // [m] downsampling of the local map
  double map_radius = 80.0;  // [m] points farther than this from the current pose are dropped
  double min_range = 3.0;    // [m] points closer than this to the sensor are dropped (ego vehicle)
  registration::IcpConfig icp{30, 1.0, 1e-4, 1e-4, 0.1};
};

class LidarOdometry {
 public:
  explicit LidarOdometry(LidarOdometryConfig config = {}) : config_(config) {}

  // Registers a scan expressed in the LiDAR frame and returns T_world_lidar, where the world
  // frame is the LiDAR frame of the first scan.
  Pose registerScan(const PointCloud& scan);

  const PointCloud& localMap() const { return map_; }
  const std::vector<Pose>& poses() const { return poses_; }

 private:
  LidarOdometryConfig config_;
  PointCloud map_;  // in the world frame
  std::vector<Pose> poses_;
};

}  // namespace slam::odometry
