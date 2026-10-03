#pragma once
// Exercise 2: time-ordered samples with linear interpolation, e.g. poses or IMU readings.
// T must support T + T and double * T (double, Eigen fixed-size vectors, ...).

#include <cstddef>
#include <optional>
#include <stdexcept>
#include <vector>

#include "cppf/not_implemented.hpp"

namespace cppf {

template <class T>
class TimedBuffer {
 public:
  // Times must be strictly increasing; otherwise throws std::invalid_argument and changes nothing.
  void insert(double t, T value) {
    // TODO(m0b): implement.
    (void)t;
    (void)value;
    throw NotImplemented("TimedBuffer::insert");
  }

  // Linear interpolation at t; std::nullopt outside [startTime(), endTime()] or when empty.
  // Must be O(log n): use a standard algorithm, not a linear scan.
  std::optional<T> at(double t) const {
    // TODO(m0b): implement.
    (void)t;
    throw NotImplemented("TimedBuffer::at");
  }

  // Removes samples older than t, but keeps the newest sample at or before t so that at(t) still
  // works.
  void dropBefore(double t) {
    // TODO(m0b): implement.
    (void)t;
    throw NotImplemented("TimedBuffer::dropBefore");
  }

  std::size_t size() const noexcept { return times_.size(); }
  // Both throw std::out_of_range when empty.
  double startTime() const {
    // TODO(m0b): implement.
    throw NotImplemented("TimedBuffer::startTime");
  }
  double endTime() const {
    // TODO(m0b): implement.
    throw NotImplemented("TimedBuffer::endTime");
  }

 private:
  std::vector<double> times_;
  std::vector<T> values_;
};

}  // namespace cppf
