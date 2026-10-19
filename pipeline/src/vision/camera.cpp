#include "slam/vision/camera.hpp"

namespace slam::vision {

Mat3 PinholeCamera::K() const {
  Mat3 k;
  k << fx, 0.0, cx, 0.0, fy, cy, 0.0, 0.0, 1.0;
  return k;
}

bool PinholeCamera::inImage(const Vec2& uv) const {
  return uv.x() >= -0.5 && uv.x() < width - 0.5 && uv.y() >= -0.5 && uv.y() < height - 0.5;
}

std::optional<Vec2> project(const PinholeCamera& cam, const Vec3& p_cam, double min_depth) {
  // TODO(m4b): perspective division, then intrinsics. Reject points with z < min_depth and pixels
  // outside the image.
  (void)cam;
  (void)p_cam;
  (void)min_depth;
  throw NotImplemented("vision::project");
}

Vec3 unproject(const PinholeCamera& cam, const Vec2& uv, double depth) {
  // TODO(m4b): the inverse of project for a known depth (z).
  (void)cam;
  (void)uv;
  (void)depth;
  throw NotImplemented("vision::unproject");
}

std::vector<ProjectedPoint> projectCloud(const PinholeCamera& cam, const Pose& T_cam_lidar,
                                         const PointCloud& cloud_lidar, double min_depth) {
  // TODO(m4b): transform each point with T_cam_lidar and keep those that project into the image.
  // C++ focus: no allocation inside the loop (reserve once), and no copy of the input cloud.
  (void)cam;
  (void)T_cam_lidar;
  (void)cloud_lidar;
  (void)min_depth;
  throw NotImplemented("vision::projectCloud");
}

}  // namespace slam::vision
