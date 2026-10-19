#pragma once
// Module 5 (and 6): factor-graph back-end on GTSAM.
// Variables are body (IMU) poses T_world_body indexed by keyframe id, plus velocity and
// IMU bias per keyframe when IMU factors are used.

#include <map>
#include <memory>

#include "slam/estimation/eskf.hpp"
#include "slam/types.hpp"

namespace slam::backend {

// Tangent-space sigmas in GTSAM Pose3 order: rotation [rad] (3), then translation [m] (3).
using Sigmas6 = Eigen::Matrix<double, 6, 1>;

// Width of the robust kernel on loop factors, in whitened units (multiples of sigma). run_pipeline
// uses it unless --loop-kernel-width is given, and the module 6 tests use it. Module 6: choose the
// kernel and this width together, by experiment.
inline constexpr double kLoopKernelWidth = 5.0;

class GraphBuilder {
 public:
  GraphBuilder();
  ~GraphBuilder();

  // Initial guess for keyframe i (required for every keyframe that appears in a factor).
  void setInitial(int i, const Pose& T_world_i, const Vec3& v_world = Vec3::Zero());

  void addPrior(int i, const Pose& T_world_i, const Sigmas6& sigmas);
  void addOdometry(int i, int j, const Pose& T_i_j, const Sigmas6& sigmas);
  // Like addOdometry, but wrapped in a robust kernel (your choice) of the given width, so that a
  // wrong loop closure cannot corrupt the trajectory. kernel_width is in whitened units (sigma):
  // GTSAM applies the m-estimator to the residual divided by its sigmas.
  void addLoop(int i, int j, const Pose& T_i_j, const Sigmas6& sigmas, double kernel_width);
  // Position of body i in the world frame (e.g. GNSS in local ENU).
  void addGnss(int i, const Vec3& p_world, const Vec3& sigmas);
  // Preintegrates the IMU samples between keyframes i and j (gravity along -z, 9.81 m/s^2).
  void addImu(int i, int j, const std::vector<estimation::ImuSample>& samples,
              const estimation::ImuNoise& noise);

  // Optimizes with Levenberg-Marquardt and returns T_world_i for every keyframe.
  std::map<int, Pose> optimize(int max_iterations = 100);

  size_t numFactors() const;

 private:
  struct Impl;  // hides GTSAM types from this header
  std::unique_ptr<Impl> impl_;
};

}  // namespace slam::backend
