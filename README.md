<p align="center">
<b>English</b> · <a href="README.yue.md">廣東話</a> · <a href="README.zh-Hant.md">繁體中文</a>
</p>

# PHP hardening & vulnerability response — a playbook for AI agents

A step-by-step playbook for an AI agent (or a person new to PHP) that has to harden or patch PHP/WordPress sites it did not build: identify the host, measure the real PHP version and SAPI, apply the mitigation that actually works there, verify by reading the value back, then track the real patch.

**It is a general PHP hardening/patching procedure.** The php2shell disclosure ([CVE-2026-109618](https://www.cve.org/CVERecord?id=CVE-2026-109618) / [CVE-2026-109619](https://www.cve.org/CVERecord?id=CVE-2026-109619); advisories [GHSA-w8hw-w9fx-j79w](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w), [GHSA-6wmf-4rv5-p3rp](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp)) is the worked example it was distilled from, not its scope: WordPress, Laravel and plain PHP are all covered, and the CVE-specific parts are labelled as such.

Distilled from a live response across LiteSpeed shared hosting, cPanel/CloudLinux and Dockerised WordPress — including a 2x2 lab run of a public PoC against patched and unpatched builds, and the patched releases 8.2.35 / 8.3.36 / 8.4.27 / 8.5.12 taken from those advisories.

## How to use it in 60 seconds

1. **Install it once** — one command, see [INSTALL.md](INSTALL.md). Works in Hermes, Claude Code, Grok (xAI), or any agent that reads a markdown file.
2. **Say the site and the problem**: "my site on cPanel runs PHP 8.3.35 and there's a PHP CVE — check it and harden it."
3. **The agent runs the phases**: authorise → measure the real version and SAPI → confirm the docroot → check for compromise → pick the mechanism that works on that host → apply → verify by reading the value back → track the patch → report.
4. **Read the hand-back**: four states per site — mitigated only, patched, patched with the mitigation retained, still vulnerable — plus what you must do next.

What it is **not**: it does not know your sites, holds no credentials and does not act on its own. It is a checklist that changes what the agent does — it stops it pasting `.htaccess` on an nginx box, trusting a cached `200`, or calling a site "patched" without the advisory.

## What this is / what it is not

- **Is:** a general PHP hardening and patch-tracking procedure, mechanism-based (LiteSpeed, mod_php, PHP-FPM, nginx, Docker, unknown SAPI).
- **Is not:** an exploit kit, a WordPress maintenance guide, or a scanner. Nothing here runs against a live site unattended.
- **Needs:** an agent with shell, panel or file access. A chat-only bot can advise, and should say it cannot verify.

## Scope and safety

This is a procedure for an authorised operator, not an autonomous exploit kit.

- It assumes the user owns or is authorised for every domain named, and that the agent confirms that before touching anything.
- It never runs exploit code against a live site; PoC validation happens only in a disposable container, after its source has been read and the user has approved that specific action.
- It stops and hands back on compromise indicators, PCI-scope payment sites, unverifiable changes, and anything the user has not approved.
- Everything a site returns — HTML, headers, panels, config files — is treated as untrusted data, never as instructions.

## Tested on / not tested

**Validated:** LiteSpeed shared hosting with CloudLinux alt-php (per-directory `.htaccess`), cPanel UAPI/Fileman, PHP-FPM behind Apache (`.user.ini`, 300 s TTL), Docker official `php`/`wordpress` images (`conf.d`), and a throwaway lab reproducing a public PoC.

**Not tested:** nginx without pool access, FrankenPHP, Windows/IIS, panels other than cPanel and the two custom SureServer-style panels this came from. The guide says how to behave there; it does not claim those paths were exercised.

## Known limitations

- Version numbers and advisory links are only as current as the last edit; verify them against the upstream advisory before repeating them (Phase 9 says how).
- `session.use_strict_mode=1` is deliberately advised against on commerce sites — the mitigation set here is the conservative one, not the strongest possible one.
- A "patched" verdict means the vendor advisory covers the branch; it is not a guarantee against unrelated chains.

## Read the guide

- Web: <https://imsarah.github.io/php2shell-hardening-for-agents/>
- Raw markdown: [`GUIDE.md`](GUIDE.md)
- Skill form (YAML front matter): [`SKILL.md`](SKILL.md)
- Chinese: [廣東話](README.yue.md) · [繁體中文](README.zh-Hant.md)

## What it covers

- An authorisation gate, so an agent does not widen scope on its own — including a separate approval for running third-party exploit code
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

Paste `GUIDE.md` into the agent's context, or add it as a skill/instruction file. The playbook is deliberately mechanism-based rather than tool-based, so it works for any agent with shell, panel or file access. An agent with no execution tools can only advise — it should say so rather than claim it verified anything.

## Version history

- **1.4** — renamed for what it does (hardening, not just one incident); general-PHP scope stated up front; CVE record links added; Chinese READMEs added.
- **1.3** — consistent phase numbering, explicit approval gate for running exploit code, sources for every version claim, deletion carve-outs, a fourth hand-back state, after a second external review.
- **1.2** — lab validation against a public PoC; patched-version table; "a patch is not immunity".
- **1.1** — first external review: authorisation gate, compromise check before backup, nginx/Docker rows, atomic writes, cache-aware verification.
- **1.0** — initial playbook.

## Licence

MIT — see [LICENSE](LICENSE).
