// Module 0b bug hunt. Built with ASan + UBSan: a memory error or undefined behaviour aborts the
// test with a report that points at the faulty line. Wrong results fail as ordinary assertions.
#include <gtest/gtest.h>

#include "cppf/bug_hunt.hpp"

using namespace cppf::bugs;

TEST(M0bBugHunt, SmoothedMovingAverage) {
  const std::vector<double> x{1, 2, 3, 4, 5};
  const std::vector<double> s = smoothed(x, 2);
  ASSERT_EQ(s.size(), 5u);
  EXPECT_DOUBLE_EQ(s[0], 1.0);
  EXPECT_DOUBLE_EQ(s[1], 1.5);
  EXPECT_DOUBLE_EQ(s[4], 4.5);
}

TEST(M0bBugHunt, MeanOfLast) {
  const std::vector<double> x{1, 2, 3, 4};
  EXPECT_DOUBLE_EQ(meanOfLast(x, 2), 3.5);
  EXPECT_DOUBLE_EQ(meanOfLast(x, 4), 2.5);
}

TEST(M0bBugHunt, SumMicroseconds) {
  EXPECT_EQ(sumMicroseconds({2'000'000'000, 2'000'000'000, 5}), 4'000'000'005);
}

TEST(M0bBugHunt, Transposed) {
  Eigen::Matrix3d m;
  m << 1, 2, 3, 4, 5, 6, 7, 8, 9;
  const Eigen::Matrix3d expected = m.transpose().eval();
  EXPECT_TRUE(transposed(m).isApprox(expected));
}

TEST(M0bBugHunt, IncrementAndReturnOld) {
  Eigen::Vector3d v(1, 2, 3);
  const Eigen::Vector3d old = incrementAndReturnOld(v);
  EXPECT_TRUE(old.isApprox(Eigen::Vector3d(1, 2, 3)));
  EXPECT_TRUE(v.isApprox(Eigen::Vector3d(2, 3, 4)));
}
