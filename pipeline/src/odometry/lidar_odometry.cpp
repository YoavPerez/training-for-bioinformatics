#include "slam/odometry/lidar_odometry.hpp"

#include "slam/geometry/transform.hpp"
#include "slam/registration/normals.hpp"

namespace slam::odometry {

Pose LidarOdometry::registerScan(const PointCloud& scan) {
  // TODO(m5): preprocess the scan, predict the pose, register against the local map,
  // then update the map. Your design doc should say how each step works.
  (void)scan;
  throw NotImplemented("LidarOdometry::registerScan");
}

}  // namespace slam::odometry
