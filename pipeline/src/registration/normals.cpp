#include "slam/registration/normals.hpp"

#include <Eigen/Eigenvalues>
#include <cmath>
#include <unordered_map>

#include "slam/registration/kdtree.hpp"

namespace slam::registration {

namespace {
struct VoxelKey {
  int64_t x, y, z;
  bool operator==(const VoxelKey& o) const { return x == o.x && y == o.y && z == o.z; }
};
struct VoxelHash {
  size_t operator()(const VoxelKey& k) const {
    return static_cast<size_t>(k.x * 73856093) ^ static_cast<size_t>(k.y * 19349669) ^
           static_cast<size_t>(k.z * 83492791);
  }
};
}  // namespace

PointCloud voxelDownsample(const PointCloud& cloud, double voxel_size) {
  std::unordered_map<VoxelKey, std::pair<Vec3, int>, VoxelHash> grid;
  for (const auto& p : cloud) {
    const VoxelKey key{static_cast<int64_t>(std::floor(p.x() / voxel_size)),
                       static_cast<int64_t>(std::floor(p.y() / voxel_size)),
                       static_cast<int64_t>(std::floor(p.z() / voxel_size))};
    auto& cell = grid[key];
    if (cell.second == 0) cell.first.setZero();
    cell.first += p;
    cell.second += 1;
  }
  PointCloud out;
  out.reserve(grid.size());
  for (const auto& [key, cell] : grid) out.push_back(cell.first / cell.second);
  return out;
}

std::vector<Vec3> estimateNormals(const PointCloud& cloud, size_t k) {
  const KdTree tree(cloud);
  std::vector<Vec3> normals(cloud.size(), Vec3::UnitZ());
  for (size_t i = 0; i < cloud.size(); ++i) {
    const auto nn = tree.knn(cloud[i], k);
    if (nn.size() < 3) continue;
    Vec3 mean = Vec3::Zero();
    for (size_t j : nn) mean += cloud[j];
    mean /= static_cast<double>(nn.size());
    Mat3 C = Mat3::Zero();
    for (size_t j : nn) C += (cloud[j] - mean) * (cloud[j] - mean).transpose();
    Eigen::SelfAdjointEigenSolver<Mat3> es(C);
    normals[i] = es.eigenvectors().col(0).normalized();
  }
  return normals;
}

}  // namespace slam::registration
