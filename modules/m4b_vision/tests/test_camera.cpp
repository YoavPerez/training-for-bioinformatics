// Module 4b acceptance tests: pinhole projection and LiDAR-to-image projection.
#include <gtest/gtest.h>

#include "slam/vision/camera.hpp"

using namespace slam;
using vision::PinholeCamera;
using vision::Vec2;

namespace {

PinholeCamera kittiLike() {
  PinholeCamera cam;
  cam.fx = 721.5377;
  cam.fy = 721.5377;
  cam.cx = 609.5593;
  cam.cy = 172.854;
  cam.width = 1242;
  cam.height = 375;
  return cam;
}

// LiDAR (x forward, y left, z up) -> camera (x right, y down, z forward), no offset.
Pose lidarToCameraAxes() {
  Pose T = Pose::Identity();
  T.linear() << 0, -1, 0,  //
      0, 0, -1,            //
      1, 0, 0;
  return T;
}

}  // namespace

TEST(Camera, PointOnOpticalAxisProjectsToPrincipalPoint) {
  const auto cam = kittiLike();
  const auto uv = vision::project(cam, Vec3(0, 0, 7));
  ASSERT_TRUE(uv.has_value());
  EXPECT_NEAR(uv->x(), cam.cx, 1e-9);
  EXPECT_NEAR(uv->y(), cam.cy, 1e-9);
}

TEST(Camera, KnownProjection) {
  const auto cam = kittiLike();
  const auto uv = vision::project(cam, Vec3(1.0, -0.5, 4.0));
  ASSERT_TRUE(uv.has_value());
  EXPECT_NEAR(uv->x(), cam.fx * 0.25 + cam.cx, 1e-9);
  EXPECT_NEAR(uv->y(), cam.fy * -0.125 + cam.cy, 1e-9);
}

TEST(Camera, PointsBehindOrTooCloseAreRejected) {
  const auto cam = kittiLike();
  EXPECT_FALSE(vision::project(cam, Vec3(0, 0, -5)).has_value());
  EXPECT_FALSE(vision::project(cam, Vec3(0, 0, 0)).has_value());
  EXPECT_FALSE(vision::project(cam, Vec3(0, 0, 0.05)).has_value());  // default min_depth 0.1 m
  EXPECT_TRUE(vision::project(cam, Vec3(0, 0, 0.05), 0.01).has_value());
}

TEST(Camera, PointsOutsideTheImageAreRejected) {
  const auto cam = kittiLike();
  EXPECT_FALSE(vision::project(cam, Vec3(10, 0, 1)).has_value());   // far right
  EXPECT_FALSE(vision::project(cam, Vec3(0, -10, 1)).has_value());  // far above
  // Exactly on the last valid pixel centre: inside. Half a pixel further: outside.
  const double z = 10.0;
  const Vec3 last((cam.width - 1 - cam.cx) * z / cam.fx, 0, z);
  EXPECT_TRUE(vision::project(cam, last).has_value());
  const Vec3 beyond((cam.width - 0.5 - cam.cx) * z / cam.fx + 1e-9, 0, z);
  EXPECT_FALSE(vision::project(cam, beyond).has_value());
}

TEST(Camera, UnprojectInvertsProject) {
  const auto cam = kittiLike();
  for (const double depth : {0.5, 3.0, 40.0}) {
    for (const Vec2 uv :
         {Vec2(0, 0), Vec2(cam.cx, cam.cy), Vec2(1200.3, 360.7), Vec2(17.25, 300.0)}) {
      const Vec3 p = vision::unproject(cam, uv, depth);
      EXPECT_NEAR(p.z(), depth, 1e-12);
      const auto back = vision::project(cam, p, 0.1);
      ASSERT_TRUE(back.has_value());
      EXPECT_LT((*back - uv).norm(), 1e-9);
    }
  }
}

TEST(Camera, ProjectCloudAppliesTheExtrinsicAndKeepsIndices) {
  const auto cam = kittiLike();
  Pose T_cam_lidar = lidarToCameraAxes();
  T_cam_lidar.translation() = Vec3(0.0, 0.08, 0.27);
  const PointCloud cloud = {
      Vec3(10, 0, 0.08),   // 0: ahead, at camera height -> principal point column
      Vec3(-10, 0, 0),     // 1: behind
      Vec3(10, 30, 0),     // 2: far left, outside the image
      Vec3(20, -2, -1.5),  // 3: ahead, right and below
  };
  const auto out = vision::projectCloud(cam, T_cam_lidar, cloud);
  ASSERT_EQ(out.size(), 2u);
  EXPECT_EQ(out[0].index, 0);
  EXPECT_EQ(out[1].index, 3);
  EXPECT_NEAR(out[0].depth, 10.27, 1e-9);
  EXPECT_NEAR(out[0].uv.x(), cam.cx, 1e-9);
  EXPECT_NEAR(out[0].uv.y(), cam.cy, 1e-9);
  const Vec3 p3 = T_cam_lidar * cloud[3];
  EXPECT_NEAR(out[1].depth, p3.z(), 1e-12);
  EXPECT_GT(out[1].uv.x(), cam.cx);  // right of centre
  EXPECT_GT(out[1].uv.y(), cam.cy);  // below centre
}

TEST(Camera, ProjectCloudOfEmptyCloudIsEmpty) {
  EXPECT_TRUE(vision::projectCloud(kittiLike(), Pose::Identity(), {}).empty());
}
