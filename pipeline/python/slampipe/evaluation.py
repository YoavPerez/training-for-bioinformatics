"""Modules 5 and 6: trajectory evaluation on top of evo (module 5: ATE and bootstrap CI; module 6: RPE).

    python -m slampipe.evaluation <estimate.tum> <reference.tum> [--out metrics.json] [--no-align]

Prints and optionally writes ATE/RPE summaries with bootstrap confidence intervals.
ATE is SE(3)-aligned by default; `--no-align` keeps the absolute frame (e.g. GNSS-fused ENU).
The output records the mode as "ate": {"aligned": true|false, ...}.
"""

import argparse
import json
from collections.abc import Callable
from pathlib import Path

import numpy as np
from evo.core.trajectory import PoseTrajectory3D
from evo.tools import file_interface


def load_tum(path: Path) -> PoseTrajectory3D:
    """Provided."""
    return file_interface.read_tum_trajectory_file(str(path))


def ate_errors(est: PoseTrajectory3D, ref: PoseTrajectory3D, align: bool = True, max_diff: float = 0.05) -> np.ndarray:
    """Per-pose absolute translation errors [m] after time association and (optionally) SE(3) alignment.

    Must not modify the inputs.
    """
    # TODO(m5): use evo (sync, alignment, metrics.APE).
    raise NotImplementedError("ate_errors")


def rpe_errors(
    est: PoseTrajectory3D, ref: PoseTrajectory3D, delta_m: float = 10.0, max_diff: float = 0.05
) -> np.ndarray:
    """Relative translation errors [m] over segments of delta_m metres of travelled distance."""
    # TODO(m6): use evo (metrics.RPE).
    raise NotImplementedError("rpe_errors")


def bootstrap_ci(
    values: np.ndarray,
    statistic: Callable[[np.ndarray], float] = np.mean,
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float]:
    """Percentile bootstrap (1 - alpha) confidence interval of statistic(values)."""
    # TODO(m5): implement.
    raise NotImplementedError("bootstrap_ci")


def summarize(errors: np.ndarray) -> dict[str, float]:
    """Provided: distribution summary with a bootstrap CI on the mean."""
    errors = np.asarray(errors, dtype=float)
    lo, hi = bootstrap_ci(errors)
    return {
        "n": int(errors.size),
        "rmse": float(np.sqrt(np.mean(errors**2))),
        "mean": float(np.mean(errors)),
        "median": float(np.median(errors)),
        "p95": float(np.quantile(errors, 0.95)),
        "max": float(np.max(errors)),
        "mean_ci95": [lo, hi],
    }


def evaluate_ate(est_path: Path, ref_path: Path, align: bool = True) -> dict:
    """Provided: ATE summary only (module 5). `align` is passed to ate_errors and recorded as "aligned"."""
    return {"aligned": align, **summarize(ate_errors(load_tum(est_path), load_tum(ref_path), align=align))}


def evaluate(est_path: Path, ref_path: Path, rpe_delta_m: float = 10.0, align: bool = True) -> dict[str, dict]:
    """Provided: ATE (as evaluate_ate) and, for trajectories longer than 2 * rpe_delta_m, RPE (module 6)."""
    result = {"ate": evaluate_ate(est_path, ref_path, align=align)}
    ref = load_tum(ref_path)
    if ref.path_length > 2.0 * rpe_delta_m:
        result["rpe"] = summarize(rpe_errors(load_tum(est_path), ref, rpe_delta_m))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("estimate", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--rpe-delta", type=float, default=10.0)
    parser.add_argument("--no-align", action="store_true", help="ATE without SE(3) alignment (absolute frame)")
    args = parser.parse_args()
    result = evaluate(args.estimate, args.reference, args.rpe_delta, align=not args.no_align)
    text = json.dumps(result, indent=2)
    print(text)
    if args.out:
        args.out.write_text(text + "\n")


if __name__ == "__main__":
    main()
