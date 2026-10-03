// Module 2 acceptance tests: estimation/eskf.hpp on a synthetic circular trajectory.
#include <gtest/gtest.h>

#include <cmath>
#include <random>

#include "slam/estimation/eskf.hpp"

using namespace slam;
using namespace slam::estimation;

namespace {
constexpr double kRadius = 50.0, kSpeed = 10.0, kRate = 100.0, kGravity = 9.81;
const ImuNoise kNoise{0.02, 0.002, 0.0005, 0.00005};

struct Truth {
  Vec3 p, v;
  Quat q;
};

Truth truthAt(double t) {
  const double w = kSpeed / kRadius;
  Truth s;
  s.p = Vec3(kRadius * std::sin(w * t), kRadius * (1.0 - std::cos(w * t)), 0.0);
  s.v = Vec3(kSpeed * std::cos(w * t), kSpeed * std::sin(w * t), 0.0);
  s.q = Quat(Eigen::AngleAxisd(w * t, Vec3::UnitZ()));
  return s;
}

// Body-frame specific force and angular rate are constant on the circle.
ImuSample imuAt(double t, std::mt19937& rng, bool noisy) {
  const double w = kSpeed / kRadius;
  std::normal_distribution<double> n(0.0, 1.0);
  ImuSample s{t, Vec3(0.0, kSpeed * w, kGravity), Vec3(0.0, 0.0, w)};
  if (noisy) {
    const double sa = kNoise.acc_noise * std::sqrt(kRate),
                 sg = kNoise.gyro_noise * std::sqrt(kRate);
    s.acc += Vec3(n(rng), n(rng), n(rng)) * sa;
    s.gyro += Vec3(n(rng), n(rng), n(rng)) * sg;
  }
  return s;
}

struct RunResult {
  double rmse = 0.0;
  double gnss_rmse = 0.0;  // of the raw GNSS fixes, for comparison
  double mean_nees = 0.0;
  Vec3 final_error = Vec3::Zero();
  Mat3 final_cov = Mat3::Identity();
  std::vector<double> trace_during_outage;
};

// Runs the filter for `duration` s with GNSS at 1 Hz (sigma 1 m) except inside [outage0, outage1).
RunResult run(unsigned seed, double duration, double outage0 = -1.0, double outage1 = -1.0) {
  std::mt19937 rng(seed);
  std::normal_distribution<double> n(0.0, 1.0);
  const Truth t0 = truthAt(0.0);
  NominalState x0;
  x0.p = t0.p + Vec3(n(rng), n(rng), n(rng)) * 0.5;
  x0.v = t0.v + Vec3(n(rng), n(rng), n(rng)) * 0.1;
  x0.q = t0.q * Quat(Eigen::AngleAxisd(0.01 * n(rng), Vec3::UnitZ()));
  Eskf::Cov P0 = Eskf::Cov::Zero();
  P0.block<3, 3>(0, 0) = Mat3::Identity() * 0.25;
  P0.block<3, 3>(3, 3) = Mat3::Identity() * 0.01;
  P0.block<3, 3>(6, 6) = Mat3::Identity() * 1e-4;
  P0.block<3, 3>(9, 9) = Mat3::Identity() * 1e-4;
  P0.block<3, 3>(12, 12) = Mat3::Identity() * 1e-6;
  Eskf filter(x0, P0, kNoise, Vec3(0.0, 0.0, -kGravity));

  RunResult r;
  const double dt = 1.0 / kRate;
  const int steps = static_cast<int>(duration * kRate);
  double sq = 0.0, nees = 0.0, sq_gnss = 0.0;
  int n_gnss = 0, n_fix = 0;
  for (int k = 0; k < steps; ++k) {
    const double t = k * dt;
    filter.predict(imuAt(t, rng, true), dt);
    const double t1 = t + dt;
    const bool gnss_epoch = (k + 1) % static_cast<int>(kRate) == 0;
    const bool in_outage = t1 >= outage0 && t1 < outage1;
    if (gnss_epoch && !in_outage) {
      const Vec3 z = truthAt(t1).p + Vec3(n(rng), n(rng), n(rng)) * 1.0;
      filter.updatePosition(z, Mat3::Identity());
      sq_gnss += (z - truthAt(t1).p).squaredNorm();
      ++n_fix;
    }
    if (in_outage) r.trace_during_outage.push_back(filter.covariance().block<3, 3>(0, 0).trace());
    if (gnss_epoch) {
      const Vec3 e = filter.state().p - truthAt(t1).p;
      const Mat3 P = filter.covariance().block<3, 3>(0, 0);
      sq += e.squaredNorm();
      nees += e.dot(P.ldlt().solve(e));
      ++n_gnss;
      r.final_error = e;
      r.final_cov = P;
    }
  }
  r.rmse = std::sqrt(sq / n_gnss);
  r.gnss_rmse = n_fix > 0 ? std::sqrt(sq_gnss / n_fix) : 0.0;
  r.mean_nees = nees / n_gnss;
  return r;
}
}  // namespace

