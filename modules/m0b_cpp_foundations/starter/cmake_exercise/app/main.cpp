#include <iostream>

#include "units/units.hpp"

int main() {
  std::cout << "90 deg = " << units::degToRad(90.0) << " rad\n";
  return 0;
}
