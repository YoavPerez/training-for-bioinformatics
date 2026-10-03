// Runs the module 2 ESKF over files written by `python -m slampipe.prepare`.
// Usage: eskf_run <prep_dir> <out.csv> [--outage <t_start> <t_end>]
// Output CSV: t,x,y,z,sx,sy,sz (position and its 1-sigma per axis).
#include <fstream>
#include <iostream>

#include "slam/estimation/eskf.hpp"
#include "slam/io/kitti.hpp"

using namespace slam;

int main(int argc, char** argv) {
  if (argc < 3) {
    std::cerr << "usage: eskf_run <prep_dir> <out.csv> [--outage t0 t1]\n";
    return 2;
  }
  const std::string prep = argv[1];
  double outage0 = -1.0, outage1 = -1.0;
  if (argc >= 6 && std::string(argv[3]) == "--outage") {
    outage0 = std::stod(argv[4]);
    outage1 = std::stod(argv[5]);
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
  estimation::Eskf::Cov P0 = estimation::Eskf::Cov::Identity() * 1e-2;
  const estimation::ImuNoise noise{0.05, 0.005, 0.001, 0.0001};
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
