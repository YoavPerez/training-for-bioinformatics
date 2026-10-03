#!/usr/bin/env bash
# Builds the pipeline and runs one module's acceptance tests. Usage: infra/ci/test_module.sh m3
set -euo pipefail
infra/ci/build.sh . build
SLAM_REQUIRE_DATA=1 python tools/module_tests.py --build-dir build "$1"
