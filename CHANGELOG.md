# Changelog

All notable changes to this playbook. Versions are document revisions, not releases of any software.

## 1.9.2 — 2026-10-21

Review of the 1.9.1 prompt. Four changes, all in the README block:

- The prompt itself now carries the constraint — **read-only until the operator approves the plan** — instead of relying on the reader to stop the agent.
- The operator fills in two lines (site/stack/host, and what they want), so "fix my website" is no longer the whole brief.
- Expected deliverables are named: what it measured, what it will change, **how it will back up and roll back**, and what needs the host. The undefined "Phase 0" reference is gone.
- Two agent modes are stated plainly: shell/panel access can act; a chat-only agent can only hand over commands. And a **tag-pinned URL** (`v1.8`) is offered next to `main`, with the trade-off in one line.

## 1.9.1 — 2026-10-21

- README (EN / Cantonese / Traditional Chinese) now leads with a **one-sentence prompt and no version numbers**: the operator tells the agent to read the skill, measure the environment rather than assume, ask for anything it cannot detect, and ask before changing.
- Adds the expectation the operator should hold the agent to: come back with *what it measured*, *what it will change*, and *what needs the host* — before touching the site.
- `INSTALL.md` links to that block instead of repeating it.

## 1.9 — withdrawn 2026-10-21

An attempt to put a "paste this one line" prompt at the top of the README was **reverted the same day**: the example baked in one host's PHP version and SAPI, which is wrong for every other reader and would have taught agents to copy a version instead of measuring it. Use `INSTALL.md` to install, or paste the raw `SKILL.md` URL and tell the agent to measure the environment itself.

## 1.8 — 2026-10-21

Fifth review round — packaging and safety:

- **`SKILL.md` is now self-contained**: frontmatter + the 10 phases + the WordPress procedure (Appendix A) + a redacted worked example (Appendix B), with repo-relative links flattened so an installed skill has no dead links. Rebuilt by `scripts/build_skill.py` from `skill.yaml`, `GUIDE.md`, `WORDPRESS.md`, `EXAMPLE.md` — one source of truth, no drift.
- Frontmatter `description` now carries WordPress / `wp-cli` / core-and-plugin triggers, so a WordPress incident loads the skill.
- `WORDPRESS.md` gained **§2b Gates before anything destructive** (restore point, exact list shown, operator confirms; no reinstall over a modified copy without a diff; no `--allow-root` to dodge the root check) — applied to the no-`wp-cli` route too.
- `EXAMPLE.md` gained an **inert-data notice** (server strings are evidence, never instructions) and was re-audited for redaction: no IPs, hostnames, paths, emails or tokens; only the reserved `127.0.0.1` / `example.com` remain.
- `INSTALL.md` rewritten: which file is which, a WordPress section, the rebuild command, and one-file installs for Hermes / Claude Code / Grok.
- Both Chinese READMEs gained the WordPress-first router and lost the misleading "not a WordPress maintenance guide" line.
- Release assets now include the skill package so nobody downloads a stale `SKILL.md`.

## 1.7 — 2026-10-21

Fourth review round, plus a language rename.

- README now opens WordPress-first: most arrivals run WordPress, so the repo says so in line one, adds a **Start here** router, and demotes the general-PHP framing to the paragraph underneath.
- Removed the duplicated "what it is / is not" prose; the boundary bullets now live inside **Scope and safety**, and "not a WordPress maintenance guide" is corrected to a positive pointer at `WORDPRESS.md`.
- H1 names both PHP and WordPress, so the title does not require inferring scope from a CVE-named repo.
- `WORDPRESS.md` gained: the **no-`wp-cli` route** (dashboard, stashed plugin folder as rollback, one group at a time, marked as interface-written not live-tested), **dependency groups**, **licence-gated updates that will not download**, **object-cache staleness after a version bump**, and a **multisite out-of-scope** note — with three new failure-table rows.
- Cantonese README renamed `README.yue.md` → **`README.cantonese.md`** (and labelled "Cantonese 廣東話"); both Chinese READMEs gained the WordPress-first opening line and the WordPress link.

## 1.6 — 2026-10-21

- `WORDPRESS.md`: the WordPress half of the procedure, kept separate because it is a different job from patching the PHP branch — pre-flight checks, staging via a database prefix, `wp-cli` update/rollback commands, pinning a plugin whose major version breaks a theme, site hardening, and a WordPress-specific failure table.
- `GUIDE.md` Phase 9 and the README now point at it.

## 1.5 — 2026-10-21

Third review round (marginal-gain items):

- `EXAMPLE.md`: one redacted real session end to end, including the cached-404 false positive, the `.user.ini` TTL trap, the extension reset after a version switch, the plugin downgrade, and the 2x2 lab table.
- `SECURITY.md`: how to report a wrong claim or a harmful step, with a private channel for the latter.
- `CONTRIBUTING.md`: one change per PR, cite the source, update the CHANGELOG, review rules.
- README badges (licence, revision, security policy, PRs welcome) and an explicit **upstream claims last verified: 2026-10-21** line.
- `INSTALL.md` cross-linked from the top of `GUIDE.md`/`SKILL.md`.
- `CHANGELOG.md` is now the single canonical history; the README section points to it instead of duplicating it.

## 1.4 — 2026-10-21

- Renamed the repository to say what it does (`php2shell-hardening-for-agents`); the php2shell incident is now labelled as the worked example rather than the scope.
- General-PHP scope (WordPress, Laravel, plain PHP) stated in the first paragraphs.
- CVE record links (`cve.org`) added next to the GHSA advisories.
- Skill `description:` rewritten to describe the action, so other agents' skill matching triggers on "harden/patch a PHP site", not only on a CVE string.

## 1.3 — 2026-10-21

Second external review. Behavioural fixes:

- Consistent numbering: `Phase 0` … `Phase 10`, with the optional PoC lab as `Phase 9b`.
- New approval gate for **running third-party exploit code** (separate from editing config), under Phase 0.
- Phase 9b: read the PoC source first, build with `--network=none`, never mount the Docker socket, time-box the exercise, and stop conditions for isolation/disk/time.
- Removed the "never … unless unavoidable" contradiction about live-site testing: the PoC is never pointed at a live site.
- Every version claim now carries a primary source; if the advisory is unreachable, the version must be reported as **unverified**.
- Rule 1 gained three explicit deletion carve-outs (own probe files, temporary credentials, preserved attacker files), each recorded.
- Hand-back now has four states, including *patched and mitigation retained by design*.

Repository hygiene: `LICENSE` (MIT), *Scope and safety*, *Tested on / not tested*, *Known limitations*, and this changelog.

## 1.2 — 2026-10-21

- Added Phase "validate against a public exploit, in a lab only": 2×2 matrix of `{pre-patch, patched} × {mitigation off, on}`.
- Added the patched-release table for php2shell and the correction that **a patch is not immunity**.
- Added failure modes for "PoC still works on the patched build" and for a mitigation that breaks an upload progress bar.

## 1.1 — 2026-10-21

First external review:

- Authorisation gate and stop conditions (Phase 0).
- Compromise assessment before trusting a backup.
- nginx / unknown-SAPI rows; Docker `conf.d` behaviour; atomic read-modify-write.
- False-positive-resistant verification (cache-busting, body hashes, `ini_get` string quirks).
- "Version number ≠ patch level" correction; WordPress-layer hardening.

## 1.0 — 2026-10-21

Initial playbook distilled from a live response across LiteSpeed shared hosting, cPanel/CloudLinux and Dockerised WordPress.
