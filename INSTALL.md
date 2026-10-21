# Installing this as a skill

The repository is a valid skill package: `SKILL.md` (frontmatter + body) is the skill, `GUIDE.md` is the same body for plain reading.

## Hermes

```bash
mkdir -p ~/.hermes/skills/devops
git clone https://github.com/imsarah/php-vuln-response-for-agents.git   ~/.hermes/skills/devops/php-vuln-response-for-agents
```

Restart the session (or start a new one). Confirm with `skills_list` — it should appear as `php-vuln-response-for-agents`. The description is the trigger: when a task involves hardening or patching a PHP site, the agent loads the body automatically.

## Claude Code

```bash
mkdir -p ~/.claude/skills/php-vuln-response-for-agents
curl -fsSL https://raw.githubusercontent.com/imsarah/php-vuln-response-for-agents/main/SKILL.md   -o ~/.claude/skills/php-vuln-response-for-agents/SKILL.md
```

(Project-scoped alternative: `.claude/skills/php-vuln-response-for-agents/SKILL.md` inside the repo you are working in.)

## Grok (xAI)

```bash
mkdir -p ~/.grok/skills/php-vuln-response-for-agents
curl -fsSL https://raw.githubusercontent.com/imsarah/php-vuln-response-for-agents/main/SKILL.md   -o ~/.grok/skills/php-vuln-response-for-agents/SKILL.md
```

Grok discovers skills from `./.grok/skills/` (walked up to the repo root), `~/.grok/skills/`, `~/.agents/skills/` and any enabled plugin's `skills/` directory; user-invocable skills also appear as `/<skill-name>`. Unknown frontmatter keys are ignored, so the `version` / `license` / `metadata` keys here are harmless.

Grok is fully Claude Code compatible, so the Claude Code path above works as-is with no extra setup.

Project-scoped alternative: `.grok/skills/php-vuln-response-for-agents/SKILL.md` in the repo you are working in.

## Any other agent

Either:

- **Instruction file** — append `GUIDE.md` to the project's `AGENTS.md` / `CLAUDE.md` / system prompt, or
- **Retrieval** — point the agent at `https://raw.githubusercontent.com/imsarah/php-vuln-response-for-agents/main/GUIDE.md` and have it fetch the file when a PHP hardening task appears.

## Keeping it current

```bash
cd ~/.hermes/skills/devops/php-vuln-response-for-agents && git pull
```

## What the agent gets

- The hard rules (back up, one change at a time, never claim unverified success)
- A 7-phase procedure: identify → get access → measure → choose mechanism by SAPI → apply → verify → patch
- The body assumes shell, panel or file access; an agent with no execution tools can only advise
- A failure-mode table for the traps that actually happen (root `.php` 404s, `php_value` 500s, `mysqli` disappearing after a version switch, CDN cache hiding changes)
