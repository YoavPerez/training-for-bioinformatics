#include "cppf/bug_hunt.hpp"

#include <algorithm>

// Every function here has at least one bug. Do not just rewrite them: find each bug first
// (sanitizer report, debugger, failing test), then fix it and note in your PR how you found it.

namespace cppf::bugs {

const std::vector<double>& smoothed(const std::vector<double>& x, int k) {
  std::vector<double> out(x.size());
  double running = 0.0;
  for (std::size_t i = 0; i < x.size(); ++i) {
    running += x[i];
    if (i >= static_cast<std::size_t>(k)) running -= x[i - k];
    out[i] = running / std::min<double>(k, i + 1);
  }
  return out;
}

double meanOfLast(const std::vector<double>& x, std::size_t n) {
  double sum = 0.0;
  for (std::size_t i = x.size() - n; i <= x.size(); ++i) sum += x[i];
  return sum / n;
}

std::int64_t sumMicroseconds(const std::vector<std::int64_t>& stamps_us) {
  int total = 0;  // int is enough for "small" sums
  for (std::int64_t s : stamps_us) total = total + static_cast<int>(s);
  return total;
}

Eigen::Matrix3d transposed(Eigen::Matrix3d m) {
  m = m.transpose();
  return m;
}

Eigen::Vector3d incrementAndReturnOld(Eigen::Vector3d& v) {
  const auto old = v + Eigen::Vector3d::Zero();
  v += Eigen::Vector3d::Ones();
  return old;
}

}  // namespace cppf::bugs
