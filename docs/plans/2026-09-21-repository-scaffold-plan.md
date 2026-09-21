# Repository Scaffold Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create and publish a private, collaboration-ready repository containing the complete folder structure and templates for the COMP3211 PIM project.

**Architecture:** Keep application code in `src`, model tests in `tests`, editable deliverable sources in `docs`, recording material in `media`, and final assembly instructions in `submission`. Use feature branches and pull requests for group collaboration.

**Tech Stack:** Git, GitHub, Python standard library, Markdown, PDF and MP4 final artifacts.

---

### Task 1: Create the repository control files

**Files:**
- Create: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `.gitignore`
- Create: `.gitattributes`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

1. Add the project overview and quick-start instructions.
2. Add the feature-branch and pull-request workflow.
3. Add Python, IDE, coverage, local data, and large-video ignore rules.
4. Verify every file is tracked with `git status --short`.

### Task 2: Create project management files

**Files:**
- Create: `requirements-checklist.md`
- Create: `decisions.md`
- Create: `tasks.md`

1. Transcribe US1-US11 into a checkable list.
2. Record confirmed technical decisions and unresolved team choices.
3. Add milestone and ownership tables.

### Task 3: Create source and test structure

**Files:**
- Create: `src/main.py`
- Create: `src/model/__init__.py`
- Create: `src/controller/__init__.py`
- Create: `src/storage/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/model/__init__.py`
- Create: `tests/README.md`

1. Create importable packages without implementing PIM features.
2. Document the standard-library-only and model-testing constraints.
3. Run Python compilation to confirm the scaffold has no syntax errors.

### Task 4: Create deliverable templates

**Files:**
- Create: `docs/srs/SRS_TEMPLATE.md`
- Create: `docs/design/DESIGN_TEMPLATE.md`
- Create: `docs/manuals/DEVELOPER_MANUAL_TEMPLATE.md`
- Create: `docs/manuals/USER_MANUAL_TEMPLATE.md`
- Create: `docs/reports/REQUIREMENTS_COVERAGE_TEMPLATE.md`
- Create: `docs/reports/TEST_COVERAGE_TEMPLATE.md`
- Create: `docs/meeting-notes/MEETING_TEMPLATE.md`
- Create: `media/demo/README.md`
- Create: `media/presentation/README.md`
- Create: `submission/README.md`
- Create: `submission/honour-declaration/README.md`

1. Add the required headings and checklists to each template.
2. Mark final file types and time limits.
3. Verify that every official deliverable has a destination.

### Task 5: Commit and publish

1. Review `git diff --check` and `git status --short`.
2. Create the initial commit.
3. Create the private GitHub repository and push `main`.
4. Confirm the remote URL, visibility, default branch, and clean local status.
