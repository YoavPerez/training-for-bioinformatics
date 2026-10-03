// Module 1 acceptance tests: geometry/transform.hpp
#include <gtest/gtest.h>

#include <cmath>
#include <random>

#include "slam/geometry/transform.hpp"

using namespace slam;
using namespace slam::geometry;

namespace {
Pose randomPose(std::mt19937& rng) {
  std::normal_distribution<double> n(0.0, 1.0);
  Pose T = Pose::Identity();
  T.linear() = Quat(n(rng), n(rng), n(rng), n(rng)).normalized().toRotationMatrix();
  T.translation() = Vec3(n(rng), n(rng), n(rng)) * 10.0;
  return T;
}

bool isRotation(const Mat3& R, double tol = 1e-9) {
  return (R.transpose() * R - Mat3::Identity()).norm() < tol &&
         std::abs(R.determinant() - 1.0) < tol;
}

double angleBetween(const Mat3& A, const Mat3& B) {
  return Eigen::AngleAxisd(A.transpose() * B).angle();
}
}  // namespace

TEST(M1Compose, MatchesHandComputedExample) {
  Pose T_a_b = Pose::Identity();
  T_a_b.linear() = Eigen::AngleAxisd(M_PI / 2, Vec3::UnitZ()).toRotationMatrix();
  T_a_b.translation() = Vec3(1, 0, 0);
  Pose T_b_c = Pose::Identity();
  T_b_c.translation() = Vec3(1, 0, 0);
  const Pose T_a_c = compose(T_a_b, T_b_c);
  EXPECT_TRUE(T_a_c.translation().isApprox(Vec3(1, 1, 0), 1e-12));
}

TEST(M1Compose, InverseRoundTrip) {
  std::mt19937 rng(1);
  for (int i = 0; i < 100; ++i) {
    const Pose T = randomPose(rng);
    EXPECT_TRUE(compose(T, inverse(T)).matrix().isApprox(Eigen::Matrix4d::Identity(), 1e-12));
    EXPECT_TRUE(compose(inverse(T), T).matrix().isApprox(Eigen::Matrix4d::Identity(), 1e-12));
    EXPECT_TRUE(inverse(inverse(T)).matrix().isApprox(T.matrix(), 1e-12));
  }
}

TEST(M1Compose, Associative) {
  std::mt19937 rng(2);
  const Pose A = randomPose(rng), B = randomPose(rng), C = randomPose(rng);
  EXPECT_TRUE(
      compose(compose(A, B), C).matrix().isApprox(compose(A, compose(B, C)).matrix(), 1e-12));
}

TEST(M1Apply, ConsistentWithCompose) {
  std::mt19937 rng(3);
  const Pose T_a_b = randomPose(rng), T_b_c = randomPose(rng);
  const Vec3 p_c(0.3, -2.0, 5.0);
  EXPECT_TRUE(apply(compose(T_a_b, T_b_c), p_c).isApprox(apply(T_a_b, apply(T_b_c, p_c)), 1e-12));
  const PointCloud cloud{p_c, Vec3::Zero(), Vec3::UnitX()};
  const PointCloud out = applyAll(T_a_b, cloud);
  ASSERT_EQ(out.size(), 3u);
  EXPECT_TRUE(out[1].isApprox(T_a_b.translation(), 1e-12));
}

TEST(M1So3, ExpOfZeroIsIdentity) { EXPECT_TRUE(so3Exp(Vec3::Zero()).isApprox(Mat3::Identity())); }

TEST(M1So3, ExpMatchesAngleAxis) {
  const Vec3 phi(0.1, -0.4, 0.7);
  const Mat3 expected = Eigen::AngleAxisd(phi.norm(), phi.normalized()).toRotationMatrix();
  EXPECT_TRUE(so3Exp(phi).isApprox(expected, 1e-12));
}

TEST(M1So3, ExpLogRoundTrip) {
  std::mt19937 rng(4);
  std::uniform_real_distribution<double> u(-1.0, 1.0);
  for (int i = 0; i < 200; ++i) {
    Vec3 axis(u(rng), u(rng), u(rng));
    axis.normalize();
    const double angle = std::abs(u(rng)) * (M_PI - 1e-3);
    const Vec3 phi = axis * angle;
    const Mat3 R = so3Exp(phi);
    EXPECT_TRUE(isRotation(R));
    EXPECT_TRUE(so3Log(R).isApprox(phi, 1e-7)) << "angle " << angle;
  }
}

