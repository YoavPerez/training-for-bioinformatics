#pragma once
// Module 1: rigid-body geometry utilities.

#include "slam/types.hpp"

namespace slam::geometry {

// Skew-symmetric matrix such that skew(a) * b == a.cross(b). Provided.
Mat3 skew(const Vec3& v);

// T_a_c from T_a_b and T_b_c.
Pose compose(const Pose& T_a_b, const Pose& T_b_c);

// T_b_a from T_a_b. Must not call Eigen's generic inverse().
Pose inverse(const Pose& T_a_b);

// p_a from T_a_b and p_b.
Vec3 apply(const Pose& T_a_b, const Vec3& p_b);

// Applies T_a_b to every point of a cloud expressed in frame b.
PointCloud applyAll(const Pose& T_a_b, const PointCloud& cloud_b);

// Spherical linear interpolation, t in [0, 1]. Must take the shortest path
// and must return q0 at t = 0 and q1 at t = 1 (up to sign).
Quat slerp(const Quat& q0, const Quat& q1, double t);

// Interpolates a pose: SLERP on rotation, linear on translation.
Pose interpolate(const Pose& T0, const Pose& T1, double t);

// SO(3) exponential map: rotation vector (axis * angle, rad) -> rotation matrix.
Mat3 so3Exp(const Vec3& phi);

// SO(3) logarithm: rotation matrix -> rotation vector with angle in [0, pi].
// Must be accurate for small angles and for angles close to pi.
Vec3 so3Log(const Mat3& R);

}  // namespace slam::geometry
