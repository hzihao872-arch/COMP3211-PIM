# COMP3211 PIM Repository Design

## Purpose

Create a private GitHub repository where the group can develop the 2026 COMP3211 command-line PIM project and prepare every required submission item in one place.

## Decisions

- Repository: `hzihao872-arch/COMP3211-PIM`
- Visibility: private
- Default branch: `main`
- Language baseline: Python, using only the standard library
- Application layout: `src/model`, `src/controller`, and `src/storage`
- Tests: Python `unittest`, with model tests under `tests/model`
- Documentation: editable Markdown templates under `docs`; final documents will be exported to PDF
- Collaboration: one feature branch per task, followed by a pull request into `main`
- Large recordings: keep instructions and scripts in Git; add final MP4 files during submission assembly rather than normal source commits

## Repository Areas

- Root project files explain the project, decisions, task status, and collaboration process.
- `src/` contains the application. The required `model` package stays separate from command handling and file I/O.
- `tests/` mirrors the model and other testable components.
- `docs/` contains templates for the SRS, design document, manuals, reports, and meeting notes.
- `media/` contains recording plans and final media placeholders.
- `submission/` contains the final ZIP checklist and Honour Declaration placeholder.

## Success Criteria

The repository can be cloned by another member, its purpose and workflow are clear from the README, every required deliverable has an obvious location, and the GitHub remote is private and up to date with the initial commit.
