#include "slam/backend/graph_builder.hpp"

#include <gtsam/geometry/Pose3.h>
#include <gtsam/inference/Symbol.h>
#include <gtsam/navigation/GPSFactor.h>
#include <gtsam/navigation/ImuFactor.h>
#include <gtsam/nonlinear/LevenbergMarquardtOptimizer.h>
#include <gtsam/nonlinear/NonlinearFactorGraph.h>
#include <gtsam/nonlinear/PriorFactor.h>
#include <gtsam/nonlinear/Values.h>
#include <gtsam/slam/BetweenFactor.h>

namespace slam::backend {

using gtsam::symbol_shorthand::B;  // IMU bias
using gtsam::symbol_shorthand::V;  // velocity
using gtsam::symbol_shorthand::X;  // pose

struct GraphBuilder::Impl {
  gtsam::NonlinearFactorGraph graph;
  gtsam::Values initial;
  std::map<int, Vec3> initial_velocity;
};

GraphBuilder::GraphBuilder() : impl_(std::make_unique<Impl>()) {}
GraphBuilder::~GraphBuilder() = default;

void GraphBuilder::setInitial(int i, const Pose& T_world_i, const Vec3& v_world) {
  impl_->initial.insert_or_assign(X(i), gtsam::Pose3(T_world_i.matrix()));
  impl_->initial_velocity[i] = v_world;
}

// Worked example of one factor; the other factors follow the same pattern.
void GraphBuilder::addPrior(int i, const Pose& T_world_i, const Sigmas6& sigmas) {
  const auto noise = gtsam::noiseModel::Diagonal::Sigmas(sigmas);
  impl_->graph.emplace_shared<gtsam::PriorFactor<gtsam::Pose3>>(
      X(i), gtsam::Pose3(T_world_i.matrix()), noise);
}

void GraphBuilder::addOdometry(int i, int j, const Pose& T_i_j, const Sigmas6& sigmas) {
  // TODO(m5)
  (void)i, (void)j, (void)T_i_j, (void)sigmas;
  throw NotImplemented("GraphBuilder::addOdometry");
}

void GraphBuilder::addLoop(int i, int j, const Pose& T_i_j, const Sigmas6& sigmas,
                           double kernel_width) {
  // TODO(m6): look up robust noise models in the GTSAM docs; compare kernels on a false loop.
  (void)i, (void)j, (void)T_i_j, (void)sigmas, (void)kernel_width;
  throw NotImplemented("GraphBuilder::addLoop");
}

void GraphBuilder::addGnss(int i, const Vec3& p_world, const Vec3& sigmas) {
  // TODO(m5)
  (void)i, (void)p_world, (void)sigmas;
  throw NotImplemented("GraphBuilder::addGnss");
}

void GraphBuilder::addImu(int i, int j, const std::vector<estimation::ImuSample>& samples,
                          const estimation::ImuNoise& noise) {
  // TODO(m5): preintegrate, add the IMU factor and a bias random-walk factor.
  // Velocity and bias variables need initial values and must not be left unconstrained.
  (void)i, (void)j, (void)samples, (void)noise;
  throw NotImplemented("GraphBuilder::addImu");
}

std::map<int, Pose> GraphBuilder::optimize(int max_iterations) {
  // TODO(m5)
  (void)max_iterations;
  throw NotImplemented("GraphBuilder::optimize");
}

size_t GraphBuilder::numFactors() const { return impl_->graph.size(); }

}  // namespace slam::backend
