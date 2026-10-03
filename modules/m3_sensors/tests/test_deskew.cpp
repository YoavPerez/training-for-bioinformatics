// Module 3 acceptance tests: sensors/deskew.hpp
#include <gtest/gtest.h>

#include <cmath>

#include "slam/sensors/deskew.hpp"

using namespace slam;
using namespace slam::sensors;

namespace {
constexpr double kSweep = 0.1;     // [s]
constexpr double kYawRate = 1.57;  // [rad/s], ~90 deg/s
constexpr double kSpeed = 5.0;     // [m/s] along x

Pose truePose(double t) {
  Pose T = Pose::Identity();
  T.linear() = Eigen::AngleAxisd(kYawRate * t, Vec3::UnitZ()).toRotationMatrix();
  T.translation() = Vec3(kSpeed * t, 0.0, 0.0);
  return T;
}

Trajectory trueTrajectory(int samples = 11) {
  Trajectory traj;
  for (int i = 0; i < samples; ++i) {
    const double t = kSweep * i / (samples - 1);
    traj.push_back({t, truePose(t)});
  }
  return traj;
}

// Walls of a 20 m x 20 m room centred on the start position, sampled every ~0.2 m at two heights.
PointCloud roomWorld() {
  PointCloud pts;
  for (double s = -10.0; s <= 10.0; s += 0.2)
    for (double z : {-1.0, 1.0}) {
      pts.emplace_back(s, -10.0, z);
      pts.emplace_back(s, 10.0, z);
      pts.emplace_back(-10.0, s, z);
      pts.emplace_back(10.0, s, z);
    }
  return pts;
}

// Each world point is "measured" at a time given by its index; returns sensor-frame points.
void skew(const PointCloud& world, PointCloud& measured, std::vector<double>& times) {
  for (size_t i = 0; i < world.size(); ++i) {
    const double t = kSweep * static_cast<double>(i) / static_cast<double>(world.size() - 1);
    times.push_back(t);
    measured.push_back(truePose(t).inverse() * world[i]);
  }
}
}  // namespace

TEST(M3PoseAt, InterpolatesAndClamps) {
  const Trajectory traj = trueTrajectory(3);  // t = 0, 0.05, 0.1
  EXPECT_TRUE(poseAt(traj, 0.025).matrix().isApprox(truePose(0.025).matrix(), 1e-9));
  EXPECT_TRUE(poseAt(traj, -1.0).matrix().isApprox(traj.front().T.matrix(), 1e-12));
  EXPECT_TRUE(poseAt(traj, 5.0).matrix().isApprox(traj.back().T.matrix(), 1e-12));
  EXPECT_TRUE(poseAt(traj, 0.05).matrix().isApprox(traj[1].T.matrix(), 1e-12));
}

TEST(M3PropagateImu, ConstantRateAndVelocity) {
  std::vector<estimation::ImuSample> imu;
  for (int k = 0; k <= 100; ++k) imu.push_back({k * 0.001, Vec3::Zero(), Vec3(0, 0, kYawRate)});
  const Trajectory traj = propagateImu(imu, Pose::Identity(), Vec3(kSpeed, 0, 0));
  ASSERT_EQ(traj.size(), imu.size());
  EXPECT_DOUBLE_EQ(traj.front().t, 0.0);
  EXPECT_TRUE(traj.back().T.linear().isApprox(truePose(0.1).linear(), 1e-9));
  EXPECT_TRUE(traj.back().T.translation().isApprox(Vec3(kSpeed * 0.1, 0, 0), 1e-9));
}

TEST(M3Deskew, RestoresKnownGeometry) {
  const PointCloud world = roomWorld();
  PointCloud measured;
  std::vector<double> times;
  skew(world, measured, times);

  double skewed_err = 0.0;
  for (size_t i = 0; i < world.size(); ++i)
    skewed_err = std::max(skewed_err, (measured[i] - world[i]).norm());
  ASSERT_GT(skewed_err, 1.0) << "the synthetic scan should be visibly distorted";

  const PointCloud fixed = deskew(measured, times, trueTrajectory(), 0.0);
  ASSERT_EQ(fixed.size(), world.size());
  for (size_t i = 0; i < world.size(); ++i)
    EXPECT_LT((fixed[i] - world[i]).norm(), 1e-6) << "point " << i;
}

TEST(M3Deskew, ReferenceTimeAtEndOfSweep) {
  const PointCloud world = roomWorld();
  PointCloud measured;
  std::vector<double> times;
  skew(world, measured, times);
  const PointCloud fixed = deskew(measured, times, trueTrajectory(), kSweep);
  const Pose T_end_world = truePose(kSweep).inverse();
  for (size_t i = 0; i < world.size(); i += 37)
    EXPECT_LT((fixed[i] - T_end_world * world[i]).norm(), 1e-6);
}

TEST(M3Deskew, UsesImuPropagatedTrajectory) {
  std::vector<estimation::ImuSample> imu;
  for (int k = 0; k <= 200; ++k)
    imu.push_back({k * kSweep / 200, Vec3::Zero(), Vec3(0, 0, kYawRate)});
  const Trajectory traj = propagateImu(imu, Pose::Identity(), Vec3(kSpeed, 0, 0));
  const PointCloud world = roomWorld();
  PointCloud measured;
  std::vector<double> times;
  skew(world, measured, times);
  const PointCloud fixed = deskew(measured, times, traj, 0.0);
  for (size_t i = 0; i < world.size(); i += 13) EXPECT_LT((fixed[i] - world[i]).norm(), 1e-3);
}

TEST(M3Deskew, RejectsSizeMismatch) {
  EXPECT_THROW(deskew({Vec3::Zero()}, {}, trueTrajectory(), 0.0), std::invalid_argument);
}
