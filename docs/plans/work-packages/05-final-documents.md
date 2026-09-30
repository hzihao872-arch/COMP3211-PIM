# WP05 - Final Documents and Reports

## Purpose

Generate every written deliverable from the same verified code-freeze commit and remove inconsistencies among requirements, design, commands, code, tests, and coverage evidence.

## Dependencies

Gate G4 passed. `docs/reports/code-freeze.md` identifies the exact commit.

## Read first

- Official Project Description PDF and requirement matrix
- `decisions.md`
- `docs/srs/SRS.md`
- `docs/design/Design_Document.md`
- `docs/design/TECHNICAL_CONTRACT.md`
- `docs/reports/code-freeze.md`
- Frozen source, tests, and coverage output

## Multi-agent production

Subagents may draft disjoint files in parallel:

1. SRS/design finalizer.
2. User Manual writer.
3. Developer Manual writer.
4. Requirements/Test Coverage report writer.

The primary Agent integrates and verifies all claims against the freeze commit. If only three subagent slots are available, combine the two coverage reports with the developer manual task.

## Files to finalize

```text
docs/srs/SRS.md
docs/design/Design_Document.md
docs/design/diagrams/*
docs/manuals/Developer_Manual.md
docs/manuals/User_Manual.md
docs/reports/Requirements_Coverage.md
docs/reports/Test_Coverage.md
```

Create final PDFs under:

```text
artifacts/documents/SRS.pdf
artifacts/documents/Design_Document.pdf
artifacts/documents/Developer_Manual.pdf
artifacts/documents/User_Manual.pdf
artifacts/documents/Requirements_Coverage.pdf
artifacts/documents/Test_Coverage.pdf
```

PDF is a group formatting choice for the manuals/reports; do not misstate it as an official format requirement unless the restored PDF says so.

## SRS finalization

- Preserve requirement intent and IDs.
- Reconcile product behavior with the freeze build.
- Do not rewrite the SRS as a class-by-class implementation description.
- Ensure every user story remains covered and every FR/NFR remains verifiable.

## Design finalization

- Regenerate the architecture, component/class, and search-update process diagrams from real packages, classes, public/protected methods, parameters, returns, and exceptions.
- Explain the chosen generic architecture and its PIM mapping.
- Include explanatory text for every diagram.

## Developer Manual

Include one supported platform, actual Python version, IDE guidance, project structure, exact run/test/coverage commands, debugging steps, and clean-checkout setup. Execute every shell command from a clean directory.

## User Manual

Include every real command, prompt, field, format, search rule, output form, invalid-input behavior, save/load behavior, and one complete example session. Capture examples from the frozen program rather than inventing them.

## Requirements Coverage

Include every US and every requirement in the final SRS:

| US/FR/NFR | Status | Source file and symbol | Test/manual evidence | Notes |
|---|---|---|---|---|

Every symbol and test name must exist at the freeze SHA. Mark any gap honestly.

## Test Coverage

Use only the real WP04 evidence. Include environment, exact command, test result, each model module's covered/total lines, total model coverage, and uncovered-line explanations. Do not recalculate or round inconsistently.

## Verification

- Check every command in User Manual against the CLI.
- Check every developer command in a clean checkout.
- Script or manually verify all requirement-coverage symbols and test names.
- Compare all coverage numbers to the raw output.
- Render every final PDF to page images and visually inspect every page.
- Search all final sources and PDFs for stale names and unresolved placeholders.
- Run `git diff --check`.

## Gate G5

- Six final PDFs exist and render cleanly.
- All documents identify or record the same freeze SHA.
- No document invents code, tests, commands, or metrics.
- Requirements Coverage connects US/SRS requirements to implementation and evidence.
- Only explicit human-data placeholders remain.

## Copy-ready prompt

```text
在 D:\comp3211\COMP3211-PIM 执行 WP05。读取 master plan、WP05、官方矩阵、最终decisions/SRS/Design、code-freeze文件和冻结源码测试。使用不超过四个子Agent分别处理SRS/Design、User Manual、Developer Manual、两份coverage报告，且只编辑互不重叠的文件；主Agent统一术语并逐项核对冻结commit。生成六份最终PDF，使用相应documents/pdf技能逐页渲染检查。所有命令、类、方法、测试和覆盖率必须来自真实证据。通过G5后提交、推送并创建PR。
```
