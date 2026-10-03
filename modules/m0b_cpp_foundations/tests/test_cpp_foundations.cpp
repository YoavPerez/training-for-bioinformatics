// Module 0b acceptance tests: ring buffer, timed buffer, RAII scan file, Eigen statistics.
#include <gtest/gtest.h>

#include <Eigen/Core>
#include <cmath>
#include <cstdio>
#include <filesystem>
#include <memory>
#include <string>
#include <type_traits>
#include <vector>

#include "cppf/ring_buffer.hpp"
#include "cppf/scan_file.hpp"
#include "cppf/stats.hpp"
#include "cppf/timed_buffer.hpp"

using namespace cppf;

// ---------------------------------------------------------------- RingBuffer
TEST(M0bRingBuffer, FifoOrderAndSize) {
  RingBuffer<int, 3> rb;
  EXPECT_TRUE(rb.empty());
  EXPECT_FALSE(rb.push(1));
  EXPECT_FALSE(rb.push(2));
  EXPECT_EQ(rb.size(), 2u);
  EXPECT_EQ(rb[0], 1);
  EXPECT_EQ(rb[1], 2);
  EXPECT_EQ(rb.pop(), 1);
  EXPECT_EQ(rb.pop(), 2);
  EXPECT_FALSE(rb.pop().has_value());
}

TEST(M0bRingBuffer, OverwritesOldestWhenFull) {
  RingBuffer<int, 3> rb;
  for (int i = 1; i <= 3; ++i) rb.push(i);
  EXPECT_TRUE(rb.full());
  EXPECT_TRUE(rb.push(4));  // overwrote 1
  std::vector<int> seen;
  rb.forEach([&](int v) { seen.push_back(v); });
  EXPECT_EQ(seen, (std::vector<int>{2, 3, 4}));
  EXPECT_EQ(rb.size(), 3u);
}

TEST(M0bRingBuffer, WrapsAroundManyTimes) {
  RingBuffer<int, 4> rb;
  for (int i = 0; i < 1000; ++i) rb.push(i);
  EXPECT_EQ(rb[0], 996);
  EXPECT_EQ(rb[3], 999);
  EXPECT_THROW(rb[4], std::out_of_range);
}

TEST(M0bRingBuffer, WorksWithMoveOnlyTypes) {
  static_assert(!std::is_copy_constructible_v<std::unique_ptr<int>>);
  RingBuffer<std::unique_ptr<int>, 2> rb;
  rb.push(std::make_unique<int>(7));
  rb.push(std::make_unique<int>(8));
  rb.push(std::make_unique<int>(9));  // drops 7
  auto first = rb.pop();
  ASSERT_TRUE(first.has_value());
  EXPECT_EQ(**first, 8);
  EXPECT_EQ(*rb[0], 9);
}

// ---------------------------------------------------------------- TimedBuffer
TEST(M0bTimedBuffer, InterpolatesScalars) {
  TimedBuffer<double> tb;
  tb.insert(0.0, 0.0);
  tb.insert(1.0, 10.0);
  tb.insert(3.0, 30.0);
  EXPECT_DOUBLE_EQ(*tb.at(0.5), 5.0);
  EXPECT_DOUBLE_EQ(*tb.at(2.0), 20.0);
  EXPECT_DOUBLE_EQ(*tb.at(3.0), 30.0);
  EXPECT_DOUBLE_EQ(*tb.at(0.0), 0.0);
  EXPECT_FALSE(tb.at(-0.1).has_value());
  EXPECT_FALSE(tb.at(3.1).has_value());
}

TEST(M0bTimedBuffer, InterpolatesEigenVectors) {
  TimedBuffer<Eigen::Vector3d> tb;
  tb.insert(10.0, Eigen::Vector3d(0, 0, 0));
  tb.insert(12.0, Eigen::Vector3d(2, 4, 6));
  EXPECT_TRUE(tb.at(11.0)->isApprox(Eigen::Vector3d(1, 2, 3)));
}

TEST(M0bTimedBuffer, RejectsNonIncreasingTimesWithoutChangingState) {
  TimedBuffer<double> tb;
  tb.insert(1.0, 1.0);
  EXPECT_THROW(tb.insert(1.0, 2.0), std::invalid_argument);
  EXPECT_THROW(tb.insert(0.5, 2.0), std::invalid_argument);
  EXPECT_EQ(tb.size(), 1u);
  EXPECT_DOUBLE_EQ(tb.endTime(), 1.0);
}

TEST(M0bTimedBuffer, EmptyBufferBehaviour) {
  TimedBuffer<double> tb;
  EXPECT_FALSE(tb.at(0.0).has_value());
  EXPECT_THROW(tb.startTime(), std::out_of_range);
  EXPECT_THROW(tb.endTime(), std::out_of_range);
}

TEST(M0bTimedBuffer, DropBeforeKeepsInterpolationValid) {
  TimedBuffer<double> tb;
  for (int i = 0; i < 10; ++i) tb.insert(i, i * 2.0);
  tb.dropBefore(4.5);
  EXPECT_DOUBLE_EQ(tb.startTime(), 4.0);
  EXPECT_DOUBLE_EQ(*tb.at(4.5), 9.0);
  EXPECT_EQ(tb.size(), 6u);
  tb.dropBefore(-1.0);
  EXPECT_EQ(tb.size(), 6u);
}

TEST(M0bTimedBuffer, LargeBufferIsFast) {
  TimedBuffer<double> tb;
  for (int i = 0; i < 1000000; ++i) tb.insert(i * 0.01, i);
  double sum = 0.0;
  for (int q = 0; q < 1000000; ++q) sum += *tb.at(q * 0.009 + 0.0005);
  EXPECT_GT(sum, 0.0);  // finishes quickly only with a logarithmic search (ctest TIMEOUT 30 s)
}

