// End-to-end pipeline (modules 5 and 6): LiDAR odometry + factor graph with GNSS, IMU and loops.
// Inputs come from a KITTI raw drive and from `python -m slampipe.prepare`.
//
// Usage: run_pipeline <drive_dir> <prep_dir> <out_dir> [options]
//   --no-gnss              do not add GNSS factors
//   --imu                  add IMU preintegration factors
//   --loops                detect, verify and add loop closures
//   --deskew               deskew each scan (module 3) with the previous odometry step as motion
//   --false-loop <i> <j>   inject a wrong loop (identity transform) between frames i and j
//   --max-frames <n>       process at most n frames
// Writes <out_dir>/odometry.tum and <out_dir>/optimized.tum (body/IMU frame poses in local ENU).
#include <cmath>
#include <cstdio>
#include <iostream>
#include <set>

#include "slam/backend/graph_builder.hpp"
#include "slam/geometry/transform.hpp"
#include "slam/io/kitti.hpp"
#include "slam/loop/scan_context.hpp"
#include "slam/odometry/lidar_odometry.hpp"
#include "slam/registration/normals.hpp"

using namespace slam;

namespace {
backend::Sigmas6 sigmas6(double rot, double trans) {
  backend::Sigmas6 s;
  s << rot, rot, rot, trans, trans, trans;
  return s;
}

// IMU samples covering exactly [t0, t1]: the sample in force at t0 (clamped to t0), the samples
// inside the interval, and a copy of the last one stamped t1.
std::vector<estimation::ImuSample> imuBetween(const std::vector<estimation::ImuSample>& imu,
                                              double t0, double t1) {
  std::vector<estimation::ImuSample> seg;
  for (size_t i = 0; i < imu.size(); ++i) {
    const bool in_force_at_t0 = imu[i].t <= t0 && (i + 1 == imu.size() || imu[i + 1].t > t0);
    if (in_force_at_t0) {
      seg.push_back(imu[i]);
      seg.back().t = t0;
    } else if (imu[i].t > t0 && imu[i].t < t1) {
      seg.push_back(imu[i]);
    }
  }
  if (!seg.empty()) {
    seg.push_back(seg.back());
    seg.back().t = t1;
  }
  return seg;
}

// Assumption to verify (module 6 ablation): the HDL-64 spins clockwise seen from above, each sweep
// starts and ends behind the car, and the scan timestamp corresponds to the forward direction.
// Per-point time is therefore the clockwise azimuth from the rear, and t_ref is mid-sweep.
constexpr double kSweep = 0.1;  // [s]

PointCloud deskewScan(const PointCloud& scan, const Pose& T_prev_cur) {
  std::vector<double> times;
  times.reserve(scan.size());
  for (const auto& p : scan)
    times.push_back((M_PI - std::atan2(p.y(), p.x())) / (2.0 * M_PI) * kSweep);
  const Pose half = geometry::interpolate(Pose::Identity(), T_prev_cur, 0.5);
  const sensors::Trajectory traj{
      {0.0, geometry::inverse(half)}, {0.5 * kSweep, Pose::Identity()}, {kSweep, half}};
  return sensors::deskew(scan, times, traj, 0.5 * kSweep);
}

std::string scanPath(const std::string& drive, size_t k) {
  char name[32];
  std::snprintf(name, sizeof(name), "%010zu.bin", k);
  return drive + "/velodyne_points/data/" + name;
}
}  // namespace

