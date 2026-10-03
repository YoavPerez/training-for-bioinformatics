#pragma once
// Module 6: LiDAR place recognition (Scan Context) and geometric verification.

#include <optional>

#include "slam/registration/icp.hpp"
#include "slam/types.hpp"

namespace slam::loop {

struct ScanContextConfig {
  int num_rings = 20;
  int num_sectors = 60;
  double max_range = 80.0;     // [m]
  double sensor_height = 2.0;  // [m] added to z so that ground points are positive
};

using Descriptor = Eigen::MatrixXd;  // num_rings x num_sectors

// Builds the descriptor of a scan expressed in the sensor frame.
Descriptor makeScanContext(const PointCloud& scan, const ScanContextConfig& config = {});

struct DescriptorMatch {
  double distance = 1.0;  // in [0, 1]; 0 = identical
  int sector_shift = 0;   // column shift of `b` that best aligns it with `a`
};
// Rotation-invariant distance between two descriptors.
DescriptorMatch scanContextDistance(const Descriptor& a, const Descriptor& b);

// Accepts a loop only if ICP converges with an RMSE below `max_rmse`.
// Returns T_target_source on success.
std::optional<Pose> verifyLoop(const PointCloud& source, const PointCloud& target,
                               const Pose& T_init, double max_rmse,
                               const registration::IcpConfig& config = {});

struct LoopCandidate {
  int match_id = -1;
  DescriptorMatch match;
};

// Provided: brute-force database of descriptors.
class LoopDetector {
 public:
  explicit LoopDetector(ScanContextConfig config = {}, double max_distance = 0.2,
                        int exclude_recent = 50)
      : config_(config), max_distance_(max_distance), exclude_recent_(exclude_recent) {}

  // Returns the best earlier match for `scan` (if below max_distance), then stores it under `id`.
  std::optional<LoopCandidate> queryAndAdd(int id, const PointCloud& scan);

 private:
  ScanContextConfig config_;
  double max_distance_;
  int exclude_recent_;
  std::vector<std::pair<int, Descriptor>> db_;
};

}  // namespace slam::loop
