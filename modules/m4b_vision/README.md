# Module 4b: Camera geometry and visual odometry
**Tentative effort:** ~1 week · **Phase:** C — Mapping core

## Goal
Add the camera to your toolbox: the pinhole model, LiDAR-to-image projection, two-view geometry (epipolar constraint, essential matrix, triangulation), feature matching with RANSAC, two-frame monocular visual odometry, a small bundle adjustment, and metric depth from a stereo pair. Know what a camera gives that a LiDAR does not (texture, cheap long-range bearing) and what it does not (metric scale from one camera).

---

## Segment 1 — Learn

### Learn from
- [Stachniss — Camera Parameters: Extrinsics and Intrinsics](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho1-20-camera-params.pptx.pdf) — slides — whole deck
- [Geiger et al. — Vision meets Robotics: The KITTI Dataset](https://www.cvlibs.net/publications/Geiger2013IJRR.pdf) — paper — Section II "Sensor Setup"; Section IV-B "Camera Calibration" and IV-C "Velodyne and IMU Calibration", eq. 3–7
- [Stachniss — Visual Features: Descriptors (SIFT, BRIEF, and ORB)](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho1-11-features-descriptors.pptx.pdf) — slides — the BRIEF and ORB parts
- [OpenCV tutorial — ORB](https://github.com/opencv/opencv/blob/4.x/doc/py_tutorials/py_feature2d/py_orb/py_orb.markdown) and [Feature Matching](https://github.com/opencv/opencv/blob/4.x/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.markdown) — docs — "ORB in OpenCV"; "Brute-Force Matching with ORB Descriptors" and "… with SIFT Descriptors and Ratio Test"
- [Stachniss — Relative Orientation, Fundamental and Essential Matrix](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-02-fundamentalmatrix.pptx.pdf) and [Epipolar Geometry](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-03-epipolar-geometry.pptx.pdf) — slides — whole decks
- [Stachniss — Direct Solutions for Computing Fundamental and Essential Matrix](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-04-fe-direct.pptx.pdf) — slides — "8-Point Algorithm", "Well-Conditioned Problem", "Conditioning/Normalization"
- [Stachniss — RANSAC](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-06-ransac.pptx.pdf) and [Triangulation and Absolute Orientation](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-07-triangulation.pptx.pdf) — slides — whole RANSAC deck; the triangulation part, incl. "Stereo Normal Case" and "Height/Depth Precision"
- [Stachniss — Bundle Adjustment, Part I](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-09-BA-part1.pptx.pdf) — slides — whole deck; [Part II](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-10-BA-part2.pptx.pdf) — slides "BA Without Control Points" and "Datum Without Control Points" (gauge)
- [Scaramuzza & Fraundorfer — Visual Odometry, Part I](https://rpg.ifi.uzh.ch/docs/VO_Part_I_Scaramuzza.pdf) — paper — "Formulation of the VO Problem", "Camera Modeling and Calibration", "Motion Estimation" (incl. "Extracting R and t from E", "Triangulation and Keyframe Selection"), "VO Versus V-SLAM"
- [OpenCV tutorial — Epipolar Geometry](https://github.com/opencv/opencv/blob/4.x/doc/py_tutorials/py_calib3d/py_epipolar_geometry/py_epipolar_geometry.markdown) — docs — "Basic Concepts" and "Code"

Optional:
- [Stachniss — Photogrammetry I & II course page](https://www.ipb.uni-bonn.de/photo12-2021/) — slides of every lecture, e.g. [Keypoints](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho1-10-features-keypoints.pptx.pdf), [P3P](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho1-23-p3p.pptx.pdf), [Bag of Visual Words](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-12-bag-of-visual-words.pptx.pdf)
- [ORB-SLAM](https://arxiv.org/abs/1502.00956) — paper — III "System Overview", IV "Automatic Map Initialization", VII "Loop Closing": how the pieces of this module become a full visual SLAM system
- Learned methods: [SuperPoint](https://arxiv.org/abs/1712.07629) (keypoints and descriptors), [LightGlue](https://arxiv.org/abs/2306.13643) (matching), [DROID-SLAM](https://arxiv.org/abs/2108.10869) (dense visual SLAM) — abstract and introduction of each

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before coding, then grade yourself.

## Segment 3 — Build

The sample drive includes the grayscale stereo pair (`image_00`, `image_01`, rectified). For a full drive, fetch them with `--camera` (see [`data/README.md`](../../data/README.md)). The camera calibration readers are provided: `io::readKittiCamera` (C++) and `kitti.Drive.camera()` (Python).

### Assignment
1. **Camera model (C++).** Implement `project`, `unproject` and `projectCloud` in [`pipeline/src/vision/camera.cpp`](../../pipeline/src/vision/camera.cpp) against `pipeline/include/slam/vision/camera.hpp`.
2. **LiDAR on the image.** Complete `overlay` in [`starter/lidar_on_image.py`](starter/lidar_on_image.py). It runs the provided `project_lidar` tool (your C++ code) and draws the scan on the image, coloured by depth. Make overlays for three frames, then one with a deliberately wrong calibration (e.g. leave out `R_rect_00`, or invert the extrinsic) and compare.
3. **Two-view geometry (numpy).** Implement `normalize_points`, `eight_point`, `essential_from_fundamental`, `triangulate_dlt` and `reprojection_errors` in [`pipeline/python/slampipe/vision.py`](../../pipeline/python/slampipe/vision.py). Do not call OpenCV there. Then compare your `eight_point` with `cv2.findFundamentalMat(..., cv2.FM_8POINT)` on real matches.
4. **Two-frame visual odometry.** Complete `match_features`, `relative_pose` and `main` in [`starter/mono_vo.py`](starter/mono_vo.py) (ORB, ratio test, essential matrix with RANSAC, `recoverPose`). Run it on the sample and on a full drive. Plot the per-step rotation and translation-direction errors against ground truth, and the trajectory (scaled with the ground-truth step length) against `gt.tum` with the [evo](https://github.com/MichaelGrupp/evo) command line (`evo_ape tum gt.tum vo.tum -a`).
5. **Bundle adjustment.** Complete `ba_residuals` and `refine` in [`starter/two_view_ba.py`](starter/two_view_ba.py). Run it on at least five frame pairs, including your worst VO step, and report the reprojection RMS and the pose errors before and after.
6. **Stereo (metric scale).** Complete `stereo_matches` and `stereo_depth` in [`starter/stereo_depth.py`](starter/stereo_depth.py): match camera 0 with camera 1 (the rectified pair, same row), triangulate with your `triangulate_dlt`, and compare each depth with the LiDAR at the same pixel (`lidar_depth_at` is provided). Plot the depth error against depth and explain its shape.

### C++ focus: a lean projection loop
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — docs — "Per: Performance", "F.call: Parameter passing"
- [cppreference: std::optional](https://en.cppreference.com/w/cpp/utility/optional) — docs

Task: `projectCloud` runs on every scan (about 120 000 points). It must not copy the input cloud, must allocate its output once (`reserve`), and must reuse `project` rather than duplicate its logic. In the PR, give the median runtime of `project_lidar` on 20 scans and say whether `std::optional` costs anything measurable here.

### Deliverables
- [ ] Camera model and `vision.py` merged through PR review
- [ ] LiDAR overlays (three frames + one wrong calibration), with one sentence each on what you see
- [ ] VO error plots and trajectory plot (sample + one full drive); your `eight_point` vs OpenCV on the same matches
- [ ] Bundle-adjustment table (≥ 5 pairs, incl. the worst VO step)
- [ ] Stereo-vs-LiDAR depth error plot (error against depth, ≥ 4 frames)

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m4b`): C++ `ctest --test-dir build -L '^m4b$'` and pytest.
- Every transform follows `T_<to>_<from>` naming (`T_cam_velo`, `T_cam2_cam1`, …), and camera axes are written down in `CONVENTIONS.md`.
- Error plots show distributions over steps, not a single number, and name the frames that fail.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) using your overlays, VO errors and BA table, and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open a PR (camera + `vision.py` first, scripts second) and request review.

## Where to look if stuck
- Which frame a KITTI point is in, and the order of `P_rect`, `R_rect` and `Tr_velo_to_cam`: KITTI IJRR, eq. 3–7, and the axes in Section II.
- Pixel centres and image bounds: the comment on `PinholeCamera::inImage` in `camera.hpp`.
- `eight_point` fits the noise-free test but fails with noise: Stachniss "Direct Solutions…", "Well-Conditioned Problem" and "Conditioning/Normalization".
- Which of the four (R, t) from E is right: VO tutorial, "Extracting R and t from E".
- `recoverPose` returns `T_cam2_cam1` (points of camera 1 expressed in camera 2): compare with your ground-truth convention before chaining.
- A pose with many inliers that is still wrong: draw the inlier matches on the image (`cv2.line`) and look at where they are.
- Stereo depth error that grows fast with distance: Stachniss "Triangulation and Absolute Orientation", slides "Stereo Normal Case" and "Height/Depth Precision"; the KITTI baseline is in IJRR Section II.
- Bundle adjustment that does not move or gets worse: check the gauge (camera 1 fixed, |t| fixed) and the initial guess; Stachniss "Bundle Adjustment, Part II", "BA Without Control Points".
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
