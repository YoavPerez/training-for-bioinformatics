#!/usr/bin/env bash
# Formatting, linting and content checks.
set -euo pipefail
ruff check .
ruff format --check .
find pipeline modules \( -name '*.cpp' -o -name '*.hpp' \) -print0 | xargs -0 clang-format --dry-run --Werror
python tools/check_links.py
python tools/check_quizzes.py
