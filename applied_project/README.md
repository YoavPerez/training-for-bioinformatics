# Applied fusion project (after training)

After the 8 weeks, trainees take the training pipeline into a sensor domain that plays to their own strengths. Length and scope are set per team need. There are no starter solutions: you scope, design and build.

## Shared structure (all tracks)
1. **Proposal** (one page, [`proposal_template.md`](proposal_template.md)): question, hypothesis, dataset, metrics, scope cut.
2. **Design review** with a senior.
3. **Reproduce a baseline** before any new idea.
4. **Tracked experiments on Argo** (commit + config + data version for every number).
5. **Tech report** ([`templates/tech_report.md`](../templates/tech_report.md)) and a **cross-track presentation**. Judged with [`templates/rubric.md`](../templates/rubric.md).

## Licenses — check before you start

| Dataset | Track | License | Commercial use | Access |
|---|---|---|---|---|
| [NEON AOP](https://www.neonscience.org/data-collection/airborne-remote-sensing) | A | CC BY 4.0 (CC0 before 2026-06-30) | Yes, with attribution | Free account required; [usage policies](https://www.neonscience.org/usage-policies) |
| [NeonTreeEvaluation](https://github.com/weecology/NeonTreeEvaluation) | A | CC0-1.0 (repository) | Yes | GitHub |
| [IEEE GRSS DFC 2018 (Houston)](https://www.grss-ieee.org/community/technical-committees/2018-ieee-grss-data-fusion-contest/) | A (alt.) | Contest terms; redistribution forbidden | **No** | **Availability unconfirmed:** the original portal is archived; ask GRSS |
| [MUUFL Gulfport](https://github.com/GatorSense/MUUFLGulfport) | A (alt.) | MIT (repository); cite dataset papers | Yes | GitHub |
| [Wild-Places](https://csiro-robotics.github.io/Wild-Places/) | B | CC BY-NC-SA 4.0 | **No** | [CSIRO Data Access Portal](https://data.csiro.au/collection/csiro:56372) |
| [BotanicGarden](https://github.com/robot-pesg/BotanicGarden) | B | No formal license, "academic purposes" | **No** | OneDrive / Baidu / SJTU links in README |
| [FOR-instance](https://zenodo.org/records/8287792) | B | CC BY 4.0 | Yes | Zenodo |
| [Boreas](https://www.boreas.utias.utoronto.ca/) | C | CC BY 4.0 ([AWS registry](https://registry.opendata.aws/boreas/)) | Yes | Public S3 bucket |
| [MulRan](https://sites.google.com/view/mulran-pr) | C (alt.) | CC BY-NC-SA 4.0 | **No** | Request form |
| [Oxford Radar RobotCar](https://oxford-robotics-institute.github.io/radar-robotcar-dataset/) | C (alt.) | CC BY-NC-SA 4.0 | **No** (by agreement) | Registration |

The Trento hyperspectral + LiDAR dataset from the original curriculum was dropped: no official public download could be found. Non-commercial datasets are fine for training and research, but never for product work. Ask before using results from them outside the team.

## Track A — Ecology (LiDAR + hyperspectral)
- **Data:** NEON AOP (discrete-return LiDAR `DP1.30003.001`, hyperspectral reflectance mosaic `DP3.30006.001`, RGB) plus field surveys; benchmark: NeonTreeEvaluation. Alternatives for faster iteration: MUUFL Gulfport (and DFC 2018 if GRSS can still provide it).
- **Why it fits:** a hyperspectral pixel behaves like an omics profile (many correlated features, dimensionality reduction, classification). The training stack covers georeferencing, LiDAR and registration.
- **Project options** (in order of difficulty):
  1. Tree species classification from fused spectral + LiDAR-structural features vs either sensor alone, with proper statistical tests.
  2. Quantify hyperspectral-to-LiDAR misregistration and its effect on classification accuracy.
  3. Change detection between repeat flights over the same site.

## Track B — Forest SLAM and place recognition
- **Data:** Wild-Places (forest LiDAR, revisits over months); BotanicGarden (LiDAR, cameras, IMU, ground truth); FOR-instance (tree segmentation). Some files are ROS bags: read them with the `rosbags` Python package (no ROS installation or ROS knowledge needed), as `data/download.py --static-imu` does.
- **Why it fits:** forests defeat urban-tuned methods because scenes look alike, and sequence matching is the trainees' home turf.
- **Project options:**
  1. SeqSLAM-style sequence matching over LiDAR descriptors vs single-scan place recognition (your module 6 Scan Context).
  2. Run the training pipeline on forest data and characterize where it fails.
  3. Add tree-instance landmarks as factors in the pose graph.

## Track C — Radar (optional)
- **Data:** Boreas (LiDAR, FMCW radar, camera, GNSS/IMU, all seasons); alternatives MulRan, Oxford Radar RobotCar.
- **Project:** radar odometry, or radar-to-LiDAR-map localization, evaluated where LiDAR degrades (rain, snow).

## Getting the data
[`download.py`](download.py) automates what can be automated and prints the manual steps for the rest:

```bash
python applied_project/download.py licenses                          # print the table above
python applied_project/download.py neon-list --product DP1.30003.001 --site SJER
python applied_project/download.py neon-get --product DP1.30003.001 --site SJER --month 2021-03 --dest data/neon
python applied_project/download.py boreas --sequence boreas-2020-11-26-13-58 --sensors lidar applanix --dest data/boreas
python applied_project/download.py for-instance --dest data/for_instance
python applied_project/download.py manual                            # Wild-Places, BotanicGarden, MulRan, Oxford, DFC2018
```

NEON downloads need a free account token (`export NEON_TOKEN=...`) since 2026-06-30. Boreas uses the AWS CLI with `--no-sign-request`.
