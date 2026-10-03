# Phase gate A — Foundations (modules 0–1)

Closed-book, 45 minutes. Score yourself with `phase_A_answers.md`.

**PA-01.** Write `T_world_lidar` in terms of `T_world_imu` and `T_lidar_imu`.

**PA-02.** A point is (2, 0, 0) in the lidar frame. `T_world_lidar` is a 90° rotation about z plus a translation (10, 0, 0). Where is the point in the world frame?

**PA-03.** Which REP-105 frame should a GNSS-fused global pose be expressed in, and which frame is continuous but drifts?

**PA-04.** Give two quaternions that represent the identity rotation.

**PA-05.** You store quaternions in `xyzw` order but a library reads `wxyz`. Describe the symptom for a small rotation about z.

**PA-06.** What is so3Log of a rotation by exactly π about the x axis? Is the answer unique?

**PA-07.** Why must SLERP flip one quaternion when their dot product is negative?

**PA-08.** What is the size and structure of the Jacobian of `exp` at zero for SO(3)?

**PA-09.** Name the ellipsoid and the three Cartesian frames involved in turning a GNSS fix into a local map coordinate.

**PA-10.** You move 1° of longitude east at latitude 60°. Roughly how many kilometres is that?

**PA-11.** In git, how do you undo the last commit locally while keeping its changes in the working tree?

**PA-12.** Bridge: a multiple sequence alignment uses a reference coordinate system for positions. What plays that role in mapping, and what goes wrong if two people use different ones?
