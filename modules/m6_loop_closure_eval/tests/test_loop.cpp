// Module 6 acceptance tests: loop/scan_context.hpp
#include <gtest/gtest.h>

#include <cmath>
#include <random>

#include "slam/loop/scan_context.hpp"

using namespace slam;
using namespace slam::loop;

namespace {
// An asymmetric "place": buildings and poles at fixed positions around the origin.
PointCloud place(unsigned seed, double noise = 0.02) {
  std::mt19937 rng(seed);
  std::uniform_real_distribution<double> u(-40.0, 40.0), h(0.5, 12.0);
  std::normal_distribution<double> n(0.0, noise);
  PointCloud pts;
  for (int b = 0; b < 12; ++b) {
    const double cx = u(rng), cy = u(rng), height = h(rng);
    for (double dx = -2; dx <= 2; dx += 0.25)
      for (double z = -1.7; z <= height; z += 0.5)
        pts.emplace_back(cx + dx + n(rng), cy + n(rng), z + n(rng));
  }
  for (double x = -40; x <= 40; x += 0.5)
    for (double y = -40; y <= 40; y += 1.0) pts.emplace_back(x + n(rng), y + n(rng), -1.7 + n(rng));
  return pts;
}

PointCloud rotateZ(const PointCloud& in, double angle) {
  const Mat3 R = Eigen::AngleAxisd(angle, Vec3::UnitZ()).toRotationMatrix();
  PointCloud out;
  for (const auto& p : in) out.push_back(R * p);
  return out;
}
}  // namespace

TEST(M6ScanContext, DescriptorShape) {
  const ScanContextConfig cfg;
  const Descriptor d = makeScanContext(place(1), cfg);
  EXPECT_EQ(d.rows(), cfg.num_rings);
  EXPECT_EQ(d.cols(), cfg.num_sectors);
  EXPECT_GT(d.maxCoeff(), 0.0);
  EXPECT_GE(d.minCoeff(), 0.0);
}

TEST(M6ScanContext, SamePlaceIsCloseToZero) {
  const Descriptor a = makeScanContext(place(1, 0.02));
  const Descriptor b = makeScanContext(place(1, 0.03));
  EXPECT_LT(scanContextDistance(a, b).distance, 0.05);
}

TEST(M6ScanContext, RotationInvariantWithCorrectShift) {
  // Rotating the scan by +5 sectors (30 deg) shifts every column of b by +5 relative to a.
  const ScanContextConfig cfg;
  const PointCloud scan = place(2);
  const double sector = 2.0 * M_PI / cfg.num_sectors;
  const Descriptor a = makeScanContext(scan, cfg);
  const Descriptor b = makeScanContext(rotateZ(scan, 5 * sector + 0.5 * sector), cfg);
  const DescriptorMatch m = scanContextDistance(a, b);
  EXPECT_LT(m.distance, 0.15);
  EXPECT_TRUE(m.sector_shift == 5 || m.sector_shift == 6) << "shift " << m.sector_shift;
}

TEST(M6ScanContext, DifferentPlacesAreFar) {
  const Descriptor a = makeScanContext(place(1));
  const Descriptor same = makeScanContext(place(1, 0.03));
  const Descriptor other = makeScanContext(place(99));
  const double d_same = scanContextDistance(a, same).distance;
  const double d_other = scanContextDistance(a, other).distance;
  EXPECT_GT(d_other, 3.0 * d_same + 0.1);
}

TEST(M6ScanContext, LoopDetectorFindsRevisit) {
  LoopDetector detector({}, 0.2, 5);
  for (int k = 0; k < 10; ++k) EXPECT_FALSE(detector.queryAndAdd(k, place(100 + k)).has_value());
  const auto hit = detector.queryAndAdd(10, rotateZ(place(102, 0.03), 0.3));
  ASSERT_TRUE(hit.has_value());
  EXPECT_EQ(hit->match_id, 2);
}

TEST(M6Verify, AcceptsGoodLoopAndRejectsBadOne) {
  const PointCloud target = place(3);
  Pose offset = Pose::Identity();
  offset.translation() = Vec3(0.5, -0.3, 0.0);
  PointCloud source;
  for (const auto& p : place(3, 0.03)) source.push_back(offset.inverse() * p);
  const auto good = verifyLoop(source, target, Pose::Identity(), 0.2);
  ASSERT_TRUE(good.has_value());
  EXPECT_LT((good->translation() - offset.translation()).norm(), 0.05);
  EXPECT_FALSE(verifyLoop(place(4), target, Pose::Identity(), 0.2).has_value());
}
