# Security policy

This repository is a **procedure**, not software. It also collects claims about PHP releases and CVEs, and a wrong claim here can send an agent down the wrong path on a live site — so corrections are treated as security-relevant.

## Reporting a problem

- **A wrong or stale technical claim** (version number, advisory status, a directive that does not work on a SAPI): open an issue with the link to the primary source that contradicts it. If it would cause a destructive action, say so in the title.
- **A step that could cause harm if followed literally** (deleting data, running exploit code against a live system, acting without authorisation): report it **privately** via GitHub's [Report a vulnerability](https://github.com/imsarah/php2shell-hardening-for-agents/security/advisories/new) form, not as a public issue.
- **A vulnerability in a site you are using this playbook on**: this repository cannot help you; patch the site and contact your host. See the advisories linked in the README.

## What to expect

- Harmful-step reports: acknowledged within 7 days, fixed in the next revision with a CHANGELOG entry.
- Stale claims: fixed with a source link; no revision bump if nothing else changes.
- There is no supported version matrix — the newest revision is the only one maintained.

## Scope

In scope: correctness and safety of the instructions, and the accuracy of every version/CVE claim. Out of scope: the security of PHP itself, of WordPress, or of any host named in passing.
