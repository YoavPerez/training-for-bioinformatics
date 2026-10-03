// Smoke tests for provided (non-assignment) code. These pass on the starter code.
#include <gtest/gtest.h>

#include "slam/geometry/transform.hpp"
#include "slam/registration/kdtree.hpp"
#include "slam/registration/normals.hpp"

using namespace slam;

TEST(Smoke, SkewMatchesCrossProduct) {
  const Vec3 a(1, 2, 3), b(-4, 5, 0.5);
  EXPECT_TRUE(geometry::skew(a) * b == a.cross(b));
}

TEST(Smoke, KdTreeFindsNearest) {
  const PointCloud cloud{{0, 0, 0}, {1, 0, 0}, {0, 5, 0}};
  const registration::KdTree tree(cloud);
  EXPECT_EQ(tree.nearest({0.9, 0.1, 0}).first, 1u);
}

TEST(Smoke, VoxelDownsampleMergesPoints) {
  const PointCloud cloud{{0.1, 0.1, 0.1}, {0.2, 0.2, 0.2}, {5, 5, 5}};
  EXPECT_EQ(registration::voxelDownsample(cloud, 1.0).size(), 2u);
}

TEST(Smoke, NormalsOfPlaneAreVertical) {
  PointCloud plane;
  for (int i = 0; i < 10; ++i)
    for (int j = 0; j < 10; ++j) plane.emplace_back(i * 0.1, j * 0.1, 0.0);
  for (const auto& n : registration::estimateNormals(plane))
    EXPECT_NEAR(std::abs(n.z()), 1.0, 1e-9);
}
