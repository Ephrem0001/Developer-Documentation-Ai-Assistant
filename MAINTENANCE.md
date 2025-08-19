Maintenance & Support
=====================

This file documents minimal maintenance, versioning, and support guidance for the Module 1 submission.

Versioning
----------

- Package version is tracked in `src/langchain_documentation_aichatbot/__init__.py` as `__version__`.
- Use semantic versioning for releases: `vMAJOR.MINOR.PATCH`.
- Tag release commits and update the changelog (`CHANGELOG.md`) with notable changes.

Support channels
----------------

- For Module 1 submissions, use GitHub Issues on this repository for questions and bug reports.
- For mentor support or urgent help, contact the program mentor on Discord (e.g., @RP) as described in the program instructions.
- For production deployments, configure a dedicated support channel (Slack/Teams) and an on-call rotation.

Maintenance checklist (minimal)
------------------------------

1. Keep `requirements` and `pyproject.toml` up to date.
2. Run tests on each PR and require a passing CI status before merging.
3. Add a release note and bump `__version__` for releases.
4. Monitor logs for hallucination/user-reported issues and add failing examples to `data/eval`.

Security & secrets
------------------

- Never commit API keys. Use environment variables (.env) or secret stores for deployments.
- Rotate keys on schedule and audit access.

Contact
-------

Create an issue or pull request and tag the repository owner to request more help.
