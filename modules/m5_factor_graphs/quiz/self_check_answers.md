# Module 5 — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M5-R01.** Variables and factors; a factor is a (probabilistic) constraint on the variables it connects. See: gtsam_intro — Section 1 "Factor Graphs"
**M5-R02.** Front-end turns sensor data into constraints (odometry, loops); back-end optimizes them. See: dellaert_kaess — Ch. 1
**M5-R03.** Without it the problem is invariant to a global transform (gauge freedom), so the system is singular. See: gtsam_intro — Section 4 "PoseSLAM"
**M5-R04.** Avoids re-integrating raw IMU samples whenever the linearization point changes. See: forster_preintegration — Section VI
**M5-R05.** Velocities at both keyframes and the IMU bias. See: gtsam_imufactor — whole page
**M5-R06.** Filter: constant cost per step; smoother: re-linearizes past states, more accurate. See: dellaert_kaess — Ch. 2
**M5-R07.** More, denser and older structure to match against, so less drift and fewer degenerate cases. See: kiss_icp_paper — Step 3
**M5-R08.** Each factor touches few variables; sparse solvers make large problems tractable. See: dellaert_kaess — Ch. 3 "Exploiting Sparsity"

## Self-check 2 — Apply
**M5-A01.** Depends on your run; compare differences with the bootstrap CIs. See: evo_metrics_wiki — "evo_ape"
**M5-A02.** Short drive: odometry drift is tiny while GNSS noise (1.5 m, biased) is large. See: navipedia_measurements — error budget
**M5-A03.** E.g. from the ICP residual / benchmark error distributions of module 4. See: gtsam_intro — Section 2 "Modeling Robot Motion"
**M5-A04.** Report seconds and keyframes; batch LM grows with problem size. See: dellaert_kaess — Ch. 5 "Incremental Smoothing and Mapping"
**M5-A05.** Depends on your run. See: lio_sam — `src/mapOptmization.cpp` (degeneracy handling)
