"""Module 6: ablation study over pipeline components.

    python modules/m6_loop_closure_eval/starter/ablation.py --build-dir build --out outputs/m6 \
        --drive data/kitti/2011_09_30/2011_09_30_drive_0027_sync outputs/prep_0027 \
        --drive data/kitti/2011_09_30/2011_09_30_drive_0018_sync outputs/prep_0018

Runs run_pipeline with GNSS, loop closure and deskew switched on/off, evaluates every run with
slampipe.evaluation (ATE/RPE distributions and bootstrap CIs) and writes a summary table.
"""

import argparse
import itertools  # noqa: F401
import subprocess
from pathlib import Path

VARIANTS = {
    "gnss": ("", "--no-gnss"),  # (on, off) flags
    "loops": ("--loops", ""),
    "deskew": ("--deskew", ""),
}


def variant_flags(gnss: bool, loops: bool, deskew: bool) -> list[str]:
    """Provided: command-line flags for one combination."""
    flags = [
        VARIANTS["gnss"][0 if gnss else 1],
        VARIANTS["loops"][0 if loops else 1],
        VARIANTS["deskew"][0 if deskew else 1],
    ]
    return [f for f in flags if f]


def run(build_dir: Path, drive: Path, prep: Path, out: Path, flags: list[str]) -> Path:
    """Provided: one pipeline run; returns its output directory."""
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [str(build_dir / "pipeline/apps/run_pipeline"), str(drive), str(prep), str(out), *flags],
        check=True,
        stderr=subprocess.DEVNULL,
    )
    return out


def summarize_ablation(results: dict[tuple[bool, bool, bool], dict]) -> str:
    """Markdown table: one row per (gnss, loops, deskew) combination with ATE RMSE, median, p95 and the
    95 % CI of the mean, plus the difference to the all-on configuration."""
    # TODO(m6): implement.
    del results
    raise NotImplementedError("summarize_ablation")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--out", type=Path, default=Path("outputs/m6"))
    parser.add_argument(
        "--drive", nargs=2, type=Path, action="append", metavar=("DRIVE_DIR", "PREP_DIR"), required=True
    )
    args = parser.parse_args()  # noqa: F841
    # TODO(m6): for each drive and each combination in itertools.product([True, False], repeat=3), run the
    # pipeline, evaluate optimized.tum against gt.tum (aligned, and unaligned with align=False), and print/save
    # summarize_ablation per drive for both.


if __name__ == "__main__":
    main()
