# Collaboration Guide

## One task, one branch

Do not develop directly on `main`. Create a short branch from the latest `main`:

```powershell
git switch main
git pull
git switch -c feature/search-parser
```

Recommended prefixes:

- `feature/` for new functionality
- `fix/` for a defect
- `docs/` for document-only work
- `test/` for test-only work

## Before committing

1. Run the relevant unit tests.
2. Update the matching requirement or coverage entry.
3. Check that no personal data, API keys, IDE output, or temporary `.pim` data is included.
4. Keep commits focused on one task.

Commit examples:

```text
feat: add task record model
test: cover compound search conditions
docs: define CLI command syntax
fix: preserve records after failed load
```

## Pull requests

Every pull request should state:

- what changed;
- which user story or requirement it addresses;
- how it was tested;
- any decision the team still needs to make.

At least one teammate should review a pull request before it is merged. Resolve conflicts on the feature branch and rerun tests after resolving them.

## Documents

Edit the Markdown sources in `docs/`. Export required final documents to PDF only when preparing a reviewed milestone or final submission. Keep requirement IDs consistent across the SRS, code comments where helpful, tests, coverage report, and presentation.

## Generated content and GenAI

Record material assistance from GenAI or other tools as work proceeds so that the final Honour Declaration can be completed accurately.
