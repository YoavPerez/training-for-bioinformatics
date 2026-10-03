#pragma once
// Provided: point cloud preprocessing used by registration.

#include "slam/types.hpp"

namespace slam::registration {

// Keeps one point (the centroid) per occupied voxel of edge length `voxel_size`.
PointCloud voxelDownsample(const PointCloud& cloud, double voxel_size);

// Unit normals from PCA over the k nearest neighbours. Orientation is arbitrary.
std::vector<Vec3> estimateNormals(const PointCloud& cloud, size_t k = 10);

}  // namespace slam::registration
