#include "cppf/stats.hpp"

#include "cppf/not_implemented.hpp"

namespace cppf {

Eigen::Vector3d centroid(const Eigen::Ref<const Eigen::Matrix3Xd>& points) {
  // TODO(m0b): implement without copying the input.
  (void)points;
  throw NotImplemented("centroid");
}

Eigen::Matrix3d covariance(const Eigen::Ref<const Eigen::Matrix3Xd>& points) {
  // TODO(m0b): implement.
  (void)points;
  throw NotImplemented("covariance");
}

void transformInPlace(const Eigen::Isometry3d& T, Eigen::Ref<Eigen::Matrix3Xd> points) {
  // TODO(m0b): implement.
  (void)T;
  (void)points;
  throw NotImplemented("transformInPlace");
}

}  // namespace cppf
