// Runs the module 2 ESKF over files written by `python -m slampipe.prepare`.
// Usage: eskf_run <prep_dir> <out.csv> [--outage <t_start> <t_end>]
//                 [--imu-noise <acc> <gyro> <acc_bias_rw> <gyro_bias_rw>]
//                 [--p0-bias <sigma_acc_bias> <sigma_gyro_bias>]
// --imu-noise: continuous-time densities (units as in ImuNoise, eskf.hpp).
// --p0-bias: initial 1-sigma of the acc bias [m/s^2] and gyro bias [rad/s].
// Output CSV: t,x,y,z,sx,sy,sz (position and its 1-sigma per axis).
#include <cmath>
#include <fstream>
#include <iostream>
#include <string>

#include "slam/estimation/eskf.hpp"
#include "slam/io/kitti.hpp"

using namespace slam;

int main(int argc, char** argv) {
  const char* usage =
      "usage: eskf_run <prep_dir> <out.csv> [--outage t0 t1] [--imu-noise acc gyro acc_bw gyro_bw]"
      " [--p0-bias sigma_ba sigma_bg]\n";
  if (argc < 3) {
    std::cerr << usage;
    return 2;
  }
  const std::string prep = argv[1];
  double outage0 = -1.0, outage1 = -1.0;
  estimation::ImuNoise noise{0.05, 0.005, 0.001, 0.0001};
  // Initial 1-sigma per error-state block. Position, velocity, attitude: the start is taken from
  // the OXTS solution (gt.tum), so 0.1 m, 0.1 m/s and 1 degree. Biases: a high-grade INS such as
  // the KITTI OXTS unit; a much larger gyro-bias sigma lets the first GNSS fixes (noise) leak
  // into the bias estimate. Override with --p0-bias.
  double sigma_ba = 0.02, sigma_bg = 1e-4;
  try {
    for (int i = 3; i < argc; ++i) {
      const std::string flag = argv[i];
      if (flag == "--outage" && i + 2 < argc) {
        outage0 = std::stod(argv[++i]);
        outage1 = std::stod(argv[++i]);
      } else if (flag == "--imu-noise" && i + 4 < argc) {
        noise.acc_noise = std::stod(argv[++i]);
        noise.gyro_noise = std::stod(argv[++i]);
        noise.acc_bias_rw = std::stod(argv[++i]);
        noise.gyro_bias_rw = std::stod(argv[++i]);
      } else if (flag == "--p0-bias" && i + 2 < argc) {
        sigma_ba = std::stod(argv[++i]);
        sigma_bg = std::stod(argv[++i]);
      } else {
        std::cerr << usage;
        return 2;
      }
    }
  } catch (const std::exception&) {
    std::cerr << usage;
    return 2;
  }
  const auto imu = io::readImuCsv(prep + "/imu.csv");
  const auto gnss = io::readGnssCsv(prep + "/gnss.csv");
  const auto gt = io::readTum(prep + "/gt.tum");
  if (imu.size() < 2 || gnss.empty() || gt.empty()) {
    std::cerr << "empty input\n";
    return 1;
  }

  estimation::NominalState x0;
  x0.p = gt.front().T.translation();
  x0.q = Quat(gt.front().T.linear());
  if (gt.size() > 1) x0.v = (gt[1].T.translation() - gt[0].T.translation()) / (gt[1].t - gt[0].t);
  const double deg = M_PI / 180.0;
  estimation::Eskf::Cov P0 = estimation::Eskf::Cov::Zero();
  P0.block<3, 3>(0, 0) = Mat3::Identity() * 0.1 * 0.1;              // position [m]
  P0.block<3, 3>(3, 3) = Mat3::Identity() * 0.1 * 0.1;              // velocity [m/s]
  P0.block<3, 3>(6, 6) = Mat3::Identity() * deg * deg;              // attitude [rad]
  P0.block<3, 3>(9, 9) = Mat3::Identity() * sigma_ba * sigma_ba;    // acc bias [m/s^2]
  P0.block<3, 3>(12, 12) = Mat3::Identity() * sigma_bg * sigma_bg;  // gyro bias [rad/s]
  estimation::Eskf filter(x0, P0, noise);

  std::ofstream out(argv[2]);
  out << "t,x,y,z,sx,sy,sz\n";
  size_t g = 0;
  for (size_t k = 0; k + 1 < imu.size(); ++k) {
    filter.predict(imu[k], imu[k + 1].t - imu[k].t);
    const double t = imu[k + 1].t;
    while (g < gnss.size() && gnss[g].t <= t + 1e-6) {
      const bool in_outage = gnss[g].t >= outage0 && gnss[g].t <= outage1;
      if (!in_outage)
        filter.updatePosition(gnss[g].p, gnss[g].sigma.cwiseAbs2().asDiagonal().toDenseMatrix());
      ++g;
    }
    const auto& s = filter.state();
    const auto& P = filter.covariance();
    out << t << ',' << s.p.x() << ',' << s.p.y() << ',' << s.p.z() << ',' << std::sqrt(P(0, 0))
        << ',' << std::sqrt(P(1, 1)) << ',' << std::sqrt(P(2, 2)) << '\n';
  }
  return 0;
}
