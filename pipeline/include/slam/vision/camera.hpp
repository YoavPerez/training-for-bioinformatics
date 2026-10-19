#pragma once
// Module 4b: pinhole camera model and LiDAR-to-image projection.
// Camera frame: x right, y down, z forward (optical axis), as in the KITTI devkit.

#include <optional>

#include "slam/types.hpp"

namespace slam::vision {

using Vec2 = Eigen::Vector2d;

// Pinhole camera without distortion (KITTI rectified images). Pixel (0, 0) is the centre of the
// top-left pixel.
struct PinholeCamera {
  double fx = 0.0;
  double fy = 0.0;
  double cx = 0.0;
  double cy = 0.0;
  int width = 0;
  int height = 0;

  // Calibration matrix K = [fx 0 cx; 0 fy cy; 0 0 1].
  Mat3 K() const;
  // True if the pixel lies inside [-0.5, width - 0.5) x [-0.5, height - 0.5).
  bool inImage(const Vec2& uv) const;
};

// Projects a point given in the camera frame. Returns nullopt if the point is closer than min_depth
// along z (including behind the camera) or projects outside the image.
std::optional<Vec2> project(const PinholeCamera& cam, const Vec3& p_cam, double min_depth = 0.1);

// The point in the camera frame that projects to `uv` and lies at `depth` along z (not along the
// ray).
Vec3 unproject(const PinholeCamera& cam, const Vec2& uv, double depth);

struct ProjectedPoint {
  Vec2 uv;
  double depth = 0.0;  // z in the camera frame [m]
  int index = 0;       // index of the point in the input cloud
};

// Transforms every point of a LiDAR cloud into the camera frame and keeps those that project into
// the image, in input order.
std::vector<ProjectedPoint> projectCloud(const PinholeCamera& cam, const Pose& T_cam_lidar,
                                         const PointCloud& cloud_lidar, double min_depth = 0.1);

}  // namespace slam::vision
