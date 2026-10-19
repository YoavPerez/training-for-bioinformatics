#include "slam/io/kitti.hpp"

#include <fstream>
#include <iomanip>
#include <sstream>

namespace slam::io {

namespace {
std::ifstream openOrThrow(const std::string& path) {
  std::ifstream f(path);
  if (!f) throw std::runtime_error("cannot open " + path);
  return f;
}

std::vector<double> parseCsvLine(const std::string& line) {
  std::vector<double> v;
  std::stringstream ss(line);
  std::string cell;
  while (std::getline(ss, cell, ',')) v.push_back(std::stod(cell));
  return v;
}
}  // namespace

PointCloud readVelodyneBin(const std::string& path) {
  std::ifstream f(path, std::ios::binary);
  if (!f) throw std::runtime_error("cannot open " + path);
  PointCloud cloud;
  float buf[4];
  while (f.read(reinterpret_cast<char*>(buf), sizeof(buf)))
    cloud.emplace_back(buf[0], buf[1], buf[2]);
  return cloud;
}

std::vector<double> readColumn(const std::string& path) {
  auto f = openOrThrow(path);
  std::vector<double> out;
  double v;
  while (f >> v) out.push_back(v);
  return out;
}

Pose readPoseMatrix(const std::string& path) {
  auto f = openOrThrow(path);
  Eigen::Matrix4d M;
  for (int r = 0; r < 4; ++r)
    for (int c = 0; c < 4; ++c) f >> M(r, c);
  if (!f) throw std::runtime_error("bad 4x4 matrix in " + path);
  Pose T = Pose::Identity();
  T.matrix() = M;
  return T;
}

std::vector<estimation::ImuSample> readImuCsv(const std::string& path) {
  auto f = openOrThrow(path);
  std::vector<estimation::ImuSample> out;
  std::string line;
  std::getline(f, line);  // header
  while (std::getline(f, line)) {
    const auto v = parseCsvLine(line);
    if (v.size() < 7) continue;
    out.push_back({v[0], Vec3(v[1], v[2], v[3]), Vec3(v[4], v[5], v[6])});
  }
  return out;
}

std::vector<PositionFix> readGnssCsv(const std::string& path) {
  auto f = openOrThrow(path);
  std::vector<PositionFix> out;
  std::string line;
  std::getline(f, line);  // header
  while (std::getline(f, line)) {
    const auto v = parseCsvLine(line);
    if (v.size() < 7) continue;
    out.push_back({v[0], Vec3(v[1], v[2], v[3]), Vec3(v[4], v[5], v[6])});
  }
  return out;
}

sensors::Trajectory readTum(const std::string& path) {
  auto f = openOrThrow(path);
  sensors::Trajectory traj;
  double t, x, y, z, qx, qy, qz, qw;
  std::string line;
  while (std::getline(f, line)) {
    if (line.empty() || line[0] == '#') continue;
    std::stringstream ss(line);
    ss >> t >> x >> y >> z >> qx >> qy >> qz >> qw;
    Pose T = Pose::Identity();
    T.linear() = Quat(qw, qx, qy, qz).normalized().toRotationMatrix();
    T.translation() = Vec3(x, y, z);
    traj.push_back({t, T});
  }
  return traj;
}

void writeTum(const std::string& path, const sensors::Trajectory& traj) {
  std::ofstream f(path);
  if (!f) throw std::runtime_error("cannot write " + path);
  f << std::fixed << std::setprecision(9);
  for (const auto& tp : traj) {
    Quat q(tp.T.linear());
    if (q.w() < 0) q.coeffs() *= -1.0;  // canonical hemisphere: q and -q are the same rotation
    const Vec3& p = tp.T.translation();
    f << tp.t << ' ' << p.x() << ' ' << p.y() << ' ' << p.z() << ' ' << q.x() << ' ' << q.y() << ' '
      << q.z() << ' ' << q.w() << '\n';
  }
}

std::map<std::string, std::vector<double>> readCalib(const std::string& path) {
  auto f = openOrThrow(path);
  std::map<std::string, std::vector<double>> out;
  std::string line;
  while (std::getline(f, line)) {
    const auto colon = line.find(':');
    if (colon == std::string::npos) continue;
    std::stringstream ss(line.substr(colon + 1));
    std::vector<double> v;
    double x;
    while (ss >> x) v.push_back(x);
    out[line.substr(0, colon)] = v;
  }
  return out;
}

Pose calibToPose(const std::map<std::string, std::vector<double>>& calib) {
  const auto& R = calib.at("R");
  const auto& t = calib.at("T");
  Pose T = Pose::Identity();
  T.linear() << R[0], R[1], R[2], R[3], R[4], R[5], R[6], R[7], R[8];
  T.translation() = Vec3(t[0], t[1], t[2]);
  return T;
}

}  // namespace slam::io
