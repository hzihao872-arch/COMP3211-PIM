# WP03 - Complete Product Implementation and Unit Tests

## Purpose

Implement the complete PIM and automated tests in one coherent conversation, following the frozen contract and test-driven development.

## Dependencies

Gate G2 passed.

## Read first

- `decisions.md`
- `docs/srs/SRS.md`
- `docs/design/TECHNICAL_CONTRACT.md`
- `docs/design/Design_Document.md`
- `requirements-checklist.md`

## Agent policy

Use one modifying Agent for the implementation. Do not dispatch multiple coding Agents into the same checkout. Read-only code reviewers may be used only after a coherent implementation exists.

Use `superpowers:test-driven-development` for every behavior and `superpowers:verification-before-completion` before every completion claim.

## Target structure

```text
src/
├─ main.py
├─ model/
│  ├─ pir.py
│  ├─ note.py
│  ├─ task.py
│  ├─ event.py
│  ├─ contact.py
│  ├─ manager.py
│  └─ search.py
├─ controller/
│  └─ cli.py
└─ storage/
   └─ pim_file.py

tests/
├─ model/
├─ controller/
├─ storage/
└─ test_acceptance.py
```

## Implementation sequence

For every subtask: write a failing test, run it and confirm the intended failure, write the minimum code, run target tests, run all tests, then commit when the subtask is coherent.

### Task 1 - Test entry and four PIR types

- Correct test discovery so `tests/model` does not shadow `src/model`.
- Implement the base record and four required types.
- Validate IDs, required strings, and datetime types.
- Keep terminal and file I/O out of model.

Recommended command:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
```

### Task 2 - Manager CRUD

- Create all four record types.
- Allocate increasing IDs and never reuse deleted IDs.
- Get one, list all in stable order, update, and delete.
- Reject nonexistent IDs and forbidden `id`/`type` updates.
- Make failed updates atomic.

### Task 3 - Pure search language

- Criterion interface and type/text/time predicates.
- AND, OR, NOT.
- Tokenizer and recursive-descent parser.
- Parentheses and frozen precedence.
- Clear syntax/field/type errors.
- No `eval()`.

Required cases include each individual operator, precedence, nesting, empty input, missing values, unmatched parentheses, unknown field/type, and consecutive operators.

### Task 4 - Manager search integration

- Search using the single contract-approved entry point.
- Preserve record order.
- Return an empty list for no matches.
- Search must not mutate records.
- Add the search-then-update acceptance path used by the design diagram.

### Task 5 - `.pim` persistence

- UTF-8 JSON, `.pim` extension, format identifier, schema version, `next_id`, records.
- Round trip every record type and datetime.
- Validate before returning a new manager.
- Cover missing file, invalid JSON/schema/version/type/date, duplicate IDs, and wrong extension.
- Use `tempfile.TemporaryDirectory` in tests.

### Task 6 - CLI and entry point

Support the exact approved commands for help, create, list, show, update, delete, search, save, load, and exit.

- CLI handles strings and presentation only.
- Inject input/output functions for tests.
- Convert errors to useful messages and continue.
- Replace the active manager only after successful load.
- `main.py` only creates and starts the CLI.

### Task 7 - Acceptance tests and cleanup

- Add an automated path for every US1-US11.
- Add invalid-input recovery paths.
- Check no third-party imports exist in `src`.
- Remove scaffolding placeholder output and dead code.
- Update README run/test commands to the commands actually verified.

## Required final verification

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
python -m compileall -q src tests
git diff --check
rg -n "eval\(|TODO|TBD|PLACEHOLDER" src tests
rg -n "^\s*(from|import)\s+" src tests
```

Also run one scripted or manual CLI session covering create, list, compound search, update, delete, save, restart/load, and display restored data.

## Gate G3

- US1-US11 work through the final CLI.
- Model tests are automatically executable and green.
- Model package is independent from terminal and file I/O.
- Source has no third-party runtime dependency.
- Errors preserve data and return to the prompt.
- A focused implementation branch/PR contains real test evidence.

## Copy-ready prompt

```text
在 D:\comp3211\COMP3211-PIM 执行 WP03。先读取 master plan、WP03、冻结的decisions、SRS、TECHNICAL_CONTRACT和Design初稿。使用 test-driven-development，严格按记录类型→Manager CRUD→纯搜索→搜索接入→.pim持久化→CLI→验收测试的顺序，由一个主Agent完成，禁止多个编码Agent同时修改仓库。每项行为先运行失败测试，再做最小实现并运行目标测试和全套测试。只使用Python标准库，不用eval，model中不得有文件或终端I/O。完成WP03所有真实验证，通过G3后提交、推送并创建PR，报告测试数量、真实结果、commit和风险。
```