int main(int argc, char** argv) {
  if (argc < 4) {
    std::cerr << "usage: run_pipeline <drive_dir> <prep_dir> <out_dir> [options]\n";
    return 2;
  }
  const std::string drive = argv[1], prep = argv[2], out = argv[3];
  bool use_gnss = true, use_imu = false, use_loops = false, use_deskew = false;
  int false_i = -1, false_j = -1;
  size_t max_frames = static_cast<size_t>(-1);
  for (int a = 4; a < argc; ++a) {
    const std::string arg = argv[a];
    if (arg == "--no-gnss")
      use_gnss = false;
    else if (arg == "--imu")
      use_imu = true;
    else if (arg == "--loops")
      use_loops = true;
    else if (arg == "--deskew")
      use_deskew = true;
    else if (arg == "--false-loop" && a + 2 < argc) {
      false_i = std::stoi(argv[++a]);
      false_j = std::stoi(argv[++a]);
    } else if (arg == "--max-frames" && a + 1 < argc)
      max_frames = std::stoul(argv[++a]);
    else {
      std::cerr << "unknown option " << arg << '\n';
      return 2;
    }
  }

  const auto times = io::readColumn(prep + "/lidar_times.csv");
  const Pose T_imu_lidar = io::readPoseMatrix(prep + "/T_imu_lidar.txt");
  const Pose T_lidar_imu = geometry::inverse(T_imu_lidar);
  const auto gt = io::readTum(prep + "/gt.tum");
  const auto gnss = io::readGnssCsv(prep + "/gnss.csv");
  const auto imu = io::readImuCsv(prep + "/imu.csv");
  const size_t n = std::min(times.size(), max_frames);

  // 1. LiDAR odometry.
  odometry::LidarOdometry odom;
  std::vector<PointCloud> keyframe_scans;
  sensors::Trajectory odom_traj;
  const Pose T_world_body0 = gt.front().T;  // initial attitude and position from the INS
  for (size_t k = 0; k < n; ++k) {
    PointCloud scan = io::readVelodyneBin(scanPath(drive, k));
    if (use_deskew && odom.poses().size() >= 2) {
      const auto& P = odom.poses();
      scan = deskewScan(scan, geometry::compose(geometry::inverse(P[P.size() - 2]), P.back()));
    }
    const Pose T_l0_lk = odom.registerScan(scan);
    const Pose T_b0_bk = T_imu_lidar * T_l0_lk * T_lidar_imu;
    odom_traj.push_back({times[k], T_world_body0 * T_b0_bk});
    if (use_loops) keyframe_scans.push_back(registration::voxelDownsample(scan, 0.5));
    std::cerr << "\rodometry " << k + 1 << '/' << n << std::flush;
  }
  std::cerr << '\n';
  io::writeTum(out + "/odometry.tum", odom_traj);

  // 2. Factor graph.
  backend::GraphBuilder graph;
  for (size_t k = 0; k < n; ++k) {
    Vec3 v = Vec3::Zero();
    if (k > 0)
      v = (odom_traj[k].T.translation() - odom_traj[k - 1].T.translation()) /
          (times[k] - times[k - 1]);
    graph.setInitial(static_cast<int>(k), odom_traj[k].T, v);
  }
  graph.addPrior(0, T_world_body0, sigmas6(0.01, 0.1));
  for (size_t k = 1; k < n; ++k) {
    const Pose T_prev_cur =
        geometry::compose(geometry::inverse(odom_traj[k - 1].T), odom_traj[k].T);
    graph.addOdometry(static_cast<int>(k - 1), static_cast<int>(k), T_prev_cur,
                      sigmas6(0.002, 0.05));
  }
  if (use_gnss) {
    size_t g = 0;
    for (size_t k = 0; k < n; ++k) {
      while (g + 1 < gnss.size() && gnss[g + 1].t <= times[k]) ++g;
      for (size_t c = g; c < std::min(g + 2, gnss.size()); ++c)
        if (std::abs(gnss[c].t - times[k]) < 0.05) {
          graph.addGnss(static_cast<int>(k), gnss[c].p, gnss[c].sigma);
          break;
        }
    }
  }
  if (use_imu) {
    const estimation::ImuNoise noise{0.05, 0.005, 0.001, 0.0001};
    for (size_t k = 1; k < n; ++k) {
      const auto seg = imuBetween(imu, times[k - 1], times[k]);
      if (seg.size() >= 2) graph.addImu(static_cast<int>(k - 1), static_cast<int>(k), seg, noise);
    }
  }
  int loops = 0;
  if (use_loops) {
    loop::LoopDetector detector;
    for (size_t k = 0; k < n; ++k) {
      const auto cand = detector.queryAndAdd(static_cast<int>(k), keyframe_scans[k]);
      if (!cand) continue;
      Pose T_init = Pose::Identity();
      T_init.linear() =
          Eigen::AngleAxisd(cand->match.sector_shift * 2.0 * M_PI / 60.0, Vec3::UnitZ())
              .toRotationMatrix();
      const auto T_m_k =
          loop::verifyLoop(keyframe_scans[k], keyframe_scans[cand->match_id], T_init, 0.3);
      if (!T_m_k) continue;
      graph.addLoop(cand->match_id, static_cast<int>(k), T_imu_lidar * (*T_m_k) * T_lidar_imu,
                    sigmas6(0.01, 0.1), 1.0);
      ++loops;
    }
  }
  if (false_i >= 0 && false_j >= 0)
    graph.addLoop(false_i, false_j, Pose::Identity(), sigmas6(0.01, 0.1), 1.0);

  const auto optimized = graph.optimize();
  sensors::Trajectory opt_traj;
  for (const auto& [k, T] : optimized) opt_traj.push_back({times[static_cast<size_t>(k)], T});
  io::writeTum(out + "/optimized.tum", opt_traj);
  std::cerr << "frames " << n << ", factors " << graph.numFactors() << ", loops " << loops << '\n';
  return 0;
}
