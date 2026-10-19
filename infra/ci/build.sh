#!/usr/bin/env bash
# Configure and build the C++ pipeline. Usage: infra/ci/build.sh [source_dir] [build_dir]
set -euo pipefail
SRC="${1:-.}"
BUILD="${2:-$SRC/build}"
cmake -S "$SRC" -B "$BUILD" -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build "$BUILD"
