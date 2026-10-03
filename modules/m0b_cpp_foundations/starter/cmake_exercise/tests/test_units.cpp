// Plain test executable (no framework): returns non-zero on failure.
#include <cmath>
#include <iostream>

#include "units/units.hpp"

int main() {
  int failures = 0;
  auto check = [&](bool ok, const char* what) {
    if (!ok) {
      std::cerr << "FAILED: " << what << '\n';
      ++failures;
    }
  };
  check(std::abs(units::degToRad(180.0) - units::kPi) < 1e-12, "degToRad");
  check(std::abs(units::radToDeg(units::kPi / 2) - 90.0) < 1e-12, "radToDeg");
  Eigen::VectorXd v(2);
  v << 36.0, 72.0;
  check((units::kmhToMs(v) - Eigen::Vector2d(10.0, 20.0)).norm() < 1e-12, "kmhToMs");
  return failures == 0 ? 0 : 1;
}
