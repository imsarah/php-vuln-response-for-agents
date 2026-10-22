# Installing this as a skill

This repo contains no credentials and no site list. The agent reaches only what you hand it: create access for the task, give the least that works, back up first, revoke afterwards.

> **Shortest path:** the README has a [one-sentence prompt](README.md#use-it-in-one-sentence) — paste it into any agent, no install. Everything below is for installing the skill permanently.

`SKILL.md` is a **self-contained** skill: YAML frontmatter plus the full procedure (Phase 0–10), the WordPress patch appendix and a redacted worked example, in one 400-line file. An agent that installs only `SKILL.md` gets everything and will not chase dead links.

The other files are for humans and for agents that prefer to read one topic at a time:

| File | What it is |
|---|---|
| `SKILL.md` | The skill — everything, self-contained |
| `WORDPRESS.md` | The WordPress procedure on its own (Appendix A of the skill) |
| `EXAMPLE.md` | One real session end to end, redacted (Appendix B) |
| `GUIDE.md` | The general PHP procedure on its own (link-flattened into the skill body) |
| `CHANGELOG.md` | What changed in each revision |

Regenerate `SKILL.md` after editing `GUIDE.md`, `WORDPRESS.md`, `EXAMPLE.md` or `skill.yaml`:

```bash
python3 scripts/build_skill.py
```

## WordPress sites

Nothing different to install — the WordPress procedure is already inside `SKILL.md` as Appendix A, and the frontmatter description mentions WordPress, `wp-cli` and core/plugin updates so a WordPress incident pulls the skill in.

If you would rather keep the WordPress document separate (for example, to give a colleague just that part), fetch [`WORDPRESS.md`](https://raw.githubusercontent.com/imsarah/php2shell-hardening-for-agents/main/WORDPRESS.md) and hand it over as a plain instruction file.

## Hermes

```bash
mkdir -p ~/.hermes/skills/devops/php2shell-hardening-for-agents
curl -fsSL https://raw.githubusercontent.com/imsarah/php2shell-hardening-for-agents/main/SKILL.md \
  -o ~/.hermes/skills/devops/php2shell-hardening-for-agents/SKILL.md
```

Restart the session (or start a new one). Confirm with `skills_list` — it should appear as `php2shell-hardening-for-agents`. The description is the trigger: when a task involves hardening or patching a PHP **or WordPress** site, the agent loads the body automatically.

To keep it updated later, re-run the `curl`, or `git clone` the repository into that directory instead (it must be empty first) and `git pull` after.

## Claude Code

```bash
mkdir -p ~/.claude/skills/php2shell-hardening-for-agents
curl -fsSL https://raw.githubusercontent.com/imsarah/php2shell-hardening-for-agents/main/SKILL.md \
  -o ~/.claude/skills/php2shell-hardening-for-agents/SKILL.md
```

(Project-scoped alternative: `.claude/skills/php2shell-hardening-for-agents/SKILL.md` inside the repo you are working in.)

## Grok (xAI)

```bash
mkdir -p ~/.grok/skills/php2shell-hardening-for-agents
curl -fsSL https://raw.githubusercontent.com/imsarah/php2shell-hardening-for-agents/main/SKILL.md \
  -o ~/.grok/skills/php2shell-hardening-for-agents/SKILL.md
```

Grok discovers skills from `./.grok/skills/` (walked up to the repo root), `~/.grok/skills/`, `~/.agents/skills/` and any enabled plugin's `skills/` directory; user-invocable skills also appear as `/<skill-name>`. Unknown frontmatter keys are ignored, so the `version` / `license` keys here are harmless.

Project-scoped alternative: `.grok/skills/php2shell-hardening-for-agents/SKILL.md` in the repo you are working in.

## Any other agent

Either:

- **Instruction file** — append `SKILL.md` (or just `GUIDE.md` for non-WordPress work) to the project's `AGENTS.md` / `CLAUDE.md` / system prompt, or
- **Retrieval** — point the agent at `https://raw.githubusercontent.com/imsarah/php2shell-hardening-for-agents/main/SKILL.md` and have it fetch the file when a hardening task appears.

## Keeping it current

Re-run the install `curl` for your agent; it overwrites `SKILL.md` with the current `main`. Only if you cloned the repository instead (see Hermes above):

```bash
cd ~/.hermes/skills/devops/php2shell-hardening-for-agents && git pull
```

## What the agent gets

- The hard rules (back up, one change at a time, never claim unverified success)
- Phases 0–10: authorise → measure → identify → access → compromise check → mechanism by SAPI → no-access instructions → apply → verify → patch → optional lab validation → hand back
- A WordPress appendix: pre-flight, staging with a database prefix, `wp-cli` and the no-`wp-cli` route, plugin dependency groups, pinning a broken plugin back, destructive-action gates, and a WordPress failure table
- A worked example with the mistakes left in (cached 404, `.user.ini` TTL, a plugin major version breaking `wp-login.php`, the PoC lab, which ran four cells rather than the full 2×2)
- A failure-mode table for the traps that actually happen (root `.php` 404s, `php_value` 500s, `mysqli` disappearing after a version switch, CDN cache hiding changes)
- The body assumes shell, panel or file access; an agent with no execution tools can only advise