// ---------------------------------------------------------------- ScanFile
namespace {
std::string writeScan(const std::vector<PointXYZI>& pts) {
  const auto path =
      std::filesystem::temp_directory_path() / ("m0b_scan_" + std::to_string(pts.size()) + ".bin");
  std::FILE* f = std::fopen(path.string().c_str(), "wb");
  std::fwrite(pts.data(), sizeof(PointXYZI), pts.size(), f);
  std::fclose(f);
  return path.string();
}
}  // namespace

TEST(M0bScanFile, ReadsPoints) {
  const std::vector<PointXYZI> pts{{1, 2, 3, 0.5f}, {4, 5, 6, 0.25f}, {-1, 0, 1, 1.0f}};
  ScanFile scan(writeScan(pts));
  EXPECT_TRUE(scan.isOpen());
  EXPECT_EQ(scan.numPoints(), 3u);
  const auto read = scan.readAll();
  ASSERT_EQ(read.size(), 3u);
  EXPECT_FLOAT_EQ(read[1].y, 5.0f);
  EXPECT_FLOAT_EQ(read[2].intensity, 1.0f);
  EXPECT_EQ(scan.readAll().size(), 3u) << "readAll must start from the beginning every time";
}

TEST(M0bScanFile, MissingFileThrowsAndLeaksNothing) {
  const int before = ScanFile::openCount();
  try {
    ScanFile scan("/definitely/not/here.bin");
    FAIL() << "expected an exception";
  } catch (const std::runtime_error& e) {
    EXPECT_NE(std::string(e.what()).find("not/here.bin"), std::string::npos);
  }
  EXPECT_EQ(ScanFile::openCount(), before);
}

TEST(M0bScanFile, MoveOnlyAndNoLeaks) {
  static_assert(!std::is_copy_constructible_v<ScanFile>, "ScanFile must not be copyable");
  static_assert(!std::is_copy_assignable_v<ScanFile>, "ScanFile must not be copy-assignable");
  static_assert(std::is_nothrow_move_constructible_v<ScanFile>, "moves must be noexcept");
  static_assert(std::is_nothrow_move_assignable_v<ScanFile>, "moves must be noexcept");
  const std::string path = writeScan({{0, 0, 0, 0}, {1, 1, 1, 1}});
  const int before = ScanFile::openCount();
  {
    ScanFile a(path);
    EXPECT_EQ(ScanFile::openCount(), before + 1);
    ScanFile b(std::move(a));
    EXPECT_FALSE(a.isOpen());  // NOLINT(bugprone-use-after-move): checking the moved-from state
    EXPECT_TRUE(b.isOpen());
    EXPECT_EQ(ScanFile::openCount(), before + 1);
    ScanFile c(path);
    c = std::move(b);  // c's own file must be closed, not leaked
    EXPECT_EQ(ScanFile::openCount(), before + 1);
    std::vector<ScanFile> files;
    for (int i = 0; i < 10; ++i) files.emplace_back(path);  // reallocation moves elements
    EXPECT_EQ(ScanFile::openCount(), before + 11);
  }
  EXPECT_EQ(ScanFile::openCount(), before);
}

// ---------------------------------------------------------------- Eigen statistics
TEST(M0bStats, CentroidAndCovarianceOfKnownSet) {
  Eigen::Matrix3Xd pts(3, 4);
  pts << 1, -1, 1, -1,  //
      2, 2, -2, -2,     //
      0, 0, 0, 0;
  EXPECT_TRUE(centroid(pts).isApprox(Eigen::Vector3d::Zero()) || centroid(pts).norm() < 1e-12);
  const Eigen::Matrix3d C = covariance(pts);
  EXPECT_NEAR(C(0, 0), 4.0 / 3.0, 1e-12);
  EXPECT_NEAR(C(1, 1), 16.0 / 3.0, 1e-12);
  EXPECT_NEAR(C(0, 1), 0.0, 1e-12);
  EXPECT_THROW(covariance(pts.leftCols(1)), std::invalid_argument);
}

TEST(M0bStats, AcceptsBlocksAndMapsWithoutCopies) {
  Eigen::Matrix3Xd big = Eigen::Matrix3Xd::Random(3, 100);
  EXPECT_TRUE(centroid(big.middleCols(10, 20)).isApprox(big.middleCols(10, 20).rowwise().mean()));
  std::vector<double> raw{1, 1, 1, 3, 3, 3};
  const Eigen::Map<const Eigen::Matrix3Xd> mapped(raw.data(), 3, 2);
  EXPECT_TRUE(centroid(mapped).isApprox(Eigen::Vector3d(2, 2, 2)));
}

TEST(M0bStats, TransformInPlaceWritesThroughToTheCaller) {
  std::vector<double> raw{1, 0, 0, 0, 1, 0};
  Eigen::Map<Eigen::Matrix3Xd> mapped(raw.data(), 3, 2);
  Eigen::Isometry3d T = Eigen::Isometry3d::Identity();
  T.linear() = Eigen::AngleAxisd(M_PI / 2, Eigen::Vector3d::UnitZ()).toRotationMatrix();
  T.translation() = Eigen::Vector3d(10, 0, 0);
  transformInPlace(T, mapped);
  EXPECT_NEAR(raw[0], 10.0, 1e-12);  // (1,0,0) -> (10,1,0)
  EXPECT_NEAR(raw[1], 1.0, 1e-12);
  EXPECT_NEAR(raw[3], 9.0, 1e-12);  // (0,1,0) -> (9,0,0)
}
