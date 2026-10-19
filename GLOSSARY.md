# Glossary

## Coming from bioinformatics

Many tools in this program are ones you already use under another name. Each row points to where the SLAM version is taught; read it there. The phase gates end with one "Bridge" question each that builds on this table.

| You know | SLAM / vision term | Module | Read (links.yaml id) |
|---|---|---|---|
| Reference genome build (GRCh37 vs GRCh38) and its coordinates | Frame and datum conventions: `T_<to>_<from>`, WGS84, a local ENU origin | m0, m1 | `navipedia_ecef_enu` |
| Structural superposition (Kabsch), RMSD after superposition | Closed-form SVD step of point-to-point ICP; ATE after trajectory alignment | m4, m6 | `stachniss_icp_1`; `evo_metrics_wiki` (wiki page "Alignment") |
| PCA of a local covariance matrix | Surface normal = eigenvector of the smallest eigenvalue of a point's neighbourhood | m4 | provided code `pipeline/src/registration/normals.cpp` |
| k-nearest-neighbour search (e.g. single-cell kNN graphs) | KD-tree nearest-neighbour data association in ICP | m4 | `stachniss_icp_2`; `nanoflann` |
| Weighted least squares, regression with known variances | Nonlinear least squares with noise-weighted residuals (Gauss-Newton) | m2, m5 | `barfoot_ser` ("Nonlinear Non-Gaussian Estimation") |
| HMM forward algorithm | Bayes filter; the Kalman filter is its Gaussian case | m2 | `labbe_kalman` (02-Discrete-Bayes) |
| Mahalanobis distance, χ² test | NEES filter-consistency test; gating of measurements | m2 | `labbe_kalman` (08-Designing-Kalman-Filters, NEES) |
| Batch effect, systematic offset | Sensor biases (IMU bias states, GNSS bias) estimated jointly with the state | m2, m3 | `kalibr_imu_noise` ("The Noise Model Parameters in Kalibr") |
| Probabilistic graphical model, Bayesian network | Factor graph | m5 | `dellaert_kaess` (Ch. 1) |
| Microscopy image registration and stitching | Feature matching + RANSAC between camera images | m4b | `opencv_matcher`; `stachniss_pcv_ransac` |
| Seed-and-extend search (BLAST) | Two-phase place recognition: fast candidate retrieval, then precise alignment | m6 | `scan_context_paper` (Section III-C "Two-phase Search") |
| Aligning a circular sequence at its best rotation | Scan Context column shift: the yaw that best aligns two descriptors | m6 | `scan_context_paper` (Section III-B "Similarity Score") |
| Multiple testing, false discoveries | False loop closures; robust kernels and geometric verification | m6 | `stachniss_robust_ls` |
| Technical vs biological replicates | Simulation seeds (`prepare --seed`) vs different drives | m6 | module 6 README, assignment 5 |
| Snakemake / Nextflow workflow | Argo Workflows DAG on Kubernetes | m7 | `argo_docs` |

## Terms you had to look up

Maintained by trainees. Add a term when you had to look it up. Link to the resource where you found it (use the ids in `resources/links.yaml`).

| Term | One-line meaning (your words) | Source (links.yaml id) | Added by |
|---|---|---|---|
| | | | |
