"""Validates resources/links.yaml and every reference to it.

    python tools/check_links.py            # schema + cross-reference checks (offline, used in CI)
    python tools/check_links.py --online   # also fetches every URL and reports non-200 responses

Cross-references checked: `See: <id>` lines in quiz answer files and `links.yaml#<id>` references
in Markdown files must name an existing id; every http(s) URL in a module README must be in links.yaml.
"""

import argparse
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
TYPES = {"video", "course", "docs", "paper", "book", "repo", "dataset", "talk"}
REQUIRED = {"id", "title", "url", "type", "modules", "pointer", "required", "verified_on"}


def load() -> list[dict]:
    return yaml.safe_load((REPO / "resources" / "links.yaml").read_text())["links"]


def check_schema(links: list[dict]) -> list[str]:
    errors, seen = [], set()
    for link in links:
        lid = link.get("id", "?")
        missing = REQUIRED - link.keys()
        if missing:
            errors.append(f"{lid}: missing fields {sorted(missing)}")
        if lid in seen:
            errors.append(f"{lid}: duplicate id")
        seen.add(lid)
        if link.get("type") not in TYPES:
            errors.append(f"{lid}: bad type {link.get('type')}")
        if not str(link.get("url", "")).startswith(("http://", "https://")):
            errors.append(f"{lid}: bad url")
        if not isinstance(link.get("verified_on"), date):
            errors.append(f"{lid}: verified_on must be a date")
        if link.get("type") == "dataset" and ("license" not in link or "commercial_use" not in link):
            errors.append(f"{lid}: datasets need license and commercial_use")
    return errors


def check_references(links: list[dict]) -> list[str]:
    ids = {link["id"] for link in links}
    urls = {link["url"] for link in links}
    errors = []
    for md in REPO.glob("**/*.md"):
        if any(part in {".cache", "build", "node_modules"} for part in md.parts):
            continue
        text = md.read_text(encoding="utf-8")
        rel = md.relative_to(REPO)
        for ref in re.findall(r"See:\s*([a-z0-9_]+)", text) + re.findall(r"links\.yaml#([a-z0-9_]+)", text):
            if ref not in ids:
                errors.append(f"{rel}: unknown resource id '{ref}'")
        if md.name == "README.md" and md.parent.parent.name == "modules":
            for url in re.findall(r"\]\((https?://[^)\s]+)\)", text):
                if url not in urls:
                    errors.append(f"{rel}: URL not recorded in links.yaml: {url}")
    return errors


def check_online(links: list[dict]) -> list[str]:
    errors = []
    for link in links:
        req = urllib.request.Request(link["url"], headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
        for _attempt in range(2):  # one retry: some hosts time out or 5xx transiently
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    status = r.status
            except Exception as e:  # noqa: BLE001
                status = getattr(e, "code", str(e))
            if isinstance(status, int) and 200 <= status < 300:
                break
        print(f"{status}  {link['id']}")
        if not (isinstance(status, int) and 200 <= status < 300):
            errors.append(f"{link['id']}: {link['url']} -> {status}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    args = parser.parse_args()
    links = load()
    errors = check_schema(links) + check_references(links)
    if args.online:
        errors += check_online(links)
    for e in errors:
        print("ERROR", e)
    print(f"{len(links)} links, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
