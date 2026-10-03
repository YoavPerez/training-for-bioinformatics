"""Module 7: CI regression gate.

    python -m slampipe.gate <metrics.json> <baseline.json> [--tolerance 0.10]

Exits with status 1 if any gated metric regressed beyond the tolerance.
Both files have the layout written by `slampipe.evaluation` ({"ate": {"rmse": ...}, ...}).
"""

import argparse
import json
import sys
from pathlib import Path

# (section, metric) pairs that are gated; lower is better for all of them.
GATED = [("ate", "rmse"), ("ate", "p95")]


def check(metrics: dict, baseline: dict, tolerance: float) -> list[str]:
    """Returns one human-readable message per regression; empty if the gate passes.

    A metric regresses when it exceeds baseline * (1 + tolerance). A gated metric that is missing
    from `metrics` is also a failure.
    """
    # TODO(m7): implement.
    raise NotImplementedError("check")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("metrics", type=Path)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("--tolerance", type=float, default=0.10)
    args = parser.parse_args()
    failures = check(json.loads(args.metrics.read_text()), json.loads(args.baseline.read_text()), args.tolerance)
    for f in failures:
        print(f"REGRESSION {f}")
    print("gate:", "FAIL" if failures else "PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
