#pragma once
// Exercise 1: fixed-capacity FIFO buffer, e.g. for the latest IMU samples.
// Header-only class template. Must work with move-only element types (e.g. std::unique_ptr).

#include <array>
#include <cstddef>
#include <optional>
#include <stdexcept>

#include "cppf/not_implemented.hpp"

namespace cppf {

template <class T, std::size_t N>
class RingBuffer {
  static_assert(N > 0, "capacity must be positive");

 public:
  static constexpr std::size_t capacity() noexcept { return N; }

  // Appends a value. When full, the oldest element is overwritten. Returns true if an element was
  // overwritten.
  bool push(T value) {
    // TODO(m0b): implement.
    (void)value;
    throw NotImplemented("RingBuffer::push");
  }

  // Removes and returns the oldest element, or std::nullopt when empty.
  std::optional<T> pop() {
    // TODO(m0b): implement.
    throw NotImplemented("RingBuffer::pop");
  }

  // i = 0 is the oldest element. Throws std::out_of_range when i >= size().
  const T& operator[](std::size_t i) const {
    // TODO(m0b): implement.
    (void)i;
    throw NotImplemented("RingBuffer::operator[]");
  }

  std::size_t size() const noexcept { return size_; }
  bool empty() const noexcept { return size_ == 0; }
  bool full() const noexcept { return size_ == N; }

  // Calls f(element) for every element, oldest first.
  template <class F>
  void forEach(F&& f) const {
    // TODO(m0b): implement.
    (void)f;
    throw NotImplemented("RingBuffer::forEach");
  }

 private:
  std::array<std::optional<T>, N> slots_{};
  std::size_t head_ = 0;  // index of the oldest element
  std::size_t size_ = 0;
};

}  // namespace cppf
