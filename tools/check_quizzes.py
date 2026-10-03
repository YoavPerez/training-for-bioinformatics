"""Checks the self-check quizzes for consistency.

    python tools/check_quizzes.py

For every modules/m*/quiz/ and modules/phase_gates/:
  * questions are tagged **<ID>.** (e.g. **M1-R03.**, **M0B-A02.**, **PA-07.**)
  * module quizzes have the sections "## Self-check 1 — Readiness", "## Self-check 2 — Apply"
    and "## Explain to your mentor"
  * every question id has exactly one answer in the answers file, and vice versa
  * every answer points to a resource ("See: <links.yaml id>") that exists
  * answers stay short (no teaching prose): at most MAX_ANSWER_CHARS before the pointer
"""

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
ID = re.compile(r"\*\*((?:M\d[A-Z]?-[RA]|P[A-D]-)\d{2})\.\*\*")
MAX_ANSWER_CHARS = 220
SECTIONS = ["## Self-check 1 — Readiness", "## Self-check 2 — Apply", "## Explain to your mentor"]


def link_ids() -> set[str]:
    return {link["id"] for link in yaml.safe_load((REPO / "resources" / "links.yaml").read_text())["links"]}


def answers(path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ID.search(line)
        if m:
            out.setdefault(m.group(1), []).append(line[m.end() :].strip())
    return out


def check_pair(questions: Path, answer_file: Path, ids: set[str], module: bool) -> list[str]:
    errs = []
    rel = questions.relative_to(REPO)
    if not answer_file.exists():
        return [f"{rel}: missing {answer_file.name}"]
    text = questions.read_text(encoding="utf-8")
    if module:
        for s in SECTIONS:
            if s not in text:
                errs.append(f"{rel}: missing section '{s}'")
    q_ids = ID.findall(text)
    dup = {i for i in q_ids if q_ids.count(i) > 1}
    if dup:
        errs.append(f"{rel}: duplicate question ids {sorted(dup)}")
    if module and (not any("-R" in i for i in q_ids) or not any("-A" in i for i in q_ids)):
        errs.append(f"{rel}: needs both readiness (R) and apply (A) questions")
    ans = answers(answer_file)
    for i in sorted(set(q_ids) - ans.keys()):
        errs.append(f"{rel}: question {i} has no answer")
    for i in sorted(ans.keys() - set(q_ids)):
        errs.append(f"{answer_file.relative_to(REPO)}: answer {i} has no question")
    for i, lines in ans.items():
        if len(lines) > 1:
            errs.append(f"{answer_file.relative_to(REPO)}: {i} answered {len(lines)} times")
        body = lines[0]
        m = re.search(r"See:\s*([a-z0-9_]+)", body)
        if not m:
            errs.append(f"{answer_file.relative_to(REPO)}: {i} has no 'See: <resource id>' pointer")
            continue
        if m.group(1) not in ids:
            errs.append(f"{answer_file.relative_to(REPO)}: {i} points to unknown resource '{m.group(1)}'")
        if len(body[: m.start()]) > MAX_ANSWER_CHARS:
            errs.append(f"{answer_file.relative_to(REPO)}: {i} answer too long (keep it to the answer + pointer)")
    return errs


def main() -> int:
    ids = link_ids()
    errs = []
    count = 0
    for module in sorted((REPO / "modules").glob("m[0-9]*_*")):
        q = module / "quiz" / "self_check.md"
        if not q.exists():
            errs.append(f"{module.name}: missing quiz/self_check.md")
            continue
        errs += check_pair(q, module / "quiz" / "self_check_answers.md", ids, module=True)
        count += 1
    for gate in sorted((REPO / "modules" / "phase_gates").glob("phase_?.md")):
        errs += check_pair(gate, gate.with_name(gate.stem + "_answers.md"), ids, module=False)
        count += 1
    for e in errs:
        print("ERROR", e)
    print(f"{count} quizzes checked, {len(errs)} errors")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
