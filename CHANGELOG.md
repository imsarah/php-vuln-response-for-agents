# Changelog

All notable changes to this playbook. Versions are document revisions, not releases of any software.

## 1.9.10 — 2026-10-22

From a real WordPress-in-Docker run (official `wordpress:latest`, Apache + PHP 8.3.36, anonymous volume):

- **The Docker row's "recreate" was the unsafe instruction.** In the official Apache images `conf-enabled/docker-php.conf` sets `AllowOverride All` for `/var/www/`, so `.htaccess php_value` works, needs no restart and survives a recreate. The row now says so, and says how to verify it (read that file, or fetch a file from a directory you denied — 403 proves it).
- **Recreate now carries a warning**: if the docroot is an anonymous volume, a naive `docker run` attaches a new empty one and the site looks wiped. Check `docker inspect` mounts and quote that line in the hand-back.
- **§0b now covers the official image**, which has no wp-cli: installing it is a write needing approval and vanishes on recreate; read the database with a PHP one-liner instead.

## 1.9.9 — 2026-10-22 (no release yet)

Four gaps that two independent agents hit when they actually ran the procedure (one with shell access on a real PHP server, one in its own sandbox):

- **`cli-server` had no mechanism.** It now has a row: the `-d`/`-c` flags on the launch line, with the warning that the setting lives in the process and reverts on restart.
- **Silent failure is now named.** A `500` announces a rejected mechanism; `.htaccess` on nginx and either file on `cli-server` are ignored without a word, so the value must be read back rather than inferred from a `200`.
- **Phase 1 no longer assumes a local web server.** `curl 127.0.0.1` needs something listening; check with `ss -ltnp` first, otherwise ask the panel or the user.
- **Phase 2 confirms the docroot read-only first** (process cmdline, server config, panel, user), and calls the marker upload what it is — a write that needs approval, not something implied by the README's promise.
- Phase 9 names the concrete trap: an Ubuntu `8.3.6` can be patched where a string comparison with `8.3.36` says otherwise.

## 1.9.8 — 2026-10-22 (no release yet)

- **The agent must ask for access, not wait for it.** The prompt now tells it to ask for site access and say exactly what it needs and why; Phase 3 says "ask for it — do not wait to be offered it", and the 60-second step notes the agent has no access of its own.

## 1.9.7 — 2026-10-22

- **"Holds no credentials" was misleading for the shell/SSH mode.** True of the document, false of the agent you hand a key to. README (EN/Cantonese/zh-Hant), `INSTALL.md` and Phase 3 now say: the document ships no credentials, **you supply the access**, give the least that works, back up first, revoke afterwards — and whatever you hand over is the agent's blast radius.
- Phase 3 also states plainly that credentials must never be pasted into a chat log.

## 1.9.6 — 2026-10-22

- **The 60-second section contradicted the prompt above it.** Step 1 said "install it once — one command" while the prompt says nothing needs installing. Step 1 now sends the prompt and calls installation optional.
- **Step 3 read as if the agent applies changes by itself.** It now says the agent measures, stops, and waits for approval — matching the read-only constraint in the prompt.
- "It does not act on its own" is now "it acts only on the approval you give in step 3", which is what the phases actually describe.

## 1.9.5 — 2026-10-22

Final pass from the third independent single-file test (4 of 5 checks passed; these are the leftovers):

- **Appendix B headings clashed with the main phases** — the worked example narrated "Phase 1", "Phase 9b" inside the same file. They are now **B1–B10**, and a build assertion keeps them that way.
- **Phase 1 folded a probe upload into the "safest" SSH path.** SSH now gives the CLI version only, with the web SAPI read from the panel or from the probe on the server itself.
- **`REPLACE_ME` is explained where it is used** — a sentinel the operator swaps for a secret only they know.

## 1.9.4 — 2026-10-22

Findings from the fresh-agent test the previous revision asked for (a clean subagent given only the prompt and the raw URL):

- **"Read-only" contradicted the measurement phase.** Uploading a probe or docroot marker is a write. Phase 0 now says so explicitly, and the README prompt adds "ask before uploading a probe or marker file (that is a write)".
- **The single file still pointed at other documents.** Link flattening left bare names like `WORDPRESS.md` in the text, which read as a missing file. `build_skill.py` now rewrites them to **Appendix A / Appendix B**, so a single-file reader is never hunting.
- **"Only a patch is a patch" was easy to misread against Phase 9b.** One line added: a patched release is the fix for the CVE; the mitigation closes the demonstrated chain; they answer different questions.
- **No publication date.** The version line now carries one.

## 1.9.3 — 2026-10-21

- Prompt takes the reviewer's exact wording for the **two agent modes** (shell/SSH can act; chat-only hands over read-only commands) and drops every named agent from the prompt block.
- The **fill-in line** is the reviewer's: `My site: [WordPress / plain PHP], on [host]. [I think it was hacked / I just want to patch.]`
- The prompt also tells the agent to **fetch every file the skill links to**, so a reader is not relying on one URL being complete.
- Kept from the previous revision: the read-only-until-approved constraint, the four expected answers, and the tag-pinned URL note.

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
