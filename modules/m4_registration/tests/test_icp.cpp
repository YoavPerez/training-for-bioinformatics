// Module 4 acceptance tests: registration/icp.hpp
#include <gtest/gtest.h>

#include <chrono>
#include <cmath>
#include <random>

#include "slam/geometry/transform.hpp"
#include "slam/registration/icp.hpp"
#include "slam/registration/normals.hpp"

using namespace slam;
using namespace slam::registration;

namespace {
// A street-like scene: ground, two building facades, a few boxes and poles.
PointCloud scene(std::mt19937& rng, double noise = 0.01) {
  std::normal_distribution<double> n(0.0, noise);
  PointCloud pts;
  for (double x = -20; x <= 20; x += 0.4)
    for (double y = -8; y <= 8; y += 0.4) pts.emplace_back(x + n(rng), y + n(rng), -1.7 + n(rng));
  for (double x = -20; x <= 20; x += 0.3)
    for (double z = -1.7; z <= 6; z += 0.3) {
      pts.emplace_back(x + n(rng), -8.0 + n(rng), z + n(rng));
      pts.emplace_back(x + n(rng), 8.0 + n(rng), z + n(rng));
    }
  for (double cx : {-12.0, -3.0, 5.0, 14.0})
    for (double a = 0; a < 2 * M_PI; a += 0.15)
      for (double z = -1.7; z <= 2.0; z += 0.25)
        pts.emplace_back(cx + 0.3 * std::cos(a) + n(rng), 5.0 + 0.3 * std::sin(a) + n(rng),
                         z + n(rng));
  for (double x = 0; x <= 2; x += 0.2)
    for (double y = -4; y <= -2.5; y += 0.2)
      for (double z : {-1.7, -0.5}) pts.emplace_back(x + 7.0 + n(rng), y + n(rng), z + n(rng));
  return pts;
}

Pose makePose(double yaw_deg, double roll_deg, const Vec3& t) {
  Pose T = Pose::Identity();
  T.linear() = (Eigen::AngleAxisd(yaw_deg * M_PI / 180, Vec3::UnitZ()) *
                Eigen::AngleAxisd(roll_deg * M_PI / 180, Vec3::UnitX()))
                   .toRotationMatrix();
  T.translation() = t;
  return T;
}

struct Errors {
  double trans, rot_deg;
};
Errors poseError(const Pose& A, const Pose& B) {
  const Pose D = A.inverse() * B;
  return {D.translation().norm(), Eigen::AngleAxisd(D.linear()).angle() * 180 / M_PI};
}

// source = target expressed in a frame displaced by T_target_source (plus independent noise).
void makePair(const Pose& T_target_source, PointCloud& source, PointCloud& target, unsigned seed) {
  std::mt19937 rng(seed);
  target = scene(rng);
  PointCloud other = scene(rng);  // independent noise realisation for the source
  const Pose T_source_target = T_target_source.inverse();
  source.clear();
  for (const auto& p : other) source.push_back(T_source_target * p);
}
}  // namespace

TEST(M4Icp, IdentityWhenCloudsCoincide) {
  std::mt19937 rng(0);
  const PointCloud cloud = scene(rng, 0.0);
  const auto res = icpPointToPlane(cloud, cloud, estimateNormals(cloud), Pose::Identity());
  EXPECT_TRUE(res.converged);
  EXPECT_LT(poseError(res.T_target_source, Pose::Identity()).trans, 1e-6);
}

TEST(M4Icp, RecoversKnownTransform) {
  const Pose truth = makePose(4.0, 1.0, Vec3(0.6, -0.3, 0.05));
  PointCloud source, target;
  makePair(truth, source, target, 1);
  const auto res = icpPointToPlane(source, target, estimateNormals(target), Pose::Identity());
  const Errors e = poseError(res.T_target_source, truth);
  EXPECT_TRUE(res.converged);
  EXPECT_LT(e.trans, 0.01);
  EXPECT_LT(e.rot_deg, 0.05);
  EXPECT_GT(res.num_correspondences, source.size() / 2);
}

TEST(M4Icp, ResultIsARigidTransform) {
  const Pose truth = makePose(8.0, 0.0, Vec3(1.0, 0.2, 0.0));
  PointCloud source, target;
  makePair(truth, source, target, 2);
  const Pose T =
      icpPointToPlane(source, target, estimateNormals(target), Pose::Identity()).T_target_source;
  const Mat3 R = T.linear();
  EXPECT_LT((R.transpose() * R - Mat3::Identity()).norm(), 1e-9);
  EXPECT_NEAR(R.determinant(), 1.0, 1e-9);
}

TEST(M4Icp, ConvergenceBasin) {
  // Initial errors up to 1 m and 5 deg must still converge on this scene.
  const Pose truth = makePose(2.0, 0.0, Vec3(0.5, 0.0, 0.0));
  PointCloud source, target;
  makePair(truth, source, target, 3);
  const auto normals = estimateNormals(target);
  for (double dx : {-1.0, 1.0})
    for (double dyaw : {-5.0, 5.0}) {
      const Pose init = truth * makePose(dyaw, 0.0, Vec3(dx, 0.0, 0.0));
      const Errors e = poseError(
          icpPointToPlane(source, target, normals, init, {60, 2.0}).T_target_source, truth);
      EXPECT_LT(e.trans, 0.02) << "init dx=" << dx << " dyaw=" << dyaw;
    }
}

TEST(M4Icp, HuberKernelHandlesOutliers) {
  const Pose truth = makePose(3.0, 0.0, Vec3(0.4, 0.1, 0.0));
  PointCloud source, target;
  makePair(truth, source, target, 4);
  std::mt19937 rng(5);
  std::uniform_real_distribution<double> u(-15.0, 15.0);
  const size_t n_out = source.size() / 5;  // 20 % clutter close to real structure
  for (size_t i = 0; i < n_out; ++i) source.emplace_back(u(rng), u(rng) * 0.5, u(rng) * 0.2);
  IcpConfig cfg;
  cfg.huber_threshold = 0.05;
  const Errors robust =
      poseError(icpPointToPlane(source, target, estimateNormals(target), Pose::Identity(), cfg)
                    .T_target_source,
                truth);
  EXPECT_LT(robust.trans, 0.02);
  EXPECT_LT(robust.rot_deg, 0.1);
}

TEST(M4Icp, ReportsFailureWhenNothingOverlaps) {
  std::mt19937 rng(6);
  const PointCloud target = scene(rng);
  PointCloud far;
  for (const auto& p : target) far.push_back(p + Vec3(1000, 0, 0));
  const auto res = icpPointToPlane(far, target, estimateNormals(target), Pose::Identity());
  EXPECT_FALSE(res.converged);
  EXPECT_EQ(res.num_correspondences, 0u);
}

TEST(M4Icp, RuntimeBudget) {
  // Generous budget: a ~25k-point pair must register in under 2 s in a Release build.
  const Pose truth = makePose(3.0, 0.0, Vec3(0.5, 0.0, 0.0));
  PointCloud source, target;
  makePair(truth, source, target, 7);
  const auto normals = estimateNormals(target);
  const auto t0 = std::chrono::steady_clock::now();
  icpPointToPlane(source, target, normals, Pose::Identity());
  const double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  EXPECT_LT(s, 2.0) << "source size " << source.size();
}
