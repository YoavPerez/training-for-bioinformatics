# Changelog

## v1.0 — first cohort

**Program:** modules 0, 0b, 1, 2, 3, 4, 4b, 5, 6, 7, 8 (about 12–14 weeks including the mini-project; modules 1 and 5 re-estimated) in four phases with phase-gate self-checks,
then an optional applied project. One LiDAR–inertial–GNSS mapping pipeline in `pipeline/` grows module by module.

**Audience:** recent bioinformatics graduates. `GLOSSARY.md` opens with a "Coming from bioinformatics" table, and
each phase gate includes a bridge question.

**What each module contains:** linked free resources with precise pointers, self-check quizzes with answers and
pointers, starter code with TODOs, tests that fail until the module is done, a checklist, and a C++ focus task
(modules 1–7 and 4b).

**Data:** KITTI raw (CC BY-NC-SA 3.0, training and research only). `python data/download.py --sample` fetches the CI
sample (drive 2011_09_26_0002: LiDAR, OXTS, grayscale stereo pair); full drives with `--drive`, plus `--camera`
for images and `--extract-oxts` for 100 Hz OXTS. Module 3 can use a 16 h static IMU recording (MILUV, CC BY 4.0).

**Environment:** dev image `infra/docker/Dockerfile` (Ubuntu 24.04, GTSAM 4.3.0, Argo CLI 4.1.4, pinned Python
packages incl. OpenCV 4.12), VS Code dev container, GitHub Actions CI (lint, smoke, one job per module).

**Known limitations**
- KITTI is from 2011 (Velodyne HDL-64, OXTS RT3003); the GNSS in modules 5–6 is simulated from the OXTS solution.
- Not covered yet: localization in a prior map, extrinsic calibration, raw GNSS processing, tightly coupled
  LiDAR–inertial odometry, ROS (a separate team module is planned).
- The dev image needs about 10 GB; plan for about 60 GB more for datasets.

**Still in review ahead of the cohort:** modules 2 onwards are re-reviewed on a rolling schedule, one module ahead of
the first cohort. Fixes arrive as normal commits; pull from the template if your mentor asks you to.
