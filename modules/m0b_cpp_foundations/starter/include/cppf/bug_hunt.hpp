#pragma once
// Exercise 5: bug hunt. Every function in bug_hunt.cpp has at least one bug. The tests in
// tests/test_bug_hunt.cpp are built with AddressSanitizer and UndefinedBehaviorSanitizer.
// Find each bug with the sanitizers, the debugger or the tests, fix it, and write down in your PR
// how you found it. You may change signatures in this header if the bug is in the signature.

#include <Eigen/Core>
#include <cstdint>
#include <vector>

namespace cppf::bugs {

// Moving average of x with window k (k >= 1); output has the same length as x, and element i
// averages x[max(0, i-k+1) .. i].
const std::vector<double>& smoothed(const std::vector<double>& x, int k);

// Mean of the last n elements of x (n <= x.size(), n >= 1).
double meanOfLast(const std::vector<double>& x, std::size_t n);

// Sum of timestamps given in microseconds since the epoch.
std::int64_t sumMicroseconds(const std::vector<std::int64_t>& stamps_us);

// Returns the transpose of m.
Eigen::Matrix3d transposed(Eigen::Matrix3d m);

// Adds one to every coefficient of v and returns the value v had before the call.
Eigen::Vector3d incrementAndReturnOld(Eigen::Vector3d& v);

}  // namespace cppf::bugs
