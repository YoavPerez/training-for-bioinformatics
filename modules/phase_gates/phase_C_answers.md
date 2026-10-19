# Phase gate C — answers

**PC-01.** ∂r/∂w = (p × n)ᵀ for r = nᵀ(p − q) with p ← Exp(w)p. See: stachniss_icp_3 — whole lecture
**PC-02.** It lets points slide along surfaces, so it does not have to "walk" sampled points into exact correspondence. See: stachniss_p2plane_5min — whole video
**PC-03.** Degenerate geometry: motion along the tunnel axis leaves residuals unchanged. See: stachniss_icp_3 — whole lecture
**PC-04.** Round-off accumulates, and inverses that assume orthonormality amplify it; re-project R onto SO(3). See: micro_lie — Section II-E
**PC-05.** Chained odometry (dead reckoning); from the front-end's relative poses. See: gtsam_intro — Section 4 "PoseSLAM"
**PC-06.** The global position and orientation (gauge), unless GNSS fixes the position. See: gtsam_intro — Section 4 "PoseSLAM"
**PC-07.** The optimizer weighs evidence by the noise; overconfident odometry ignores GNSS/loops, underconfident odometry follows noise. See: dellaert_kaess — Ch. 2
**PC-08.** Verify geometrically (ICP fitness/RMSE, overlap), check consistency with odometry, use a robust kernel. See: scan_context_paper — Section III-C
**PC-09.** Cauchy's influence function goes back down for large residuals; Huber's stays constant. See: gtsam_robust_noise — whole post
**PC-10.** RPE at a fixed distance: it measures local drift independent of sequence length. See: evo_metrics_wiki — "evo_rpe"
**PC-11.** As "no significant difference on these sequences", with the CIs; do not claim an improvement. See: evo_metrics_wiki — "evo_ape" statistics
**PC-12.** Like aligning reads rather than single k-mers: context across many positions disambiguates repetitive (look-alike) places. See: scan_context_paper — Section II "Related Work"
**PC-13.** A rotation error shifts near and far points by the same number of pixels; a translation error shifts near points much more (∝ 1/depth). See: kitti_ijrr — Section IV-C, eq. 7
**PC-14.** Points triangulated in earlier frames, re-observed in the new one (3-D-to-2-D), tie the scales together. A LiDAR gives metric depth, an IMU metric acceleration. See: vo_tutorial_part1 — "Motion Estimation"
