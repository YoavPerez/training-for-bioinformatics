#include "slam/loop/scan_context.hpp"

#include "slam/registration/normals.hpp"

namespace slam::loop {

Descriptor makeScanContext(const PointCloud& scan, const ScanContextConfig& config) {
  // TODO(m6): polar binning of the scan; see the Scan Context paper for what each bin stores.
  (void)scan;
  (void)config;
  throw NotImplemented("loop::makeScanContext");
}

DescriptorMatch scanContextDistance(const Descriptor& a, const Descriptor& b) {
  // TODO(m6): column-wise distance, minimized over all sector shifts.
  (void)a;
  (void)b;
  throw NotImplemented("loop::scanContextDistance");
}

std::optional<Pose> verifyLoop(const PointCloud& source, const PointCloud& target,
                               const Pose& T_init, double max_rmse,
                               const registration::IcpConfig& config) {
  // TODO(m6): reuse your module 4 ICP.
  (void)source;
  (void)target;
  (void)T_init;
  (void)max_rmse;
  (void)config;
  throw NotImplemented("loop::verifyLoop");
}

std::optional<LoopCandidate> LoopDetector::queryAndAdd(int id, const PointCloud& scan) {
  Descriptor d = makeScanContext(scan, config_);
  std::optional<LoopCandidate> best;
  for (const auto& [other_id, other] : db_) {
    if (id - other_id < exclude_recent_) continue;
    const DescriptorMatch m = scanContextDistance(d, other);
    if (m.distance < max_distance_ && (!best || m.distance < best->match.distance))
      best = LoopCandidate{other_id, m};
  }
  db_.emplace_back(id, std::move(d));
  return best;
}

}  // namespace slam::loop
