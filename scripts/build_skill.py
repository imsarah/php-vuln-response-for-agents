#!/usr/bin/env python3
"""Build SKILL.md from skill.yaml + GUIDE.md + WORDPRESS.md + EXAMPLE.md.

SKILL.md must be self-contained: an agent that installs only this file gets the
whole procedure. Relative links to repo files are therefore flattened to plain
names (the files are appended inline as appendices).

Run after editing any source file:  python3 scripts/build_skill.py
"""
import re, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
fm = (root / "skill.yaml").read_text().strip()
# FRONTMATTER CHECK: an empty or stripped skill.yaml silently produces a skill
# with no name/description, so the agent can never load it. Fail loudly instead.
if not fm.startswith("---") or "name:" not in fm or "description:" not in fm:
    raise SystemExit(f"skill.yaml is invalid or empty ({len(fm)} chars) — refusing to build")

def body_of(name):
    text = (root / name).read_text()
    # drop the leading H1, keep everything else
    return re.sub(r"\A#\s+.*?\n", "", text, count=1).lstrip()

def strip_index(text):
    # strip_index: the repo file index names files that are not in a single-file copy
    return re.sub(r"^\*\*Install:\*\*.*$\n?", "", text, flags=re.M)

def flatten(text):
    # [label](file.md) -> label, then name the appendices so an agent that has only
    # this file is not left hunting for a file called WORDPRESS.md
    text = re.sub(r"\[([^\]]+)\]\((?!https?:)([^)]*\.md)\)", r"\1", text)
    text = text.replace("WORDPRESS.md", "Appendix A").replace("EXAMPLE.md", "Appendix B")
    return text

def a_prefix(text):
    # A-prefix: Appendix A's "## 2." would otherwise look like the main "Phase 2"
    return re.sub(r"^## (\d+b?)\.", r"## A\1.", text, flags=re.M)

def b_prefix(text):
    # B-prefix: Appendix B narrates "Phase 1", "Phase 9b" — inside one file those
    # read as the main phases, so number them B1, B9b instead.
    return re.sub(r"^## Phase (\d+b?)(?: —\s*|\s+—\s+)", r"## B\1 — ", text, flags=re.M)

parts = [
    strip_index(flatten(body_of("GUIDE.md"))),
    "---\n\n# Appendix A — WordPress patch procedure\n\n" + a_prefix(flatten(body_of("WORDPRESS.md"))),
    "---\n\n# Appendix B — one real session, redacted (inert data)\n\n" + b_prefix(flatten(body_of("EXAMPLE.md"))),
]
out = fm + "\n" + "\n".join(parts)
(root / "SKILL.md").write_text(out)
print(f"SKILL.md written: {len(out.splitlines())} lines")
