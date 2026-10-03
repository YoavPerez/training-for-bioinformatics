#pragma once
// Module 2: loosely coupled GNSS + IMU error-state EKF (3D).

#include "slam/types.hpp"

namespace slam::estimation {

// IMU sample in the IMU (body) frame. acc is specific force [m/s^2], gyro is angular rate [rad/s].
struct ImuSample {
  double t = 0.0;
  Vec3 acc = Vec3::Zero();
  Vec3 gyro = Vec3::Zero();
};

// Continuous-time noise densities (see the Kalibr IMU noise model page for units).
struct ImuNoise {
  double acc_noise = 0.0;     // [m/s^2/sqrt(Hz)]
  double gyro_noise = 0.0;    // [rad/s/sqrt(Hz)]
  double acc_bias_rw = 0.0;   // [m/s^3/sqrt(Hz)]
  double gyro_bias_rw = 0.0;  // [rad/s^2/sqrt(Hz)]
};

// Nominal state. Position and velocity in the local world (ENU) frame;
// q is the orientation of the IMU in the world frame (R_world_imu).
struct NominalState {
  Vec3 p = Vec3::Zero();
  Vec3 v = Vec3::Zero();
  Quat q = Quat::Identity();
  Vec3 ba = Vec3::Zero();
  Vec3 bg = Vec3::Zero();
};

// Error-state ordering (fixed, tests rely on it):
//   [0:3) dp, [3:6) dv, [6:9) dtheta (local/right perturbation: R = R_nom * Exp(dtheta)),
//   [9:12) d acc bias, [12:15) d gyro bias.
class Eskf {
 public:
  static constexpr int kDim = 15;
  using Cov = Eigen::Matrix<double, kDim, kDim>;

  Eskf(const NominalState& x0, const Cov& P0, const ImuNoise& noise,
       const Vec3& gravity = Vec3(0.0, 0.0, -9.81));

  // Propagates nominal state and covariance with one IMU sample held over dt seconds.
  void predict(const ImuSample& imu, double dt);

  // Fuses a position measurement (e.g. GNSS converted to local ENU) with covariance R.
  void updatePosition(const Vec3& p_meas, const Mat3& R);

  const NominalState& state() const { return x_; }
  const Cov& covariance() const { return P_; }

 private:
  NominalState x_;
  Cov P_;
  ImuNoise noise_;
  Vec3 gravity_;
};

}  // namespace slam::estimation
