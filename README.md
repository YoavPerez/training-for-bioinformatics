# SLAM, LiDAR & Navigation Onboarding Program

A self-serve onboarding program for researchers joining the SLAM / 3D LiDAR / GNSS-IMU fusion / mapping team. It is written for people coming from bioinformatics: strong in statistics, data analysis and scientific programming, new to robotics, geometry and computer vision. [`GLOSSARY.md`](GLOSSARY.md) starts with a map from bioinformatics terms you know to the SLAM terms you will meet. It takes roughly 9–10 weeks. Over modules 0–8 (plus 0b and 4b) you build **one LiDAR-inertial-GNSS mapping pipeline** in `pipeline/`, and each module adds one layer to it. An optional applied project follows.

All teaching is done by external, free resources. This repository gives you the assignments, starter code, tests, self-check quizzes and review checklists. Your mentor answers questions and reviews your work.

## Program map

The program has four **phases**. Each phase ends with a cumulative phase-gate self-check (`modules/phase_gates/`) and a short demo to your mentor.

| Phase | Module | Folder | Tentative effort |
|---|---|---|---|
| **A. Foundations** | 0. Diagnostic and team conventions | [`modules/m0_conventions`](modules/m0_conventions/) | a few days |
| | 0b. C++ foundations | [`modules/m0b_cpp_foundations`](modules/m0b_cpp_foundations/) | ~4–5 days (1–2 if strong in C++) |
| | 1. 3D geometry, frames, geodesy | [`modules/m1_geometry`](modules/m1_geometry/) | ~1 week |
| | *Phase gate A* | [`modules/phase_gates/phase_A.md`](modules/phase_gates/phase_A.md) | |
| **B. Estimation & sensors** | 2. State estimation fundamentals | [`modules/m2_estimation`](modules/m2_estimation/) | ~1 week |
| | 3. Sensors in depth | [`modules/m3_sensors`](modules/m3_sensors/) | ~1 week |
| | *Phase gate B* | [`modules/phase_gates/phase_B.md`](modules/phase_gates/phase_B.md) | |
| **C. Mapping core** | 4. Point clouds and registration (mid-program checkpoint) | [`modules/m4_registration`](modules/m4_registration/) | ~1 week |
| | 4b. Camera geometry and visual odometry | [`modules/m4b_vision`](modules/m4b_vision/) | ~1 week |
| | 5. Odometry to SLAM with factor graphs | [`modules/m5_factor_graphs`](modules/m5_factor_graphs/) | ~1 week |
| | 6. Loop closure, maps, evaluation | [`modules/m6_loop_closure_eval`](modules/m6_loop_closure_eval/) | ~1 week |
| | *Phase gate C* | [`modules/phase_gates/phase_C.md`](modules/phase_gates/phase_C.md) | |
| **D. Production & research** | 7. Productionizing the pipeline | [`modules/m7_production`](modules/m7_production/) | ~1 week |
| | 8. Research skills mini-project | [`modules/m8_research_mini_project`](modules/m8_research_mini_project/) | remainder |
| | *Phase gate D* | [`modules/phase_gates/phase_D.md`](modules/phase_gates/phase_D.md) | |
| After training | Applied fusion project (tracks A/B/C) | [`applied_project/`](applied_project/) | open |

Efforts are estimates, not deadlines. There is no fixed schedule, and modules can stretch or shrink for each trainee. Do the modules in order, because each one builds on the last.

## About ROS
This program does not use ROS, and none of it requires ROS knowledge. The pipeline is plain C++/Python. Frames, transforms and conventions are taught from first principles. A dedicated ROS 2 module for the whole team is planned for later.

## How every module is organised

C++ runs through the whole program: module 0b builds the foundations, and modules 1–7 and 4b each have a **C++ focus** task (testing, class design, generic code, performance, API design, error handling, tooling, a lean projection loop) reviewed with the rest of the module.

Every module has the same five segments, so you always know where you are:

