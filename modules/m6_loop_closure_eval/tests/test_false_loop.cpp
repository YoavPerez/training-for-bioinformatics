// Module 6 acceptance tests: a wrong loop closure must not corrupt the trajectory, and a true loop
// must still close when drift has made its initial residual large. All loops use kLoopKernelWidth
// (graph_builder.hpp), the width run_pipeline uses by default.
#include <gtest/gtest.h>

#include <cmath>
#include <random>

#include "slam/backend/graph_builder.hpp"
#include "slam/geometry/transform.hpp"

using namespace slam;
using namespace slam::backend;

namespace {
Sigmas6 sig(double rot, double trans) {
  Sigmas6 s;
  s << rot, rot, rot, trans, trans, trans;
  return s;
}

// A 40 m x 40 m square driven once (1 m steps), returning to the start.
std::vector<Pose> square() {
  std::vector<Pose> out;
  Pose T = Pose::Identity();
  for (int side = 0; side < 4; ++side) {
    for (int s = 0; s < 40; ++s) {
      out.push_back(T);
      Pose step = Pose::Identity();
      step.translation() = Vec3(1, 0, 0);
      if (s == 39) step.linear() = Eigen::AngleAxisd(M_PI / 2, Vec3::UnitZ()).toRotationMatrix();
      T = T * step;
    }
  }
  return out;
}

double rmse(const std::map<int, Pose>& est, const std::vector<Pose>& truth) {
  double sq = 0.0;
  for (size_t k = 0; k < truth.size(); ++k)
    sq += (est.at(static_cast<int>(k)).translation() - truth[k].translation()).squaredNorm();
  return std::sqrt(sq / truth.size());
}

// Noisy odometry around the square plus the true loop (last -> first); optionally a false loop.
// heading_sigma 0.003 rad leaves a loop gap of ~1.3 m before optimization, 0.009 rad ~3.7 m.
std::map<int, Pose> solve(bool add_false_loop, double heading_sigma = 0.003) {
  const auto truth = square();
  const int n = static_cast<int>(truth.size());
  std::mt19937 rng(11);
  std::normal_distribution<double> nz(0.0, 1.0);
  GraphBuilder g;
  Pose dr = truth[0];
  g.setInitial(0, dr);
  g.addPrior(0, truth[0], sig(1e-4, 1e-4));
  for (int k = 1; k < n; ++k) {
    Pose rel = geometry::compose(geometry::inverse(truth[k - 1]), truth[k]);
    Pose noise = Pose::Identity();
    noise.linear() = Eigen::AngleAxisd(heading_sigma * nz(rng), Vec3::UnitZ()).toRotationMatrix();
    noise.translation() = Vec3(nz(rng), nz(rng), 0.0) * 0.02;
    rel = rel * noise;
    dr = dr * rel;
    g.setInitial(k, dr);
    g.addOdometry(k - 1, k, rel, sig(0.003, 0.02));
  }
  g.addLoop(n - 1, 0, geometry::compose(geometry::inverse(truth[n - 1]), truth[0]), sig(0.01, 0.05),
            kLoopKernelWidth);
  if (add_false_loop)  // ~40 m apart in reality
    g.addLoop(20, 100, Pose::Identity(), sig(0.01, 0.05), kLoopKernelWidth);
  return g.optimize();
}
}  // namespace

TEST(M6FalseLoop, TrueLoopReducesDrift) { EXPECT_LT(rmse(solve(false), square()), 0.5); }

TEST(M6FalseLoop, FalseLoopDoesNotCorruptTrajectory) {
  const auto truth = square();
  const double clean = rmse(solve(false), truth);
  const double with_false = rmse(solve(true), truth);
  EXPECT_LT(with_false, clean + 0.1)
      << "clean " << clean << " m, with false loop " << with_false << " m";
}

// Same square with three times the heading noise; a plain Gaussian loop factor gives ~0.6 m.
TEST(M6FalseLoop, TrueLoopClosesUnderLargeDrift) {
  EXPECT_LT(rmse(solve(false, 0.009), square()), 1.0);
}

TEST(M6FalseLoop, FalseLoopRejectedUnderLargeDrift) {
  const auto truth = square();
  const double clean = rmse(solve(false, 0.009), truth);
  const double with_false = rmse(solve(true, 0.009), truth);
  EXPECT_LT(with_false, clean + 0.1)
      << "clean " << clean << " m, with false loop " << with_false << " m";
}
