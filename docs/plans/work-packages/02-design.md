# WP02 - Architecture, Interfaces, and Design Baseline

## Purpose

Define one implementable architecture and stable public interfaces before code is written.

## Dependencies

Gate G1 passed.

## Read first

- Official design-document requirements
- `decisions.md`
- `docs/srs/SRS.md`
- `docs/design/DESIGN_TEMPLATE.md`
- Current repository structure

## Design approach

Use a simple layered/MVC-style structure:

- `controller`: terminal input/output and conversion from strings.
- `model`: PIR data, validation, manager CRUD, search criteria/parser/evaluation.
- `storage`: `.pim` serialization and validation.
- `main.py`: composition root only.

Use two read-only reviewers after the primary design is drafted:

1. Architecture/cohesion reviewer.
2. Search/persistence/testability reviewer.

## Files to create

```text
docs/design/TECHNICAL_CONTRACT.md
docs/design/Design_Document.md
docs/design/diagrams/architecture.mmd
docs/design/diagrams/components.mmd
docs/design/diagrams/search-update-sequence.mmd
```

## Technical contract must freeze

- Exact field names and Python types.
- Exact date conversion boundary.
- Record validation rules.
- `PIMManager` public methods, parameters, returns, and exceptions.
- Search grammar, tokenizer/parser approach, Criterion interface, and errors.
- Storage API, JSON schema/version, and load atomicity.
- CLI command names, prompts, argument rules, and model-error presentation.
- What belongs in `model` and what is forbidden there.

Recommended main API:

```text
PIMManager.create_note(text)
PIMManager.create_task(description, deadline)
PIMManager.create_event(description, start_time, alarm_time)
PIMManager.create_contact(name, address, mobile_number)
PIMManager.get(record_id)
PIMManager.list_all()
PIMManager.update(record_id, **changes)
PIMManager.delete(record_id)
PIMManager.search(criterion)
parse_criterion(expression)
save_pim(manager, path)
load_pim(path)
```

## Required design-document content

- Generic architecture pattern, reason, and mapping to this PIM.
- Diagram of the architecture.
- Diagram of main components/classes and relationships.
- Fields and all important public/protected method signatures and exceptions.
- Sequence or activity diagram that includes defining a search criterion, searching, selecting a result, and updating it.
- Text explanation for every diagram.

## Verification

- Trace each FR to at least one proposed component/API.
- Confirm no business rule is left only in the CLI.
- Confirm `model` performs no file or terminal I/O.
- Confirm load failure cannot mutate the active manager.
- Confirm the search design does not use `eval()`.
- Render diagram sources and inspect them.
- Run `git diff --check`.

## Gate G2

- One field vocabulary and one command vocabulary.
- Public API and exceptions are sufficiently precise to implement tests first.
- All required diagrams have source files and explanations.
- Both reviewers' material concerns are resolved.

## Copy-ready prompt

```text
在 D:\comp3211\COMP3211-PIM 执行 WP02。读取 master plan、WP02、官方设计要求、冻结的SRS和decisions.md。设计一套最小的 controller/model/storage 架构，写 TECHNICAL_CONTRACT.md 和 Design_Document.md 初稿，并生成架构图、主要组件关系图、定义criterion→搜索→选择→修改的时序图源文件。使用两个只读子Agent分别审核架构职责和搜索/持久化/可测试性，主Agent解决问题。不要实现产品代码。完成验证，通过G2后提交、推送并创建PR。
```
