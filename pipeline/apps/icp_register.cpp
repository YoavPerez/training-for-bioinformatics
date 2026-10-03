// Registers two KITTI velodyne scans with the module 4 ICP and prints the result as JSON.
// Usage: icp_register <source.bin> <target.bin> [voxel] [init: tx ty tz yaw_deg]
#include <chrono>
#include <cmath>
#include <iostream>

#include "slam/io/kitti.hpp"
#include "slam/registration/icp.hpp"
#include "slam/registration/normals.hpp"

using namespace slam;

int main(int argc, char** argv) {
  if (argc < 3) {
    std::cerr << "usage: icp_register <source.bin> <target.bin> [voxel] [tx ty tz yaw_deg]\n";
    return 2;
  }
  const double voxel = argc > 3 ? std::stod(argv[3]) : 0.5;
  Pose T_init = Pose::Identity();
  if (argc > 7) {
    T_init.translation() = Vec3(std::stod(argv[4]), std::stod(argv[5]), std::stod(argv[6]));
    T_init.linear() =
        Eigen::AngleAxisd(std::stod(argv[7]) * M_PI / 180.0, Vec3::UnitZ()).toRotationMatrix();
  }
  const auto source = registration::voxelDownsample(io::readVelodyneBin(argv[1]), voxel);
  const auto target = registration::voxelDownsample(io::readVelodyneBin(argv[2]), voxel);

  const auto t0 = std::chrono::steady_clock::now();
  const auto normals = registration::estimateNormals(target);
  const auto res = registration::icpPointToPlane(source, target, normals, T_init);
  const double ms =
      std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();

  const Eigen::Matrix4d M = res.T_target_source.matrix();
  std::cout << "{\"runtime_ms\": " << ms << ", \"iterations\": " << res.iterations
            << ", \"converged\": " << (res.converged ? "true" : "false")
            << ", \"rmse\": " << res.rmse << ", \"T_target_source\": [";
  for (int i = 0; i < 16; ++i) std::cout << M(i / 4, i % 4) << (i < 15 ? ", " : "");
  std::cout << "]}\n";
  return 0;
}
