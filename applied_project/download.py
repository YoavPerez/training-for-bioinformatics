"""Applied-project dataset helpers. Automates what is public; prints manual steps for the rest.

python applied_project/download.py {licenses,neon-list,neon-get,boreas,for-instance,manual} ...
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

NEON_API = "https://data.neonscience.org/api/v0"

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
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
        return json.load(r)


def neon_list(product: str, site: str) -> None:
    data = _get_json(f"{NEON_API}/products/{product}")["data"]
    print(data["productCode"], "-", data["productName"])
    for s in data["siteCodes"]:
        if s["siteCode"] == site:
            print(site, "months:", ", ".join(s["availableMonths"]))
            return
    print(f"site {site} not available; sites: {', '.join(s['siteCode'] for s in data['siteCodes'])}")


def neon_get(product: str, site: str, month: str, dest: Path, pattern: str) -> None:
    files = _get_json(f"{NEON_API}/data/{product}/{site}/{month}")["data"]["files"]
    files = [f for f in files if pattern in f["name"]]
    total = sum(int(f["size"]) for f in files) / 1e9
    print(f"{len(files)} files, {total:.1f} GB -> {dest}")
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        target = dest / f["name"]
        if not target.exists():
            urllib.request.urlretrieve(f["url"], target)


def boreas(sequence: str, sensors: list[str], dest: Path) -> None:
    if not shutil.which("aws"):
        sys.exit("needs the AWS CLI (pip install awscli)")
    cmd = ["aws", "s3", "sync", "--no-sign-request", f"s3://boreas/{sequence}", str(dest / sequence), "--exclude", "*"]
    for s in sensors:
        cmd += ["--include", f"{s}/*"]
    cmd += ["--include", "calib/*"]
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
    p = sub.add_parser("boreas")
    p.add_argument("--sequence", required=True)
    p.add_argument("--sensors", nargs="+", default=["lidar", "applanix"])
    p.add_argument("--dest", type=Path, required=True)
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
        neon_get(args.product, args.site, args.month, args.dest, args.pattern)
    elif args.cmd == "boreas":
        boreas(args.sequence, args.sensors, args.dest)
    elif args.cmd == "for-instance":
        for_instance(args.dest)


if __name__ == "__main__":
    main()
