#include "slam/estimation/eskf.hpp"

#include "slam/geometry/transform.hpp"

namespace slam::estimation {

Eskf::Eskf(const NominalState& x0, const Cov& P0, const ImuNoise& noise, const Vec3& gravity)
    : x_(x0), P_(P0), noise_(noise), gravity_(gravity) {}

void Eskf::predict(const ImuSample& imu, double dt) {
  // TODO(m2): propagate the nominal state, then the error covariance (F P F^T + Q).
  (void)imu;
  (void)dt;
  throw NotImplemented("Eskf::predict");
}

void Eskf::updatePosition(const Vec3& p_meas, const Mat3& R) {
  // TODO(m2): Kalman update on the error state, inject into the nominal state, reset.
  (void)p_meas;
  (void)R;
  throw NotImplemented("Eskf::updatePosition");
}

}  // namespace slam::estimation
