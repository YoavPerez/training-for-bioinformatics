"""Applied-project dataset helpers. Automates what is public; prints manual steps for the rest.

python applied_project/download.py {licenses,neon-list,neon-get,boreas,for-instance,manual} ...
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

NEON_API = "https://data.neonscience.org/api/v0"
NEON_TOKEN_HELP = (
    "NEON requires a free API token: create an account, then export NEON_TOKEN=<your token> "
    "(see https://www.neonscience.org/usage-policies)"
)

LICENSES = [
    ("NEON AOP", "A", "CC BY 4.0 (CC0 before 2026-06-30)", "yes"),
    ("NeonTreeEvaluation", "A", "CC0-1.0", "yes"),
    ("GRSS DFC 2018", "A alt", "contest terms, no redistribution", "NO"),
    ("MUUFL Gulfport", "A alt", "MIT (repo); cite papers", "yes"),
    ("Wild-Places", "B", "CC BY-NC-SA 4.0", "NO"),
    ("BotanicGarden", "B", "academic purposes only", "NO"),
    ("FOR-instance", "B", "CC BY 4.0", "yes"),
    ("Boreas", "C", "CC BY 4.0", "yes"),
    ("MulRan", "C alt", "CC BY-NC-SA 4.0", "NO"),
    ("Oxford Radar RobotCar", "C alt", "CC BY-NC-SA 4.0", "NO (by agreement)"),
]

MANUAL = {
    "Wild-Places": "Download from the CSIRO Data Access Portal: https://data.csiro.au/collection/csiro:56372",
    "BotanicGarden": "Follow the per-sequence links in https://github.com/robot-pesg/BotanicGarden (README)",
    "MulRan": "Request access via the Download tab of https://sites.google.com/view/mulran-pr",
    "Oxford Radar RobotCar": "Register at https://oxford-robotics-institute.github.io/radar-robotcar-dataset/ "
    "then use Downloads",
    "GRSS DFC 2018": "Original portal archived; ask IEEE GRSS (see "
    "https://www.grss-ieee.org/community/technical-committees/2018-ieee-grss-data-fusion-contest/)",
    "NeonTreeEvaluation": "git clone https://github.com/weecology/NeonTreeEvaluation (see its README for data)",
    "MUUFL Gulfport": "git clone https://github.com/GatorSense/MUUFLGulfport",
}


def _get_json(url: str) -> dict:
    headers = {"User-Agent": "slam-onboarding"}
    if os.environ.get("NEON_TOKEN") and url.startswith(NEON_API):
        headers["X-API-Token"] = os.environ["NEON_TOKEN"]
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if url.startswith(NEON_API) and e.code in (401, 403):
            hint = "NEON_TOKEN was rejected. " if os.environ.get("NEON_TOKEN") else ""
            sys.exit(f"HTTP {e.code} from {url}\n{hint}{NEON_TOKEN_HELP}")
        sys.exit(f"HTTP {e.code} from {url}")


def neon_list(product: str, site: str) -> None:
    data = _get_json(f"{NEON_API}/products/{product}")["data"]
    print(data["productCode"], "-", data["productName"])
    for s in data["siteCodes"]:
        if s["siteCode"] == site:
            print(site, "months:", ", ".join(s["availableMonths"]))
            return
    print(f"site {site} not available; sites: {', '.join(s['siteCode'] for s in data['siteCodes'])}")


def neon_get(
    product: str, site: str, month: str, dest: Path, pattern: str, dry_run: bool, max_gb: float, yes: bool
) -> None:
    files = _get_json(f"{NEON_API}/data/{product}/{site}/{month}")["data"]["files"]
    files = [f for f in files if pattern in f["name"]]
    total = sum(int(f["size"]) for f in files) / 1e9
    print(f"{len(files)} files, {total:.1f} GB -> {dest}")
    if dry_run:
        for f in files:
            print(f"  {f['name']} ({int(f['size']) / 1e6:.1f} MB)")
        return
    if total > max_gb and not yes:
        sys.exit(f"{total:.1f} GB exceeds --max-gb {max_gb:g}: narrow it with --pattern (see --dry-run) or pass --yes")
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        target = dest / f["name"]
        if not target.exists():
            urllib.request.urlretrieve(f["url"], target)


def _s3_size_gb(prefix: str) -> float:
    """Total size of every key under an s3://boreas prefix (aws s3 ls --summarize pages through the whole listing)."""
    cmd = ["aws", "s3", "ls", "--no-sign-request", "--recursive", "--summarize", prefix]
    out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.strip().startswith("Total Size:"):
            return int(line.split(":")[1]) / 1e9
    return 0.0


