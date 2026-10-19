// Projects one KITTI velodyne scan into a rectified camera image with the module 4b camera model.
// Usage: project_lidar <drive_dir> <frame> <out.csv> [camera index, default 0]
// Writes "u,v,depth,index" for every point that lands in the image.
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>

#include "slam/io/kitti.hpp"
#include "slam/vision/camera.hpp"

using namespace slam;

int main(int argc, char** argv) {
  if (argc < 4) {
    std::cerr << "usage: project_lidar <drive_dir> <frame> <out.csv> [camera index]\n";
    return 2;
  }
  const std::filesystem::path drive(argv[1]);
  const int frame = std::stoi(argv[2]);
  const int index = argc > 4 ? std::stoi(argv[4]) : 0;

  std::ostringstream name;
  name << std::setw(10) << std::setfill('0') << frame << ".bin";
  const auto cloud =
      io::readVelodyneBin((drive / "velodyne_points" / "data" / name.str()).string());
  const auto calib = io::readKittiCamera(drive.parent_path().string(), index);
  const auto projected = vision::projectCloud(calib.cam, calib.T_cam_velo, cloud);

  std::ofstream out(argv[3]);
  if (!out) {
    std::cerr << "cannot write " << argv[3] << "\n";
    return 1;
  }
  out << "u,v,depth,index\n" << std::fixed << std::setprecision(4);
  for (const auto& p : projected)
    out << p.uv.x() << ',' << p.uv.y() << ',' << p.depth << ',' << p.index << '\n';
  std::cerr << projected.size() << " of " << cloud.size() << " points in the image\n";
  return 0;
}
