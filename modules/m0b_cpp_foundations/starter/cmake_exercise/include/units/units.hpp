#pragma once
// Small provided library for the CMake exercise. The code is correct; only the build is missing.
#include <Eigen/Core>

namespace units {
constexpr double kPi = 3.14159265358979323846;
double degToRad(double deg);
double radToDeg(double rad);
// Converts a vector of speeds from km/h to m/s.
Eigen::VectorXd kmhToMs(const Eigen::VectorXd& kmh);
}  // namespace units
