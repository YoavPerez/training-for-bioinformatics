#pragma once
// Exercise 3: RAII owner of an open KITTI velodyne .bin file (x, y, z, reflectance as float32).

#include <cstdio>
#include <memory>
#include <string>
#include <vector>

namespace cppf {

struct PointXYZI {
  float x, y, z, intensity;
};

namespace detail {
// Provided. Opens a file for binary reading and counts it as open; returns nullptr on failure.
std::FILE* openCounted(const std::string& path);
// Provided. Deleter that closes the file and updates the open-file counter.
struct CountedFileCloser {
  void operator()(std::FILE* f) const noexcept;
};
}  // namespace detail

class ScanFile {
 public:
  // Opens the file; throws std::runtime_error (message containing the path) if it cannot be opened.
  explicit ScanFile(const std::string& path);

  // TODO(m0b): decide which special member functions this class needs, and declare only those.
  // The class must be movable, must not be copyable, and must never leak a file handle.

  bool isOpen() const noexcept;
  // Number of points (file size / 16 bytes). Throws std::logic_error if the file is not open.
  std::size_t numPoints() const;
  // Reads every point from the start of the file. Throws std::logic_error if not open.
  std::vector<PointXYZI> readAll();

  // Provided: number of files currently open through ScanFile (for leak tests).
  static int openCount() noexcept;

 private:
  std::unique_ptr<std::FILE, detail::CountedFileCloser> file_;
  std::string path_;
};

}  // namespace cppf
