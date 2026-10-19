"""Module 8 acceptance tests: structure of the tech report."""

import re

import pytest

REPORT = "modules/m8_research_mini_project/report/report.md"
SECTIONS = ["## Question", "## Hypothesis", "## Setup", "## Results", "## Limitations", "## Conclusion"]


# Template placeholders look like <component> or <What exists today ...>. Code spans and common HTML tags
# (<br>, <img ...>, <sub>, ...) and autolinks (<https://...>) are not placeholders.
_HTML_OR_LINK = r"(?!(?:br|img|sub|sup|details|summary|a|p|b|i|em|strong|code|kbd|div|span)\b|https?:)"
_PLACEHOLDER = re.compile(r"<" + _HTML_OR_LINK + r"[A-Za-z][^<>\n]*>")


def _placeholders(text):
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    prose = re.sub(r"`[^`\n]*`", "", prose)
    return _PLACEHOLDER.findall(prose)


@pytest.fixture
def report(repo_root):
    path = repo_root / REPORT
    assert path.exists(), f"write {REPORT} from templates/tech_report.md"
    return path


def test_has_every_section(report):
    text = report.read_text(encoding="utf-8")
    for section in SECTIONS:
        assert section in text, f"missing section {section}"


def test_has_commit_and_dataset(report):
    setup = report.read_text(encoding="utf-8").split("## Setup")[1].split("## Results")[0]
    commit = re.search(r"\*\*Commit:\*\*\s*`?([0-9a-f]{7,40})\b`?", setup)
    hash_ = commit.group(1) if commit else ""
    assert re.search(r"[a-f]", hash_) or len(hash_) >= 10, "state the commit hash on the **Commit:** line of Setup"
    assert re.search(r"drive_\d{4}|sequence", setup, re.IGNORECASE), "state the dataset / drive in Setup"
    assert re.search(r"seeds?\D{0,3}\d", setup, re.IGNORECASE), "state the `prepare` seed(s) in Setup"


def test_no_placeholders(report):
    text = report.read_text(encoding="utf-8")
    assert not re.search(r"`<hash>`|`<path>`", text), "template placeholders are still present"
    assert not _placeholders(text), f"template placeholders are still present: {_placeholders(text)}"


def test_figures_exist(report):
    text = report.read_text(encoding="utf-8")
    figures = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    assert figures, "include at least one figure"
    for fig in figures:
        assert (report.parent / fig).exists(), f"missing figure {fig}"


def test_length_is_two_to_three_pages(report):
    words = len(report.read_text(encoding="utf-8").split())
    assert 450 <= words <= 1800, f"{words} words; aim for 2–3 pages"


def test_reports_uncertainty(report):
    results = report.read_text(encoding="utf-8").split("## Results")[1].split("## Limitations")[0]
    assert re.search(r"\bCI\b|confidence|±|p95|percentile|std", results, re.IGNORECASE), (
        "report distributions or uncertainty, not single numbers"
    )
