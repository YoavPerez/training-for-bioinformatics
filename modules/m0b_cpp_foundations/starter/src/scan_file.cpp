#include "cppf/scan_file.hpp"

#include <atomic>
#include <stdexcept>

#include "cppf/not_implemented.hpp"

namespace cppf {

namespace {
std::atomic<int> g_open_files{0};
}

namespace detail {
std::FILE* openCounted(const std::string& path) {
  std::FILE* f = std::fopen(path.c_str(), "rb");
  if (f != nullptr) ++g_open_files;
  return f;
}

void CountedFileCloser::operator()(std::FILE* f) const noexcept {
  if (f != nullptr) {
    std::fclose(f);
    --g_open_files;
  }
}
}  // namespace detail

int ScanFile::openCount() noexcept { return g_open_files.load(); }

ScanFile::ScanFile(const std::string& path) : path_(path) {
  // TODO(m0b): open the file with detail::openCounted and take ownership; throw if it fails.
  throw NotImplemented("ScanFile::ScanFile");
}

bool ScanFile::isOpen() const noexcept {
  // TODO(m0b): implement.
  return false;
}

std::size_t ScanFile::numPoints() const {
  // TODO(m0b): implement (hint: fseek/ftell, or std::filesystem::file_size on path_).
  throw NotImplemented("ScanFile::numPoints");
}

std::vector<PointXYZI> ScanFile::readAll() {
  // TODO(m0b): implement.
  throw NotImplemented("ScanFile::readAll");
}

}  // namespace cppf
