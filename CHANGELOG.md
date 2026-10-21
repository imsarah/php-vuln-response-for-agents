# Changelog

All notable changes to this playbook. Versions are document revisions, not releases of any software.

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
