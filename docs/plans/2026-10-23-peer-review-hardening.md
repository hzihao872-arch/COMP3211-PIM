# Peer comparison and terminal hardening plan

**Goal:** Compare the supplied COMP3211-DSV archive against Appendix B and strengthen the current PIM where reproducible defects or useful verification gaps exist.

**Architecture:** Preserve the model, command grammar, IDs and version-one snapshots. Escape terminal control characters at the controller output boundary, handle unsupported display characters without altering records, and handle process interrupts/closed pipes at the entry point. Keep reproducible evidence tools separate from runtime code.

**Tech stack:** Python 3.11–3.13 standard library, unittest, subprocess, trace.

## Tasks

1. Read both implementations and official requirements; run the existing suite. Distinguish required behavior from optional peer conventions.
2. Add `tests/controller/test_terminal.py` and `tests/test_process_boundaries.py`. Reproduce raw terminal controls, limited output encoding, interruption and closed-pipe failures before changing code.
3. Add a small output adapter in `src/controller/output.py`; use it in `CommandController.run`. Update `src/main.py` to handle process termination without masking unrelated I/O failures. Rerun focused and full tests.
4. Add portable `tools/verify_demo.py` and `tools/benchmark.py` using temporary directories and correctness checks. Exercise the two-session demo in real subprocesses and measure a mixed 1,000-record dataset; report observations, not a new performance requirement.
5. Update manuals/design/requirements notes and AI-use log. Record the comparison decisions and fresh test/coverage/evidence logs. Run on the three previously supported interpreters and check the diff. Clearly distinguish changed source from the historical packaged release.

## Decisions

Directly replacing our implementation would break documented commands and existing snapshots. Adding every optional peer feature would change the agreed SRS without evidence that it improves required coverage. Targeted corrections and reproducible evidence preserve the current contract and address observed weaknesses.

The peer's note title, field-assignment syntax, timestamp metadata, regional phone validation, multi-field update, optional script mode and unsaved-change protection are not Appendix B requirements. Retain our existing choices; document the trade-offs and the fact that the two `.pim` schemas are incompatible despite their common format name.

## Verification commands

From the repository root with `PYTHONPATH` pointing to `src`:

```text
python -m unittest tests.controller.test_terminal tests.test_process_boundaries -v
python -m unittest discover -s tests -t . -v
python tools/model_coverage.py
python tools/verify_demo.py
python tools/benchmark.py
```

Completion means observed passes, saved evidence, consistent source documentation, and an explicit statement of any remaining packaging/human deliverables. Do not claim an old release ZIP contains this revision.

## Completion evidence

- Comparison and four terminal corrections completed; independent review's Windows input-error finding reproduced and corrected at the output boundary.
- 64 tests passed on Python 3.11.9/3.12.3/3.13.5, and on 3.11.9 with `-S`; each interpreter measured 416/421 model source lines.
- Both portable evidence tools passed on all three runtimes; wrong transcript/command tests reject false passes.
- Source documentation and AI-use log updated; old release ZIP/PDF explicitly identified as predating these changes. No merge, push or release assembly performed.
- Detailed decisions and raw-log references: `docs/reports/peer-comparison-2026-10-23.md`.