| # | Segment | What you do | Where |
|---|---|---|---|
| 1 | **Learn** | Study the linked resources at the given chapter, lecture or timestamp. | `README.md` → *Learn from* |
| 2 | **Self-check 1: Readiness** | Answer the concept questions *before* coding, then grade yourself. | `quiz/self_check.md` |
| 3 | **Build** | Complete the `TODO`s in `pipeline/` and in the module's `starter/` until the tests pass. | `README.md` → *Assignment*, `starter/`, `tests/` |
| 4 | **Self-check 2: Apply** | Answer questions about *your own* results and plots. Prepare the "explain to your mentor" prompts. | `quiz/self_check.md` |
| 5 | **Review** | Tick `CHECKLIST.md`, open a PR and request mentor review. | `CHECKLIST.md` |

### Using the self-check quizzes

- Answer every question in writing (in your PR description or a personal notes file) **before** opening `quiz/self_check_answers.md`.
- The answers file gives only the answer and a pointer to where to read (`See: <resource id> — <section>`). Resource ids are listed in [`resources/links.yaml`](resources/links.yaml).
- Score yourself with the table at the top of each quiz, and log the score in `CHECKLIST.md`. The scores are for you and your mentor to adjust pace. They are not a grade.
- "Explain to your mentor" prompts have no answer key. Discuss them at review.

## Your first day

1. Create your own repository from this template ("Use this template" on GitHub), clone it, and add your mentor as a reviewer.
2. Follow **Getting started** below until the pipeline builds and the smoke tests pass.
3. Open [`modules/m0_conventions/README.md`](modules/m0_conventions/README.md) and take the diagnostic quiz (90 minutes, closed book). Hand it to your mentor.
4. Push once and look at CI: `lint` and `smoke` are green, and the eleven `module mN` jobs are red. That is expected; each module's job turns green as you complete it.

## Getting started

1. Read [`CONVENTIONS.md`](CONVENTIONS.md). You will complete it with your mentor in module 0.
2. Open the repo in the dev container (VS Code: *Reopen in Container*), or build the image yourself:
   ```bash
   docker build -t onboarding-dev -f infra/docker/Dockerfile .
   ```
3. Fetch the CI sample data: `python data/download.py --sample`. For the full KITTI raw drives, see [`data/README.md`](data/README.md) and the license notice there.
4. Build and test the pipeline:
   ```bash
   infra/ci/build.sh . build            # cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release && cmake --build build
   ctest --test-dir build -L '^smoke$'
   pytest pipeline/python/tests
   ```
   Configure from the repository root (not `pipeline/`): the root `CMakeLists.txt` sets up the dependencies and the module tests.
   Module tests (plain `ctest --test-dir build` or `pytest`) **fail on purpose** on untouched starter code. Making them pass is the assignment.
   Run one module's acceptance tests (pytest + `ctest -L '^mN$'`) with `python tools/module_tests.py m1`.
5. Start with [`modules/m0_conventions/README.md`](modules/m0_conventions/README.md).

## Working agreements

- **Stuck protocol:** time-box a blocker to about 2 hours, write down what you tried, then ask your mentor.
- **Every assignment is a PR** and is reviewed like production code. Keep PRs small.
- **Paper club:** use [`templates/paper_summary.md`](templates/paper_summary.md) from module 2 on.
- **Reproducibility:** every reported number is tied to a commit, a config and a dataset version.
- **Shared glossary:** add terms you had to look up to `GLOSSARY.md`. Gaps in it show what isn't landing.

## Repository layout

```
CONVENTIONS.md       frames, quaternions, units, time (completed in module 0)
GLOSSARY.md          trainee-maintained glossary
resources/links.yaml every external resource, verified
templates/           paper summary, design doc, tech report, rubric
infra/               Docker image, Argo workflow templates, CI scripts
data/                dataset download scripts and CI sample subset
pipeline/            your growing C++/Python library (starter code with TODOs)
modules/             one folder per module + phase-gate self-checks
tools/               repo tooling (quiz linter, test runners)
applied_project/     post-training project tracks
```
