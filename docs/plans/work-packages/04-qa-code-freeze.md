# WP04 - Integration QA, Model Coverage, and Code Freeze

## Purpose

Independently challenge the implementation, fix real defects, produce reproducible evidence, and record the commit used by all final documents.

## Dependencies

Gate G3 passed and the implementation PR is merged.

## Read first

- Official requirements matrix
- `decisions.md`
- `docs/srs/SRS.md`
- `docs/design/TECHNICAL_CONTRACT.md`
- All source and tests

## Audit process

First use read-only subagents:

1. User-story/edge-case auditor.
2. Model isolation/standard-library/API auditor.
3. Persistence/search/data-integrity auditor.

They return findings only. The primary Agent reproduces each issue, applies fixes sequentially using `superpowers:systematic-debugging`, adds regression tests, and reruns the entire suite.

## Required checks

- US1-US11 each have an automated or recorded manual path.
- Four record types round trip through `.pim` with fields and IDs intact.
- Creating after load uses the correct next ID.
- Failed update/load/search leaves current data intact.
- Type, text, `<`, `>`, `=`, `&&`, `||`, `!`, precedence, and nesting work.
- Invalid ID/date/command/search/file cases do not crash the CLI.
- `model` contains no input/output or storage access.
- Product imports are standard library or local project modules only.
- Clean checkout instructions work.

## Coverage

Generate real line coverage for `src/model` only. Prefer a reproducible standard-library `trace` wrapper under `tools/model_coverage.py`; an external development-only coverage tool may be used only if the official rule is confirmed to allow it and it is not a product runtime dependency.

Create:

```text
tools/model_coverage.py
docs/reports/integration-test-log.md
docs/reports/model-coverage-raw.txt
docs/reports/code-freeze.md
```

`code-freeze.md` records:

- final commit SHA;
- Python version and OS;
- run command;
- unit-test command and exact result;
- coverage command and exact per-model result;
- manual CLI acceptance transcript;
- known limitations.

## Required final verification

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
python tools/model_coverage.py
python -m compileall -q src tests tools
git diff --check
git status --short
```

Perform a fresh-copy or clean-directory run using the README instructions.

## Gate G4

- Full suite has zero failures and zero errors.
- Actual model line coverage is recorded per module and in total.
- All audit findings are fixed or documented as accepted limitations that do not violate the SRS.
- The exact freeze SHA is committed and pushed.
- No product behavior changes after this gate without repeating WP04.

## Copy-ready prompt

```text
在 D:\comp3211\COMP3211-PIM 执行 WP04。读取 master plan、WP04、官方矩阵、decisions、SRS、技术合同以及全部源码和测试。先用三个只读子Agent分别审核用户故事/边界、model隔离与标准库、搜索/持久化/数据完整性。主Agent逐项复现，使用systematic-debugging修复并补回归测试。实际运行全套测试、干净目录CLI验收和model行覆盖率，禁止估算数字。创建integration-test-log、coverage原始证据和code-freeze文件，记录真实commit SHA。通过G4后提交、推送并创建PR。
```
