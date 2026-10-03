# Module 4 — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M4-R01.** SVD of the cross-covariance of the centred point sets (Kabsch/Umeyama). See: stachniss_icp_1 — whole lecture
**M4-R02.** Data association (nearest neighbours), then transform estimation; repeat. See: stachniss_icp_2 — whole lecture
**M4-R03.** r = nᵀ(p − q). See: stachniss_p2plane_5min — whole video
**M4-R04.** Motion along the surface does not change the residual: geometric degeneracy (unobservable direction). See: stachniss_icp_3 — whole lecture
**M4-R05.** Robustness to outliers/wrong matches vs the convergence basin (large initial errors). See: kiss_icp_paper — "Adaptive Threshold for Data Association"
**M4-R06.** It reweights each residual (IRLS): large residuals get smaller weights in JᵀWJ and JᵀWr. See: stachniss_icp_3 — robust kernels part
**M4-R07.** KD-tree: exact NN on a fixed cloud; voxel hash: cheap incremental updates of a growing local map. See: kiss_icp_paper — Step 3 "Local Map and Correspondence Estimation"
**M4-R08.** It interrupts the program at a fixed rate and records the call stack; hot code appears in many samples. See: gregg_perf — section 5 "Background"
**M4-R09.** Scoring function = the (robust) registration cost; alignment = the correspondences plus the rigid transform. See: stachniss_icp_2 — whole lecture

## Self-check 2 — Apply
**M4-A01.** Depends on your run; report distributions on the same pairs and downsampling. See: small_gicp — README "Benchmark"
**M4-A02.** Typically on the order of 1 m / a few degrees for consecutive KITTI pairs; limited by the correspondence distance and local minima. See: open3d_icp — "Point-to-plane ICP"
**M4-A03.** Often nearest-neighbour queries or normal estimation; give median and spread before/after. See: gregg_perf — section 8 "Visualizations"
**M4-A04.** Assert RᵀR ≈ I and det R ≈ 1 after many updates; re-orthonormalize (e.g. via a normalized quaternion). See: micro_lie — Section II-E (plus/minus on the manifold)
**M4-A05.** Typically degenerate or sparse geometry, or many dynamic objects. See: kiss_icp_paper — Experimental Evaluation
