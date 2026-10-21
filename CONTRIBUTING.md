# Contributing

Corrections are welcome, especially ones backed by a primary source (a vendor advisory, release notes, or output from a real host).

## Ground rules

1. **One change per pull request**, with the source that justifies it in the description.
2. **No invented versions, CVEs or severity.** If you cannot cite it, do not add it.
3. **Say when it was measured.** New mechanism rows should name the SAPI and how the value was read back, not "this works".
4. **Do not add anything that acts on a live site unattended.** This playbook is for an authorised operator; steps that run exploit code against production will be rejected.
5. **Regenerate `SKILL.md`** (`python3 scripts/build_skill.py`) if you touched `GUIDE.md`, `WORDPRESS.md`, `EXAMPLE.md` or `skill.yaml`; a PR that edits a source file without regenerating the skill is incomplete.
6. Update `CHANGELOG.md` in the same PR. `CHANGELOG.md` is the canonical history; the summary in `README.md` is a pointer to it and must not be edited independently.

## Review

Every revision so far has been through at least one external review before publication, with the findings listed in `CHANGELOG.md`. A pull request is merged after (a) the claim is checked against its cited source and (b) a read-through for steps that could cause harm if followed literally. Reviewers are named in the merge commit; there is no anonymous merge policy.
