# Module 4b — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M4B-R01.** Write the pixel (u, v) of a point (X, Y, Z) given in the camera frame, using fx, fy, cx, cy. What information about the point does the pixel not contain?

**M4B-R02.** In KITTI, which three matrices take a homogeneous velodyne point to a pixel of the rectified camera 0 image, and in which order are they applied?

**M4B-R03.** How many degrees of freedom do the fundamental matrix and the essential matrix have? Why the difference?

**M4B-R04.** Why must pixel coordinates be normalized before the linear eight-point algorithm, and to what?

**M4B-R05.** Given a point in image 1 and the fundamental matrix, what does the epipolar constraint tell you about where its match can be in image 2?

**M4B-R06.** Why can a single moving camera recover the direction of its translation between two frames but not its length?

**M4B-R07.** With 50 % outliers, how many RANSAC iterations give a 99.9 % chance of at least one all-inlier sample, for 5-point samples and for 8-point samples?

**M4B-R08.** What kind of descriptor is ORB, which distance compares two ORB descriptors, and what does Lowe's ratio test reject?

**M4B-R09.** What does bundle adjustment minimize? For two views from one camera, which quantities must be fixed (the gauge), and why?

**M4B-R10.** Decomposing an essential matrix gives four (R, t) candidates. How is the right one chosen?

**M4B-R11.** A stereo rig has f = 720 px and a baseline of 0.54 m. A disparity error of 0.5 px: roughly what depth error does it cause at 10 m and at 40 m?

## Self-check 2 — Apply

**M4B-A01.** How many points of your frame-0 scan land in the image, out of how many? Why is the fraction small?

**M4B-A02.** In your wrong-calibration overlay, what changed when you left out `R_rect_00`, and what when you inverted the extrinsic?

**M4B-A03.** What are your median rotation error and median translation-direction error per step? Which is relatively worse, and why?

**M4B-A04.** Look at your worst VO step. It may have many inliers and a low reprojection error and still be wrong. What did you see in the inlier matches, and why does RANSAC accept them?

**M4B-A05.** Compare your two-frame VO with your module 4 ICP on the same consecutive frames. Which gives the better rotation, which the better translation, and why?

**M4B-A06.** How much did bundle adjustment change the reprojection RMS and the pose errors on a typical pair, and on your worst pair? Why the difference?

**M4B-A07.** What median relative error did your stereo depth have against the LiDAR, and how did the absolute error change between 10 m and 40 m?

## Explain to your mentor
- Walk through eq. 7 of the KITTI paper on your overlay: point out a depth edge that lines up with an object edge, and say what each matrix does.
- A robot already has a calibrated LiDAR and IMU. Give two concrete things a camera would add, and one thing it cannot give without another sensor.
