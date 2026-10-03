#pragma once
#include <stdexcept>
#include <string>

namespace cppf {
// Thrown by starter code that is not implemented yet.
struct NotImplemented : std::logic_error {
  explicit NotImplemented(const std::string& what) : std::logic_error("TODO: " + what) {}
};
}  // namespace cppf
