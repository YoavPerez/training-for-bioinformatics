#include "slam/sensors/deskew.hpp"

#include "slam/geometry/transform.hpp"

namespace slam::sensors {

Pose poseAt(const Trajectory& traj, double t) {
  // TODO(m3): find the bracketing samples and interpolate (module 1 gives you the tool).
  (void)traj;
  (void)t;
  throw NotImplemented("sensors::poseAt");
}

Trajectory propagateImu(const std::vector<estimation::ImuSample>& imu, const Pose& T_world_imu0,
                        const Vec3& v_world) {
  // TODO(m3): integrate the gyro sample by sample.
  (void)imu;
  (void)T_world_imu0;
  (void)v_world;
  throw NotImplemented("sensors::propagateImu");
}

PointCloud deskew(const PointCloud& points, const std::vector<double>& point_times,
                  const Trajectory& traj, double t_ref) {
  // TODO(m3): move each point from the sensor frame at its own time to the frame at t_ref.
  (void)points;
  (void)point_times;
  (void)traj;
  (void)t_ref;
  throw NotImplemented("sensors::deskew");
}

}  // namespace slam::sensors
