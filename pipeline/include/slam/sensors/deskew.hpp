#pragma once
// Module 3: LiDAR motion compensation (deskewing).

#include "slam/estimation/eskf.hpp"
#include "slam/types.hpp"

namespace slam::sensors {

struct TimedPose {
  double t = 0.0;
  Pose T = Pose::Identity();
};
using Trajectory = std::vector<TimedPose>;  // sorted by time

// Pose at time t by interpolating between the two neighbouring samples.
// Clamps to the first/last pose outside the trajectory's time range.
Pose poseAt(const Trajectory& traj, double t);

// Propagates the pose of the IMU over the given samples.
// Rotation is integrated from the gyro; translation assumes constant world velocity v_world.
// Returns T_world_imu at every sample time, starting with T_world_imu0 at imu.front().t.
Trajectory propagateImu(const std::vector<estimation::ImuSample>& imu, const Pose& T_world_imu0,
                        const Vec3& v_world);

// Re-expresses every point in the sensor frame at time t_ref.
// points[i] was measured in the sensor frame at point_times[i];
// traj gives T_world_sensor over (at least) the sweep.
PointCloud deskew(const PointCloud& points, const std::vector<double>& point_times,
                  const Trajectory& traj, double t_ref);

}  // namespace slam::sensors
