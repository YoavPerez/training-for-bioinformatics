#pragma once

#include <Eigen/Core>
#include <Eigen/Geometry>
#include <stdexcept>
#include <string>
#include <vector>

namespace slam {

using Vec3 = Eigen::Vector3d;
using Mat3 = Eigen::Matrix3d;
using Quat = Eigen::Quaterniond;
// Rigid transform. Name variables T_<to>_<from>, as defined in CONVENTIONS.md.
using Pose = Eigen::Isometry3d;

using PointCloud = std::vector<Vec3>;

// Thrown by starter code that the trainee has not implemented yet.
struct NotImplemented : std::logic_error {
  explicit NotImplemented(const std::string& what) : std::logic_error("TODO: " + what) {}
};

}  // namespace slam