def boreas(sequence: str, sensors: list[str], dest: Path, dry_run: bool, max_gb: float, yes: bool) -> None:
    if not shutil.which("aws"):
        sys.exit("needs the AWS CLI (pip install awscli)")
    folders = [*sensors, "calib"]
    sizes = {f: _s3_size_gb(f"s3://boreas/{sequence}/{f}/") for f in folders}
    total = sum(sizes.values())
    for f, gb in sizes.items():
        print(f"  {sequence}/{f}/ {gb:.2f} GB")
    print(f"total {total:.1f} GB -> {dest / sequence}")
    if dry_run:
        return
    if total > max_gb and not yes:
        sys.exit(f"{total:.1f} GB exceeds --max-gb {max_gb:g}: choose fewer --sensors (see --dry-run) or pass --yes")
    cmd = ["aws", "s3", "sync", "--no-sign-request", f"s3://boreas/{sequence}", str(dest / sequence), "--exclude", "*"]
    for f in folders:
        cmd += ["--include", f"{f}/*"]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def for_instance(dest: Path) -> None:
    files = _get_json("https://zenodo.org/api/records/8287792/files")["entries"]
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        target = dest / f["key"]
        print(f"{f['key']} ({int(f['size']) / 1e9:.2f} GB)")
        if not target.exists():
            urllib.request.urlretrieve(f["links"]["content"], target)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("licenses")
    sub.add_parser("manual")
    p = sub.add_parser("neon-list")
    p.add_argument("--product", required=True)
    p.add_argument("--site", required=True)
    p = sub.add_parser("neon-get")
    p.add_argument("--product", required=True)
    p.add_argument("--site", required=True)
    p.add_argument("--month", required=True, help="YYYY-MM")
    p.add_argument("--dest", type=Path, required=True)
    p.add_argument("--pattern", default="", help="only files whose name contains this")
    p.add_argument("--dry-run", action="store_true", help="list the matching files and sizes, download nothing")
    p.add_argument("--max-gb", type=float, default=5.0, help="refuse larger downloads unless --yes (default 5)")
    p.add_argument("--yes", action="store_true", help="download even above --max-gb")
    p = sub.add_parser("boreas")
    p.add_argument("--sequence", required=True)
    p.add_argument("--sensors", nargs="+", default=["lidar", "applanix"])
    p.add_argument("--dest", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true", help="print the size per folder, download nothing")
    p.add_argument("--max-gb", type=float, default=5.0, help="refuse larger downloads unless --yes (default 5)")
    p.add_argument("--yes", action="store_true", help="download even above --max-gb")
    p = sub.add_parser("for-instance")
    p.add_argument("--dest", type=Path, required=True)
    args = parser.parse_args()

    if args.cmd == "licenses":
        for row in LICENSES:
            print("{:24s} {:7s} {:40s} commercial: {}".format(*row))
    elif args.cmd == "manual":
        for name, step in MANUAL.items():
            print(f"{name}: {step}")
    elif args.cmd == "neon-list":
        neon_list(args.product, args.site)
    elif args.cmd == "neon-get":
        neon_get(args.product, args.site, args.month, args.dest, args.pattern, args.dry_run, args.max_gb, args.yes)
    elif args.cmd == "boreas":
        boreas(args.sequence, args.sensors, args.dest, args.dry_run, args.max_gb, args.yes)
    elif args.cmd == "for-instance":
        for_instance(args.dest)


if __name__ == "__main__":
    main()
