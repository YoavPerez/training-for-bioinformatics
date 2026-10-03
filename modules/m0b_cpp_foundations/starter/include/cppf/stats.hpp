#pragma once
// Exercise 4: functions on point sets stored as columns of a 3xN matrix.
// They must accept any 3xN expression (whole matrices, blocks, Maps over raw buffers) without
// copying.

#include <Eigen/Core>
#include <Eigen/Geometry>

namespace cppf {

Eigen::Vector3d centroid(const Eigen::Ref<const Eigen::Matrix3Xd>& points);

// Sample covariance (normalized by N - 1). Throws std::invalid_argument for fewer than 2 points.
Eigen::Matrix3d covariance(const Eigen::Ref<const Eigen::Matrix3Xd>& points);

// Applies T to every column, in place.
void transformInPlace(const Eigen::Isometry3d& T, Eigen::Ref<Eigen::Matrix3Xd> points);

}  // namespace cppf
