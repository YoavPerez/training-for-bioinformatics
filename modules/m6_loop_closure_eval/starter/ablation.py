"""Module 6: ablation study over pipeline components.

    python modules/m6_loop_closure_eval/starter/ablation.py --build-dir build --out outputs/m6 \
        --drive data/kitti/2011_09_30/2011_09_30_drive_0027_sync outputs/prep_0027_s0 outputs/prep_0027_s1 ... \
        --drive data/kitti/2011_09_30/2011_09_30_drive_0018_sync outputs/prep_0018_s0 outputs/prep_0018_s1 ...

Each --drive takes the drive directory followed by one or more prep directories of that drive, one per
`prepare --seed` (the simulated GNSS differs per seed). Runs run_pipeline with GNSS, loop closure and deskew
switched on/off, evaluates every run with slampipe.evaluation (ATE/RPE distributions and bootstrap CIs) and
writes summary tables. A per-pose bootstrap CI does not include the variance across GNSS seeds, so the
GNSS-on combinations are also run once per prep directory and summarized across seeds.
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


def summarize_seeds(rmse: dict[tuple[bool, bool, bool], list[float]]) -> str:
    """Markdown table across prepare seeds: one row per (gnss, loops, deskew) combination with the number of
    seeds, the ATE RMSE of each seed, their mean, sample standard deviation (ddof=1) and min-max."""
    # TODO(m6): implement.
    del rmse
    raise NotImplementedError("summarize_seeds")


def split_drive_arg(items: list[Path]) -> tuple[Path, list[Path]]:
    """Provided: --drive DRIVE_DIR PREP_DIR [PREP_DIR ...] -> (drive_dir, prep_dirs)."""
    if len(items) < 2:
        raise SystemExit("--drive needs a drive directory and at least one prep directory")
    return items[0], items[1:]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--out", type=Path, default=Path("outputs/m6"))
    parser.add_argument(
        "--drive",
        nargs="+",
        type=Path,
        action="append",
        metavar="PATH",
        required=True,
        help="DRIVE_DIR PREP_DIR [PREP_DIR ...]: a drive and one prep dir per prepare seed",
    )
    args = parser.parse_args()
    drives = [split_drive_arg(items) for items in args.drive]  # noqa: F841
    # TODO(m6): for each drive and each combination in itertools.product([True, False], repeat=3), run the
    # pipeline with the first prep dir, evaluate optimized.tum against gt.tum (aligned, and unaligned with
    # align=False), and print/save summarize_ablation per drive for both. Then run every GNSS-on combination
    # with each further prep dir as well and print/save summarize_seeds (aligned and unaligned RMSE).


if __name__ == "__main__":
    main()
