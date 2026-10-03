#include "slam/geometry/transform.hpp"

namespace slam::geometry {

Mat3 skew(const Vec3& v) {
  Mat3 S;
  S << 0.0, -v.z(), v.y(),  //
      v.z(), 0.0, -v.x(),   //
      -v.y(), v.x(), 0.0;
  return S;
}

Pose compose(const Pose& T_a_b, const Pose& T_b_c) {
  // TODO(m1): implement.
  (void)T_a_b;
  (void)T_b_c;
  throw NotImplemented("geometry::compose");
}

Pose inverse(const Pose& T_a_b) {
  // TODO(m1): implement using the structure of a rigid transform.
  (void)T_a_b;
  throw NotImplemented("geometry::inverse");
}

Vec3 apply(const Pose& T_a_b, const Vec3& p_b) {
  // TODO(m1): implement.
  (void)T_a_b;
  (void)p_b;
  throw NotImplemented("geometry::apply");
}

PointCloud applyAll(const Pose& T_a_b, const PointCloud& cloud_b) {
  // TODO(m1): implement.
  (void)T_a_b;
  (void)cloud_b;
  throw NotImplemented("geometry::applyAll");
}

Quat slerp(const Quat& q0, const Quat& q1, double t) {
  // TODO(m1): implement. Do not call Eigen's Quaternion::slerp.
  (void)q0;
  (void)q1;
  (void)t;
  throw NotImplemented("geometry::slerp");
}

Pose interpolate(const Pose& T0, const Pose& T1, double t) {
  // TODO(m1): implement.
  (void)T0;
  (void)T1;
  (void)t;
  throw NotImplemented("geometry::interpolate");
}

Mat3 so3Exp(const Vec3& phi) {
  // TODO(m1): implement. Do not call Eigen::AngleAxisd.
  (void)phi;
  throw NotImplemented("geometry::so3Exp");
}

Vec3 so3Log(const Mat3& R) {
  // TODO(m1): implement. Do not call Eigen::AngleAxisd.
  (void)R;
  throw NotImplemented("geometry::so3Log");
}

}  // namespace slam::geometry
