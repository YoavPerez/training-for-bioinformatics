# Module 4b — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M4B-R01.** u = fx·X/Z + cx, v = fy·Y/Z + cy. The depth: every point on the ray through the pixel gives the same (u, v). See: stachniss_pcv_camera — "Calibration Matrix"
**M4B-R02.** Tr_velo_to_cam (velodyne → camera 0), then R_rect_00 (rectifying rotation), then P_rect_00 (projection); y = P·R·Tr·x. See: kitti_ijrr — Section IV-C, eq. 7
**M4B-R03.** F: 7 (3×3, up to scale, rank 2). E: 5 (relative rotation 3 + translation direction 2); E has known intrinsics, F does not. See: stachniss_pcv_fundamental — "Which Parameters Can We Obtain and Which Not?"
**M4B-R04.** Pixel values ~1000 make the linear system ill-conditioned. Shift each point set to centroid 0 and scale to mean distance √2, then undo it on F. See: stachniss_pcv_fe_direct — "Conditioning/Normalization"
**M4B-R05.** The match lies on one line in image 2, the epipolar line l₂ = F x₁; the search becomes 1-D. See: stachniss_pcv_epipolar — "Epipoles and Epipolar Lines"
**M4B-R06.** Scaling the scene and the translation by the same factor gives identical images, so E (and t) is known only up to scale. See: vo_tutorial_part1 — "Motion Estimation"
**M4B-R07.** N = log(1 − 0.999) / log(1 − 0.5ˢ): about 218 for s = 5 and about 1765 for s = 8. See: stachniss_pcv_ransac — "How to Choose the Parameters?"
**M4B-R08.** Binary (oriented FAST + rotated BRIEF); Hamming distance; matches whose best distance is not clearly smaller than the second best (ambiguous). See: opencv_matcher — "Brute-Force Matching with SIFT Descriptors and Ratio Test"
**M4B-R09.** The sum of squared reprojection errors over all poses and points. Fix camera 1's pose and the scale (e.g. |t| = 1): the error does not change under them. See: stachniss_pcv_ba2 — "BA Without Control Points"
**M4B-R10.** Triangulate a point with each candidate; keep the one that puts the points in front of both cameras (cheirality). See: vo_tutorial_part1 — "Extracting R and t from E"

## Self-check 2 — Apply
**M4B-A01.** On the sample: about 19 000 of 121 000 points (~16 %). The camera sees only a ~80° wedge in front, and the scan covers 360°. See: kitti_ijrr — Section II "Sensor Setup"
**M4B-A02.** Without R_rect_00 (0.75°) points move by ~7 px: edges slightly off. Inverted extrinsic: points from the wrong part of the scan; no relation to the image. See: kitti_ijrr — Section IV-C, eq. 7
**M4B-A03.** On the sample ~0.12° rotation, ~2° direction. Direction is worse: a ~1 m baseline against points 5–30 m away gives little parallax. See: vo_tutorial_part1 — "Triangulation and Keyframe Selection"
**M4B-A04.** On the sample, step 8→9: repeated fence bars give consistent wrong matches, plus distant foliage with no parallax. RANSAC finds consistency, not truth. See: stachniss_pcv_ransac — "RANSAC Algorithm" (step 3: score by inliers)
**M4B-A05.** On the sample ICP is better: ~0.06° vs ~0.12° rotation, and a metric translation (~4 cm error); monocular VO gives only a direction. See: vo_tutorial_part1 — "VO Versus V-SLAM"
**M4B-A06.** Typical pair on the sample: RMS 0.39 → 0.30 px, rotation error 0.13° → 0.07°. Worst pair: almost no change; BA refines but cannot fix wrong matches. See: stachniss_pcv_ba — "Reprojection Error"
