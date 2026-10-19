"""Runs the visible tests of one or all modules and reports pass/fail per module.

    python tools/module_tests.py [--build-dir build] [--expect pass|fail] [m1 m2 ...]

--expect fail  asserts that every selected module's tests FAIL (untouched starter code).
--expect pass  asserts that every selected module's tests PASS (solutions overlaid).
A module's tests are its pytest files in modules/<module>/tests plus ctest tests labelled m<N>.
The C++ build directory is rebuilt first (cmake --build) if it has been configured.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def module_dirs(selected: list[str]) -> list[Path]:
    dirs = sorted(p for p in (REPO / "modules").glob("m[0-9]*_*") if p.is_dir())
    if selected:
        dirs = [d for d in dirs if d.name.split("_")[0] in selected]
    return dirs


def run_module(module: Path, build_dir: Path) -> bool:
    label = module.name.split("_")[0]
    ok = True
    ran = False
    tests = module / "tests"
    if any(tests.glob("test_*.py")):
        ran = True
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(tests)], cwd=REPO)
        ok &= r.returncode == 0
    if (tests / "CMakeLists.txt").exists():
        ran = True
        r = subprocess.run(["ctest", "--test-dir", str(build_dir), "-L", f"^{label}$", "--output-on-failure"], cwd=REPO)
        ok &= r.returncode == 0
    if not ran:
        print(f"{module.name}: no tests found")
        return False
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-dir", type=Path, default=Path(os.environ.get("SLAM_BUILD_DIR", REPO / "build")))
    parser.add_argument("--expect", choices=["pass", "fail"])
    parser.add_argument("modules", nargs="*")
    args = parser.parse_args()
    os.environ["SLAM_BUILD_DIR"] = str(args.build_dir.resolve())

    # Rebuild first, so the C++ tests never run stale binaries after you edit a source file (no-op when up to date).
    if (args.build_dir / "CMakeCache.txt").is_file():
        if subprocess.run(["cmake", "--build", str(args.build_dir)], cwd=REPO).returncode != 0:
            print(f"ERROR: `cmake --build {args.build_dir}` failed: fix the compile errors above first")
            return 1

    results = {m.name: run_module(m, args.build_dir.resolve()) for m in module_dirs(args.modules)}
    print("\n=== module test summary ===")
    for name, passed in results.items():
        print(f"{name:32s} {'PASS' if passed else 'FAIL'}")
    if args.expect == "pass":
        return 0 if all(results.values()) else 1
    if args.expect == "fail":
        unexpected = [n for n, p in results.items() if p]
        for n in unexpected:
            print(f"ERROR: {n} tests pass on untouched starter code")
        return 1 if unexpected else 0
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
