#include "units/units.hpp"

namespace units {
double degToRad(double deg) { return deg * kPi / 180.0; }
double radToDeg(double rad) { return rad * 180.0 / kPi; }
Eigen::VectorXd kmhToMs(const Eigen::VectorXd& kmh) { return kmh / 3.6; }
}  // namespace units