TEST(M2Eskf, StationaryLevelStaysPut) {
  NominalState x0;
  Eskf filter(x0, Eskf::Cov::Identity() * 1e-6, kNoise, Vec3(0.0, 0.0, -kGravity));
  for (int k = 0; k < 1000; ++k)
    filter.predict({k * 0.01, Vec3(0, 0, kGravity), Vec3::Zero()}, 0.01);
  EXPECT_LT(filter.state().p.norm(), 1e-9);
  EXPECT_LT(filter.state().v.norm(), 1e-9);
}

TEST(M2Eskf, NoiselessPredictionFollowsTheCircle) {
  const Truth t0 = truthAt(0.0);
  NominalState x0;
  x0.p = t0.p;
  x0.v = t0.v;
  x0.q = t0.q;
  Eskf filter(x0, Eskf::Cov::Identity() * 1e-6, kNoise, Vec3(0.0, 0.0, -kGravity));
  std::mt19937 rng(0);
  for (int k = 0; k < 500; ++k) filter.predict(imuAt(k / kRate, rng, false), 1.0 / kRate);
  EXPECT_LT((filter.state().p - truthAt(5.0).p).norm(), 0.1);
}

TEST(M2Eskf, PredictionGrowsCovariance) {
  NominalState x0;
  Eskf filter(x0, Eskf::Cov::Identity() * 1e-4, kNoise, Vec3(0.0, 0.0, -kGravity));
  const double before = filter.covariance().block<3, 3>(0, 0).trace();
  for (int k = 0; k < 100; ++k)
    filter.predict({k * 0.01, Vec3(0, 0, kGravity), Vec3::Zero()}, 0.01);
  EXPECT_GT((filter.covariance().block<3, 3>(0, 0).trace()), before);
  EXPECT_TRUE(filter.covariance().isApprox(filter.covariance().transpose(), 1e-9));
}

TEST(M2Eskf, UpdatePullsTowardsMeasurementAndShrinksCovariance) {
  NominalState x0;
  Eskf filter(x0, Eskf::Cov::Identity(), kNoise, Vec3(0.0, 0.0, -kGravity));
  const double before = filter.covariance().block<3, 3>(0, 0).trace();
  filter.updatePosition(Vec3(2.0, 0.0, 0.0), Mat3::Identity());
  EXPECT_NEAR(filter.state().p.x(), 1.0, 1e-6);  // equal prior and measurement variance
  EXPECT_LT((filter.covariance().block<3, 3>(0, 0).trace()), before);
  EXPECT_NEAR(filter.state().q.norm(), 1.0, 1e-12);
}

TEST(M2Eskf, TracksTheCircleWithinErrorBound) {
  const RunResult r = run(1, 120.0);
  EXPECT_LT(r.rmse, 0.85 * r.gnss_rmse) << "the filter must clearly beat raw GNSS";
  EXPECT_LT(r.rmse, 1.5) << "position RMSE at GNSS epochs";
}

TEST(M2Eskf, ConsistentNees) {
  // Average position NEES over Monte Carlo runs should be close to 3 (the state dimension).
  double sum = 0.0;
  const int runs = 10;
  for (int s = 0; s < runs; ++s) sum += run(100 + s, 60.0).mean_nees;
  const double anees = sum / runs;
  EXPECT_GT(anees, 1.5) << "filter is too pessimistic";
  EXPECT_LT(anees, 6.0) << "filter is overconfident";
}

TEST(M2Eskf, OutageGrowsCovarianceAndStaysConsistent) {
  const RunResult r = run(7, 90.0, 40.0, 80.0);  // 40 s without GNSS
  ASSERT_GT(r.trace_during_outage.size(), 100u);
  for (size_t i = 1; i < r.trace_during_outage.size(); ++i)
    ASSERT_GE(r.trace_during_outage[i], r.trace_during_outage[i - 1] - 1e-12) << "sample " << i;
  EXPECT_GT(r.trace_during_outage.back(), 10.0 * r.trace_during_outage.front());
}