TEST(M1So3, SmallAngles) {
  for (double angle : {1e-12, 1e-9, 1e-6}) {
    const Vec3 phi = Vec3(1, 2, 3).normalized() * angle;
    EXPECT_TRUE(isRotation(so3Exp(phi)));
    EXPECT_LT((so3Log(so3Exp(phi)) - phi).norm(), 1e-12 + 1e-6 * angle);
  }
}

TEST(M1So3, NearPi) {
  for (double eps : {1e-3, 1e-6, 1e-9, 0.0}) {
    const Vec3 axis = Vec3(1, -2, 0.5).normalized();
    const Mat3 R = Eigen::AngleAxisd(M_PI - eps, axis).toRotationMatrix();
    const Vec3 phi = so3Log(R);
    ASSERT_TRUE(phi.allFinite()) << "eps " << eps;
    EXPECT_NEAR(phi.norm(), M_PI - eps, 1e-6) << "eps " << eps;
    EXPECT_LT(angleBetween(so3Exp(phi), R), 1e-6) << "eps " << eps;
  }
}

TEST(M1Quat, SignAmbiguityGivesSameRotation) {
  const Quat q = Quat(0.3, -0.5, 0.2, 0.75).normalized();
  const Quat mq(-q.w(), -q.x(), -q.y(), -q.z());
  EXPECT_TRUE(so3Log(q.toRotationMatrix()).isApprox(so3Log(mq.toRotationMatrix()), 1e-9));
}

TEST(M1Slerp, Endpoints) {
  const Quat q0 = Quat(Eigen::AngleAxisd(0.2, Vec3::UnitX()));
  const Quat q1 = Quat(Eigen::AngleAxisd(1.3, Vec3(1, 1, 0).normalized()));
  EXPECT_LT(q0.angularDistance(slerp(q0, q1, 0.0)), 1e-9);
  EXPECT_LT(q1.angularDistance(slerp(q0, q1, 1.0)), 1e-9);
}

TEST(M1Slerp, MidpointIsHalfAngle) {
  const Quat q0 = Quat::Identity();
  const Quat q1 = Quat(Eigen::AngleAxisd(1.0, Vec3::UnitZ()));
  const Quat mid = slerp(q0, q1, 0.5);
  EXPECT_NEAR(mid.angularDistance(Quat(Eigen::AngleAxisd(0.5, Vec3::UnitZ()))), 0.0, 1e-9);
  EXPECT_NEAR(std::abs(mid.norm() - 1.0), 0.0, 1e-12);
}

TEST(M1Slerp, TakesShortestPathWhenSignsDiffer) {
  const Quat q0 = Quat(Eigen::AngleAxisd(0.1, Vec3::UnitZ()));
  Quat q1 = Quat(Eigen::AngleAxisd(0.3, Vec3::UnitZ()));
  q1.coeffs() *= -1.0;  // same rotation, opposite hemisphere
  const Quat mid = slerp(q0, q1, 0.5);
  EXPECT_LT(mid.angularDistance(Quat(Eigen::AngleAxisd(0.2, Vec3::UnitZ()))), 1e-9);
}

TEST(M1Slerp, NearlyIdenticalInputsStayFinite) {
  const Quat q0 = Quat(Eigen::AngleAxisd(0.5, Vec3::UnitY()));
  const Quat q1 = Quat(Eigen::AngleAxisd(0.5 + 1e-12, Vec3::UnitY()));
  EXPECT_TRUE(slerp(q0, q1, 0.3).coeffs().allFinite());
}

TEST(M1Interpolate, Endpoints) {
  std::mt19937 rng(5);
  const Pose A = randomPose(rng), B = randomPose(rng);
  EXPECT_TRUE(interpolate(A, B, 0.0).matrix().isApprox(A.matrix(), 1e-9));
  EXPECT_TRUE(interpolate(A, B, 1.0).matrix().isApprox(B.matrix(), 1e-9));
  EXPECT_TRUE(isRotation(interpolate(A, B, 0.37).linear()));
}
