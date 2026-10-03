#include "slam/registration/icp.hpp"

#include "slam/geometry/transform.hpp"
#include "slam/registration/kdtree.hpp"

namespace slam::registration {

IcpResult icpPointToPlane(const PointCloud& source, const PointCloud& target,
                          const std::vector<Vec3>& target_normals, const Pose& T_init,
                          const IcpConfig& config) {
  // TODO(m4): data association with KdTree, linearize the point-to-plane residual,
  // solve the 6x6 normal equations, update the pose, check convergence.
  (void)source;
  (void)target;
  (void)target_normals;
  (void)T_init;
  (void)config;
  throw NotImplemented("registration::icpPointToPlane");
}

}  // namespace slam::registration
