# Module 6 — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M6-R01.** The maximum point height in that ring × sector cell of a polar grid around the sensor. See: scan_context_paper — Section III-A
**M6-R02.** By comparing descriptors under all column (sector) shifts and keeping the best. See: scan_context_paper — Section III-B
**M6-R03.** Appearance-based matches can be wrong (similar-looking places); one wrong loop can bend the map. See: stachniss_robust_ls — whole lecture
**M6-R04.** Cauchy/Geman-McClure: redescending influence, so very large residuals get almost no weight; Huber's influence stays constant. See: gtsam_robust_noise — whole post
**M6-R05.** ATE: global consistency; RPE: local drift over a fixed distance/time. See: evo_metrics_wiki — "evo_ape", "evo_rpe"
**M6-R06.** To remove the arbitrary choice of reference frame; do not align when the absolute frame is meaningful (e.g. GNSS-fused ENU). See: evo_metrics_wiki — "Alignment"
**M6-R07.** Average relative translation error in % over segments of 100–800 m. See: kitti_odometry — benchmark description
**M6-R08.** Run-to-run and pose-to-pose variability can exceed the difference; report distributions/CIs. See: evo_metrics_wiki — statistics output of evo_ape
**M6-R09.** Sequence alignment (e.g. Smith-Waterman-like local alignment); robustness where single places look alike. See: scan_context_paper — Section II "Related Work"
**M6-R10.** Free space as well as occupied space, as log-odds per voxel updated along each ray. Rays that later pass through the car's old place clear it. See: octomap_paper — "OctoMap Mapping Framework"
**M6-R11.** A truncated signed distance to the nearest surface plus a weight; new measurements are merged by a weighted running average. See: voxblox_paper — Section IV "TSDF Construction" (IV-A, IV-B)
**M6-R12.** Training: labelled matching and non-matching places (from known poses) and a loss such as triplets; it may not generalize to new places. See: pointnetvlad_paper — abstract

## Self-check 2 — Apply
**M6-A01.** A redescending kernel keeps ATE unchanged; Huber is pulled visibly. See: gtsam_robust_noise — whole post
**M6-A02.** Depends on your run; report accepted and rejected candidates. See: scan_context_paper — Section IV-B
**M6-A03.** Depends on your run; compare differences with the CIs. See: evo_repo — README (statistics)
**M6-A04.** If it helped, the sweep/time convention is at least approximately right. See: ct_icp_paper — Section V (per-point timestamps)
**M6-A05.** Depends on your run. See: kiss_icp_paper — Experimental Evaluation
