# PHP vulnerability response — a playbook for AI agents

A step-by-step playbook for an AI agent (or a person new to PHP) that has to harden or patch PHP/WordPress sites it did not build: identify the host, measure the real PHP version and SAPI, apply the mitigation that actually works there, verify by reading the value back, then track the real patch.

Distilled from a live response to a PHP core disclosure (CVE-2026-109618 / CVE-2026-109619) across LiteSpeed shared hosting, cPanel/CloudLinux and Dockerised WordPress, including a 2x2 lab run of a public exploit against patched and unpatched builds.

## Read the guide

- Web: <https://imsarah.github.io/php-vuln-response-for-agents/>
- Raw markdown: [`GUIDE.md`](GUIDE.md)
- Skill form (YAML front matter): [`SKILL.md`](SKILL.md)

## What it covers

- An authorisation gate, so an agent does not widen scope on its own
- Measuring exposure with the least intrusive method available
- Confirming the docroot before editing anything
- Checking whether the site is *already* compromised, before trusting a backup
- Choosing the right mechanism per SAPI: LiteSpeed, mod_php, PHP-FPM, nginx, Docker, unknown
- Writing config safely, and verifying without fooling yourself (cache, TTL, body hashes)
- Telling mitigation apart from a real patch, including backported vendor builds
- Validating a claim against a public PoC **in a throwaway lab**, and reading the result honestly (a patch is not immunity)
- A failure-mode table that maps symptoms to what they actually mean

## Install as a skill

See [INSTALL.md](INSTALL.md) for Hermes, Claude Code, Grok (xAI) and generic agents.

## Using it with an agent

Paste `GUIDE.md` into the agent's context, or add it as a skill/instruction file. The playbook is deliberately mechanism-based rather than tool-based, so it works for any agent with shell, panel or file access.

## Licence

MIT.
