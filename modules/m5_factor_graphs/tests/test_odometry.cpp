// Module 5 acceptance tests: odometry/lidar_odometry.hpp on a synthetic street.
#include <gtest/gtest.h>

#include <cmath>
#include <random>

#include "slam/odometry/lidar_odometry.hpp"

using namespace slam;

namespace {
PointCloud street(std::mt19937& rng) {
  std::normal_distribution<double> n(0.0, 0.01);
  PointCloud pts;
  for (double x = -30; x <= 60; x += 0.4)
    for (double y = -8; y <= 8; y += 0.5) pts.emplace_back(x + n(rng), y + n(rng), -1.7 + n(rng));
  for (double x = -30; x <= 60; x += 0.3)
    for (double z = -1.7; z <= 5; z += 0.35) {
      pts.emplace_back(x + n(rng), -8.0 + n(rng), z + n(rng));
      pts.emplace_back(x + n(rng), 8.0 + n(rng), z + n(rng));
    }
  for (double cx = -25; cx <= 55; cx += 7.0)
    for (double a = 0; a < 2 * M_PI; a += 0.2)
      for (double z = -1.7; z <= 2; z += 0.3)
        pts.emplace_back(cx + 0.3 * std::cos(a), 6.0 + 0.3 * std::sin(a), z + n(rng));
  return pts;
}

Pose truePose(int k) {
  Pose T = Pose::Identity();
  T.linear() = Eigen::AngleAxisd(0.01 * k, Vec3::UnitZ()).toRotationMatrix();
  T.translation() = Vec3(0.9 * k, 0.05 * k, 0.0);
  return T;
}

PointCloud scanAt(const PointCloud& world, const Pose& T_world_sensor, double range = 40.0) {
  PointCloud scan;
  const Pose T_sensor_world = T_world_sensor.inverse();
  for (const auto& p : world) {
    const Vec3 q = T_sensor_world * p;
    if (q.norm() < range) scan.push_back(q);
  }
  return scan;
}
}  // namespace

TEST(M5Odometry, FirstPoseIsIdentity) {
  std::mt19937 rng(0);
  odometry::LidarOdometry odom;
  const Pose T = odom.registerScan(scanAt(street(rng), Pose::Identity()));
  EXPECT_TRUE(T.matrix().isApprox(Eigen::Matrix4d::Identity()));
  EXPECT_FALSE(odom.localMap().empty());
}

TEST(M5Odometry, TracksSyntheticStreet) {
  std::mt19937 rng(1);
  const PointCloud world = street(rng);
  odometry::LidarOdometry odom;
  Pose last = Pose::Identity();
  for (int k = 0; k < 30; ++k) last = odom.registerScan(scanAt(world, truePose(k)));
  const Pose err = truePose(29).inverse() * last;
  const double path = (truePose(29).translation() - truePose(0).translation()).norm();
  EXPECT_LT(err.translation().norm(), 0.005 * path) << "drift above 0.5 % of the path length";
  EXPECT_LT(Eigen::AngleAxisd(err.linear()).angle(), 0.002);
  EXPECT_EQ(odom.poses().size(), 30u);
}

TEST(M5Odometry, PosesStayRigid) {
  std::mt19937 rng(2);
  const PointCloud world = street(rng);
  odometry::LidarOdometry odom;
  for (int k = 0; k < 40; ++k) odom.registerScan(scanAt(world, truePose(k)));
  for (const auto& T : odom.poses()) {
    const Mat3 R = T.linear();
    ASSERT_LT((R.transpose() * R - Mat3::Identity()).norm(), 1e-9);
  }
}
