#pragma once
// Module 4: point-to-plane ICP.

#include "slam/types.hpp"

namespace slam::registration {

struct IcpConfig {
  int max_iterations = 50;
  double max_correspondence_distance = 1.0;  // [m]
  // Stop when the update is smaller than both thresholds.
  double convergence_translation = 1e-5;  // [m]
  double convergence_rotation = 1e-5;     // [rad]
  // Huber threshold on the point-to-plane residual [m]; 0 disables the robust kernel.
  double huber_threshold = 0.0;
};

struct IcpResult {
  Pose T_target_source = Pose::Identity();
  int iterations = 0;
  bool converged = false;
  double rmse = 0.0;  // point-to-plane residual RMS over inliers at the final estimate
  size_t num_correspondences = 0;
};

// Aligns `source` to `target`. target_normals[i] is the unit normal of target[i].
// T_init is the initial guess of T_target_source.
IcpResult icpPointToPlane(const PointCloud& source, const PointCloud& target,
                          const std::vector<Vec3>& target_normals, const Pose& T_init,
                          const IcpConfig& config = {});

}  // namespace slam::registration
