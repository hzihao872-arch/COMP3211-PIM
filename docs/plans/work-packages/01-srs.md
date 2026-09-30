# WP01 - Software Requirements Specification

## Purpose

Turn US1-US11 and the frozen group decisions into a concise, complete, consistent, realistic, and verifiable SRS before implementation starts.

## Dependencies

Gate G0 passed. The exact Lecture 04 structure is available or has been independently verified.

## Read first

- Official Project Description PDF
- Relevant Lecture 04 slides
- `decisions.md`
- `requirements-checklist.md`
- `docs/plans/official-requirements-matrix.md`
- `docs/srs/SRS_TEMPLATE.md`

## Multi-agent review

Use three read-only roles:

1. Requirements drafter: maps every user story to functional requirements.
2. User/error reviewer: checks inputs, outputs, invalid cases, and recovery behavior.
3. Verification reviewer: checks whether every FR/NFR can be objectively tested.

The primary Agent writes one coherent document and resolves duplication or conflict.

## Files to create

```text
docs/srs/SRS.md
docs/srs/requirements-catalog.csv
docs/srs/SRS_draft.pdf
```

## Required content

- Cover information with human-data placeholders where necessary.
- Preface, introduction, system scope, and glossary.
- US1-US11.
- Stable `FR-xx` requirements for all required behavior.
- Stable `NFR-xx` requirements that are measurable or directly checkable.
- A trace table from US to FR.

Do not include System Models, System Evolution, Appendix, or Index unless the restored official materials prove they are required. Keep class names and implementation details out of the SRS.

## Required search coverage

The SRS must separately specify:

- defining a criterion;
- applying a criterion to search PIRs;
- type criterion;
- text containment on applicable text fields;
- time `<`, `>`, `=` on applicable time fields;
- `&&`, `||`, `!` combinations;
- the group-selected syntax, quoting, precedence, parentheses, invalid-expression behavior, and field applicability.

## Quality target

Prefer roughly 35-60 useful requirements over hundreds of implementation-level statements. Each requirement should describe one observable obligation and identify its user story.

## Verification

- Programmatically or manually confirm every US1-US11 appears in the trace table.
- Check FR/NFR identifiers for uniqueness.
- Search for unresolved `TBD`, contradictory date formats, command formats, or field names.
- Render the PDF to images and inspect every page for clipping, overlap, unreadable tables, and broken characters.
- Run `git diff --check`.

## Gate G1

- All user stories map to requirements.
- Every requirement has a verification idea.
- Search and `.pim` behavior are complete.
- Official requirements and chosen product rules agree.
- The reviewed SRS baseline is committed before implementation.

## Copy-ready prompt

```text
在 D:\comp3211\COMP3211-PIM 执行 WP01。先读取 master plan、WP01文件、官方PDF、Lecture 04结构材料、冻结后的 decisions.md、官方要求矩阵和SRS模板。使用需求、用户/错误、可验证性三个只读子Agent审阅，再由主Agent统一写 docs/srs/SRS.md 和 requirements-catalog.csv，并生成、渲染检查 SRS_draft.pdf。不要写尚不存在的类名或代码细节，不得遗漏US7的类型、文本、时间比较和逻辑组合。完成所有验证，通过G1后提交、推送并创建PR，报告真实结果和遗留问题。
```
