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

def body_of(name):
    text = (root / name).read_text()
    # drop the leading H1, keep everything else
    return re.sub(r"\A#\s+.*?\n", "", text, count=1).lstrip()

def flatten(text):
    # [label](file.md) -> label, then name the appendices so an agent that has only
    # this file is not left hunting for a file called WORDPRESS.md
    text = re.sub(r"\[([^\]]+)\]\((?!https?:)([^)]*\.md)\)", r"\1", text)
    text = text.replace("WORDPRESS.md", "Appendix A").replace("EXAMPLE.md", "Appendix B")
    return text

parts = [
    flatten(body_of("GUIDE.md")),
    "---\n\n# Appendix A — WordPress patch procedure\n\n" + flatten(body_of("WORDPRESS.md")),
    "---\n\n# Appendix B — one real session, redacted (inert data)\n\n" + flatten(body_of("EXAMPLE.md")),
]
out = fm + "\n" + "\n".join(parts)
(root / "SKILL.md").write_text(out)
print(f"SKILL.md written: {len(out.splitlines())} lines")
