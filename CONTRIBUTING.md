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

Where a revision came out of a review, what that review found is recorded in `CHANGELOG.md`. 1.0 was published before the first review (1.1), and not every entry records one.

**Who does that review:** AI systems, not a human security team. To date: Claude (Anthropic, web and CLI) and Hermes Agent (a local model), asked to attack the document — contradict itself, break on a real host, or state something it cannot source. Independent agents were also given nothing but the prompt and run against real servers, including WordPress in Docker; the `CHANGELOG.md` entries say which runs produced which fix. The repository owner reviews and merges.

That is worth knowing before you rely on this: an LLM review is not a security audit, and no entry here should be read as one. If a claim says it was measured, look for the host and the command in its changelog entry; where the entry does not name them, or the result cannot be reproduced, treat it as unverified.

A pull request is merged after (a) the claim is checked against its cited source and (b) a read-through for steps that could cause harm if followed literally. Commit messages name what changed and why; the test suite in `scripts/test_repo.py` runs on every push.
