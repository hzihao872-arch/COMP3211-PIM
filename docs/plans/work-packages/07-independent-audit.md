# WP07 - Independent Cross-Artifact Audit and Repair

## Purpose

Review the project as a strict grader, find contradictions and missing evidence, repair confirmed problems, and prevent polished but false deliverables.

## Dependencies

Gate G6 passed.

## Read first

Everything in the repository plus all generated PDFs and slide artifacts.

## Phase 1 - Read-only audit

Use three independent read-only subagents:

1. **Requirement/traceability grader:** PDF requirements, SRS, Requirements Coverage, US1-US11, scoring criteria.
2. **Code/test/manual grader:** design, APIs, source, tests, CLI output, User/Developer Manuals, coverage evidence.
3. **Submission/presentation grader:** required files, PDF rendering, slides, scripts, time/identity rules, declaration readiness, final paths.

Each finding must include:

- severity: blocking/high/medium/low;
- exact file and section/line;
- requirement or evidence violated;
- reproducible check;
- recommended repair.

## Phase 2 - Reproduce and repair

The primary Agent merges duplicates, rejects unsupported findings, reproduces accepted problems, and repairs them sequentially.

If any repair changes product behavior or model tests:

1. Invalidate the previous code freeze.
2. Return to WP04 verification and create a new freeze SHA.
3. Regenerate affected WP05/WP06 documents.

Do not patch documents to hide an implementation defect.

## Files to create

```text
docs/reports/final-audit.md
docs/reports/final-audit-resolution.md
```

## Mandatory audit queries

```powershell
rg -n "TODO|TBD|PLACEHOLDER|MEMBER_[A-Z]|example student|230[0-9]+" .
rg -n "^\s*(from|import)\s+" src tests tools
git diff --check
```

Also verify:

- every class/method/test cited in documents exists;
- every CLI example runs;
- every diagram matches code;
- every US/FR/NFR coverage row has evidence;
- coverage numbers match raw output;
- all PDFs open and render correctly;
- the two videos are treated as separate deliverables;
- official and group-chosen rules are not confused;
- AI assistance is logged.

## Gate G7

- No unresolved blocking/high findings.
- Any medium/low accepted risk has a written reason.
- Final audit resolution lists the exact current freeze SHA and document versions.
- Full test/coverage verification remains valid after repairs.

## Copy-ready prompt

```text
在 D:\comp3211\COMP3211-PIM 执行 WP07。先只读，不立即修。读取全部仓库和生成的PDF/幻灯片，用三个只读子Agent分别做要求追踪审计、代码测试手册审计、提交展示审计。每项发现必须给严重级、准确位置、违反的要求、复现方法和修复建议。主Agent去重并复现后再修复。若改变产品行为，必须回到WP04重新冻结并重生成受影响文档，不能只改文档掩盖问题。创建审计及解决报告，完成规定搜索、测试、coverage和PDF检查，通过G7后提交、推送并创建PR。
```
