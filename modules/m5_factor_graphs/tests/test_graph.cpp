// Module 5 acceptance tests: backend/graph_builder.hpp (GTSAM)
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

Pose pose2d(double x, double y, double yaw) {
  Pose T = Pose::Identity();
  T.linear() = Eigen::AngleAxisd(yaw, Vec3::UnitZ()).toRotationMatrix();
  T.translation() = Vec3(x, y, 0.0);
  return T;
}

// Ground truth: drive 1 m/step along a slowly curving path.
std::vector<Pose> truthPath(int n) {
  std::vector<Pose> out;
  double x = 0, y = 0, yaw = 0;
  for (int k = 0; k < n; ++k) {
    out.push_back(pose2d(x, y, yaw));
    x += std::cos(yaw);
    y += std::sin(yaw);
    yaw += 0.02;
  }
  return out;
}
}  // namespace

TEST(M5Graph, NoiselessOdometryIsReproduced) {
  const auto truth = truthPath(20);
  GraphBuilder g;
  for (int k = 0; k < 20; ++k) g.setInitial(k, k == 0 ? truth[0] : pose2d(0, 0, 0));
  g.addPrior(0, truth[0], sig(1e-3, 1e-3));
  for (int k = 1; k < 20; ++k)
    g.addOdometry(k - 1, k, geometry::compose(geometry::inverse(truth[k - 1]), truth[k]),
                  sig(0.01, 0.05));
  EXPECT_EQ(g.numFactors(), 20u);
  const auto result = g.optimize();
  ASSERT_EQ(result.size(), 20u);
  for (int k = 0; k < 20; ++k)
    EXPECT_LT((result.at(k).translation() - truth[k].translation()).norm(), 1e-6) << "k=" << k;
}

TEST(M5Graph, GnssBoundsOdometryDrift) {
  const int n = 61;  // GNSS every 5th pose, including the last one
  const auto truth = truthPath(n);
  std::mt19937 rng(3);
  std::normal_distribution<double> noise(0.0, 1.0);
  GraphBuilder g;
  std::vector<Pose> dead_reckoning{truth[0]};
  g.addPrior(0, truth[0], sig(1e-3, 1e-3));
  for (int k = 1; k < n; ++k) {
    Pose rel = geometry::compose(geometry::inverse(truth[k - 1]), truth[k]);
    rel = rel * pose2d(0.0, 0.0, 0.004);  // systematic heading drift
    dead_reckoning.push_back(dead_reckoning.back() * rel);
    g.addOdometry(k - 1, k, rel, sig(0.005, 0.05));  // sigma consistent with the drift
  }
  for (int k = 0; k < n; ++k) {
    g.setInitial(k, dead_reckoning[k]);
    if (k % 5 == 0)
      g.addGnss(k, truth[k].translation() + Vec3(noise(rng), noise(rng), noise(rng)) * 0.5,
                Vec3::Constant(0.5));
  }
  const auto result = g.optimize();
  double dr_sq = 0.0, opt_sq = 0.0;
  for (int k = 0; k < n; ++k) {
    dr_sq += (dead_reckoning[k].translation() - truth[k].translation()).squaredNorm();
    opt_sq += (result.at(k).translation() - truth[k].translation()).squaredNorm();
  }
  const double dr_rmse = std::sqrt(dr_sq / n), opt_rmse = std::sqrt(opt_sq / n);
  const double gnss_sigma_3d = 0.5 * std::sqrt(3.0);
  EXPECT_GT(dr_rmse, 2.0) << "the test scenario should drift without GNSS";
  EXPECT_LT(opt_rmse, gnss_sigma_3d) << "fused RMSE should not exceed the GNSS noise level";
  EXPECT_LT(opt_rmse, 0.2 * dr_rmse);
}

TEST(M5Graph, ImuPreintegrationPredictsConstantAcceleration) {
  // Level vehicle, v0 = 5 m/s along x, a = 1 m/s^2 for 1 s: x(1) = 5.5 m, v(1) = 6 m/s.
  std::vector<estimation::ImuSample> samples;
  for (int k = 0; k <= 100; ++k) samples.push_back({k * 0.01, Vec3(1.0, 0.0, 9.81), Vec3::Zero()});
  const estimation::ImuNoise noise{0.01, 0.001, 1e-4, 1e-5};
  GraphBuilder g;
  g.setInitial(0, Pose::Identity(), Vec3(5.0, 0.0, 0.0));
  g.setInitial(1, pose2d(4.0, 0.3, 0.05), Vec3(5.0, 0.0, 0.0));  // deliberately wrong guess
  g.addPrior(0, Pose::Identity(), sig(1e-4, 1e-4));
  g.addImu(0, 1, samples, noise);
  const auto result = g.optimize();
  EXPECT_NEAR(result.at(1).translation().x(), 5.5, 0.02);
  EXPECT_NEAR(result.at(1).translation().y(), 0.0, 0.02);
  EXPECT_LT(Eigen::AngleAxisd(result.at(1).linear()).angle(), 1e-3);
}

TEST(M5Graph, NumFactorsCountsEveryAddition) {
  GraphBuilder g;
  g.setInitial(0, Pose::Identity());
  g.setInitial(1, Pose::Identity());
  g.addPrior(0, Pose::Identity(), sig(0.1, 0.1));
  g.addOdometry(0, 1, Pose::Identity(), sig(0.1, 0.1));
  g.addGnss(1, Vec3::Zero(), Vec3::Ones());
  EXPECT_EQ(g.numFactors(), 3u);
}
