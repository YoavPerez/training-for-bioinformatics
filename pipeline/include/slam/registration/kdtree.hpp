#pragma once
// Provided: thin KD-tree wrapper over nanoflann (https://github.com/jlblancoc/nanoflann).

#include <limits>
#include <memory>
#include <nanoflann.hpp>

#include "slam/types.hpp"

namespace slam::registration {

class KdTree {
 public:
  explicit KdTree(const PointCloud& cloud)
      : adaptor_{&cloud},
        index_(
            std::make_unique<Index>(3, adaptor_, nanoflann::KDTreeSingleIndexAdaptorParams(10))) {}

  // Index and squared distance of the nearest neighbour of q.
  // Returns a squared distance of +infinity if the cloud is empty or q is not finite.
  std::pair<size_t, double> nearest(const Vec3& q) const {
    size_t idx = 0;
    double d2 = std::numeric_limits<double>::infinity();
    if (adaptor_.cloud->empty() || !q.allFinite() || index_->knnSearch(q.data(), 1, &idx, &d2) == 0)
      return {0, std::numeric_limits<double>::infinity()};
    return {idx, d2};
  }

  // Indices of the k nearest neighbours of q.
  std::vector<size_t> knn(const Vec3& q, size_t k) const {
    std::vector<size_t> idx(k);
    std::vector<double> d2(k);
    if (adaptor_.cloud->empty() || !q.allFinite()) return {};
    const size_t n = index_->knnSearch(q.data(), k, idx.data(), d2.data());
    idx.resize(n);
    return idx;
  }

 private:
  struct Adaptor {
    const PointCloud* cloud;
    size_t kdtree_get_point_count() const { return cloud->size(); }
    double kdtree_get_pt(size_t i, size_t dim) const { return (*cloud)[i][static_cast<int>(dim)]; }
    template <class BBox>
    bool kdtree_get_bbox(BBox&) const {
      return false;
    }
  };
  using Index = nanoflann::KDTreeSingleIndexAdaptor<nanoflann::L2_Simple_Adaptor<double, Adaptor>,
                                                    Adaptor, 3, size_t>;
  Adaptor adaptor_;
  std::unique_ptr<Index> index_;
};

}  // namespace slam::registration
