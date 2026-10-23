# Usability and synchronized release implementation plan

**Goal:** Retain the PIM mainline and add the peer's unsaved-load protection, focused help and positioned diagnostics, then rebuild and verify the submission candidate.

**Architecture:** The controller owns a conservative dirty flag: successful create/update/delete marks dirty, successful save/load clears it, failed operations preserve it. A dirty load is rejected unless the final argument is `force=true`; `force=false` is accepted and keeps protection. Exit/EOF warn and terminate without implicit saving, as in the peer. `help [COMMAND]` uses one command catalogue for syntax/examples/recovery hints. Search keeps iterative parsing/evaluation and attaches one-based expression character positions to errors. Quoted command-argument errors use positions in the command line. Model record types, IDs and snapshot format stay unchanged.

**Tech stack:** Python standard library; unittest; existing Markdown/PDF renderer and editable PPTX workflow; ZIP/hash validation.

## Execution

1. Add failing controller and model tests for dirty state, failure preservation, force option parsing, help topics and lexical/syntactic/semantic search positions.
2. Implement the controller catalogue/state and model error locations; adapt existing load tests to explicitly discard unsaved changes where intended. Retain their original validation/state assertions.
3. Add current SRS requirements FR-51–FR-54 and update FR-24/25/44/46/49, catalogue, design, contract, manuals, traceability, demo and recording assets.
4. Verify all tests, model-only and full model coverage on Python 3.11.9/3.12.3/3.13.5. Exercise -S and both evidence tools. Request independent code review and resolve reproducible findings.
5. Rebuild six required document PDFs; refresh presentation evidence and notes/PDF. Render and inspect all final pages/slides. Update the packager to include current evidence and demo-tool inputs without hardcoded obsolete counts.
6. Build a new uniquely named candidate, verify archive CRC and hashes, extract into a new directory, rerun tests/tools across supported versions, and write current/versioned manifests with final verification. Preserve old candidates and accurately identify the still-missing real recordings/declaration.

## Compatibility decisions

Dirty-load rejection intentionally replaces silent loss of unsaved data. Explicit `force=true` restores the former replacement behavior. Save still requires a path. No new exit confirmation loop, autosave, multi-field update, named criteria, data migration or mandatory new model fields. Detailed help is optional; bare help retains the overview. Character positions count Unicode code points, not display columns; EOF is length plus one. Source package includes the same demo fixtures used by tests.

## Completion evidence

All six execution steps completed on 2026-10-23. See `docs/reports/usability-release-2026-10-23.md`, the current candidate manifest and `usability-clean-extraction-2026-10-23.txt`. The checked ZIP preserves old candidates and passes all three interpreter runs from a new extraction. Real recordings, member data and declaration remain explicit human deliverables.
