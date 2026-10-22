#!/usr/bin/env python3
"""Regression checks for documentation defects this repo has actually shipped.

Standard library only, no network. Prints one line per check, exits non-zero if
any check fails.

Run from anywhere:  python3 scripts/test_repo.py

The build check runs scripts/build_skill.py inside a temporary copy of the repo,
so running the tests never rewrites the SKILL.md in your working tree.
"""
import pathlib, re, shutil, subprocess, sys, tempfile

root = pathlib.Path(__file__).resolve().parent.parent
REPO_SLUG = "raw.githubusercontent.com/imsarah/php2shell-hardening-for-agents"
READMES = ["README.md", "README.cantonese.md", "README.zh-Hant.md"]
# any indent: fences inside list items are indented to the item's content column
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")

results = []

def check(label, ok, detail=""):
    results.append(ok)
    line = f"{'PASS' if ok else 'FAIL'}  {label}"
    if detail:
        line += f" — {detail}"
    print(line)

def read(name, base=root):
    return (base / name).read_text(encoding="utf-8")

# a) skill.yaml frontmatter: an empty or stripped skill.yaml once built a skill
# with no name, which an agent can never load.
fm = read("skill.yaml")
missing = [k for k in ("name:", "description:", "version:", "license:")
           if not re.search(rf"^{k}", fm, re.M)]
check("a skill.yaml frontmatter", fm.startswith("---") and not missing,
      f"missing {missing}" if missing else ("does not start with '---'" if not fm.startswith("---") else ""))

# b) build succeeds and produces a SKILL.md with frontmatter first.
skill = None
with tempfile.TemporaryDirectory() as tmp:
    work = pathlib.Path(tmp) / "repo"
    shutil.copytree(root, work, ignore=shutil.ignore_patterns(".git"))
    proc = subprocess.run([sys.executable, "scripts/build_skill.py"], cwd=work,
                          capture_output=True, text=True)
    if proc.returncode == 0 and (work / "SKILL.md").exists():
        skill = read("SKILL.md", work)
    lines = skill.splitlines() if skill else []
    ok = proc.returncode == 0 and len(lines) >= 2 and lines[0] == "---" and lines[1].startswith("name:")
    detail = (proc.stderr.strip().splitlines() or ["build failed"])[-1] if proc.returncode else \
             ("" if ok else f"starts with {lines[:2]!r}")
    check("b build_skill.py builds SKILL.md with frontmatter", ok, detail)

if skill is None:
    check("c SKILL.md appendices, no sibling-file names", False, "no SKILL.md built")
    check("e SKILL.md has no relative .md links", False, "no SKILL.md built")
else:
    # c) single-file reader must never be sent to files it does not have.
    problems = [s for s in ("# Appendix A", "# Appendix B") if s not in skill]
    problems += [f"mentions {s}" for s in ("WORDPRESS.md", "EXAMPLE.md") if s in skill]
    check("c SKILL.md appendices, no sibling-file names", not problems, "; ".join(problems))

    # e) no relative markdown links to .md files (absolute http(s) links are fine).
    rel = [m.group(0) for m in re.finditer(r"\]\((?!https?:)[^)\s]*\.md(?:#[^)]*)?\)", skill)]
    check("e SKILL.md has no relative .md links", not rel, ", ".join(rel[:5]))

# d) one version everywhere.
yaml_v = re.search(r"^version:\s*['\"]?([^'\"\s]+)", fm, re.M)
guide_v = re.search(r"^Version (\S+) — \d{4}-\d{2}-\d{2}", read("GUIDE.md"), re.M)
badge_v = re.search(r"img\.shields\.io/badge/version-(.+?)-[A-Za-z]+\.svg", read("README.md"))
found = {"skill.yaml": yaml_v and yaml_v.group(1),
         "GUIDE.md": guide_v and guide_v.group(1),
         "README badge": badge_v and badge_v.group(1).replace("--", "-")}
check("d version consistency", None not in found.values() and len(set(found.values())) == 1,
      ", ".join(f"{k}={v}" for k, v in found.items()))

# f) <Directory> is invalid in .htaccess and returns 500 — it shipped once.
hits = [i for i, l in enumerate(read("WORDPRESS.md").splitlines(), 1) if "<Directory" in l]
check("f WORDPRESS.md has no <Directory", not hits, f"line(s) {hits}" if hits else "")

# g) README must not pin a hardcoded tag (one 404'd); point at the releases page.
pins = []
for name in READMES:
    for i, l in enumerate(read(name).splitlines(), 1):
        if "img.shields.io" in l:
            continue  # the version badge is checked by (d), not a pin
        if re.search(r"/(?:releases/tag|tree|blob|archive/refs/tags)/v?\d+\.\d+"
                     r"|php2shell-hardening-for-agents/v?\d+\.\d+[^/\s]*/"
                     r"|\bv\d+\.\d+\.\d+\b", l):
            pins.append(f"{name}:{i}")
readme = read("README.md")
has_releases = "php2shell-hardening-for-agents/releases)" in readme or \
               "php2shell-hardening-for-agents/releases " in readme
check("g README pins no tag, links releases page", not pins and has_releases,
      (f"pinned tag at {', '.join(pins)}; " if pins else "") +
      ("" if has_releases else "README.md has no releases-page link"))

# h) every fenced code block is closed.
for name in ("GUIDE.md", "WORDPRESS.md"):
    open_at, open_fence = None, None
    for i, l in enumerate(read(name).splitlines(), 1):
        m = FENCE.match(l)
        if not m:
            continue
        fence, info = m.groups()
        if open_fence is None:
            open_at, open_fence = i, fence
        elif fence[0] == open_fence[0] and len(fence) >= len(open_fence) and not info.strip():
            open_at, open_fence = None, None
    check(f"h {name} fenced code blocks closed", open_fence is None,
          f"block opened at line {open_at} never closed" if open_fence else "")

# i) every README carries the one-sentence prompt URL.
missing = [n for n in READMES if REPO_SLUG not in read(n)]
check("i READMEs contain the prompt URL", not missing, f"missing in {missing}" if missing else "")

failed = results.count(False)
print(f"\n{len(results) - failed}/{len(results)} checks passed")
sys.exit(1 if failed else 0)
