// Deskews a scan with the module 3 code. Used by the module 3 experiments and tests.
// Usage: deskew_scan <points.csv> <trajectory.tum> <out.csv> <t_ref> [time_offset]
//   points.csv: "x,y,z,t" per line (sensor frame, per-point time), no header
//   trajectory.tum: T_world_sensor samples in TUM format
//   time_offset: added to every point time before deskewing (to simulate clock offsets)
#include <fstream>
#include <iostream>
#include <sstream>

#include "slam/io/kitti.hpp"
#include "slam/sensors/deskew.hpp"

using namespace slam;

int main(int argc, char** argv) {
  if (argc < 5) {
    std::cerr
        << "usage: deskew_scan <points.csv> <trajectory.tum> <out.csv> <t_ref> [time_offset]\n";
    return 2;
  }
  const double offset = argc > 5 ? std::stod(argv[5]) : 0.0;
  std::ifstream in(argv[1]);
  if (!in) {
    std::cerr << "cannot open " << argv[1] << '\n';
    return 1;
  }
  PointCloud points;
  std::vector<double> times;
  std::string line;
  while (std::getline(in, line)) {
    std::stringstream ss(line);
    double x, y, z, t;
    char c;
    if (ss >> x >> c >> y >> c >> z >> c >> t) {
      points.emplace_back(x, y, z);
      times.push_back(t + offset);
    }
  }
  const auto traj = io::readTum(argv[2]);
  const PointCloud out = sensors::deskew(points, times, traj, std::stod(argv[4]));
  std::ofstream f(argv[3]);
  f.precision(9);
  for (const auto& p : out) f << p.x() << ',' << p.y() << ',' << p.z() << '\n';
  return 0;
}
