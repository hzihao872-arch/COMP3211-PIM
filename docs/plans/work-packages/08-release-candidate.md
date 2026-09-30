# WP08 - Release Candidate and ZIP Assembly

## Purpose

Build a clean submission directory from verified artifacts, prove that it reproduces on extraction, and clearly separate Agent-complete work from the remaining human video/declaration inputs.

## Dependencies

Gate G7 passed.

## Read first

- `docs/plans/deliverables-matrix.md`
- `docs/reports/code-freeze.md`
- `docs/reports/final-audit-resolution.md`
- All final artifacts
- Official Honour Declaration instructions

## Files to create

```text
submission/manifest.md
submission/ai-use-log.md
submission/human-closeout-checklist.md
output/COMP3211_Group_Project/
```

The `output` directory is intentionally ignored by Git. The manifest and checklists are committed; the assembled binaries remain local release output.

## Assembly layout

```text
output/COMP3211_Group_Project/
├─ 01_SRS/SRS.pdf
├─ 02_Design/Design_Document.pdf
├─ 03_Implementation/
│  ├─ src/
│  ├─ tests/
│  ├─ tools/
│  ├─ README.md
│  ├─ Developer_Manual.pdf
│  ├─ User_Manual.pdf
│  ├─ Requirements_Coverage.pdf
│  └─ Test_Coverage.pdf
├─ 04_Demo/System_Demo.mp4
├─ 05_Presentation/
│  ├─ Presentation.pdf
│  └─ Presentation_Recording.mp4
└─ Honour_Declaration_for_Group_Project.pdf
```

`03_Implementation` is the source-code root, so the two coverage reports are in the required root location.

## Pre-video release candidate

Before the human recordings and signed declaration exist:

- assemble every available file;
- do not create fake MP4/PDF placeholders with final filenames;
- mark the three missing human artifacts in `human-closeout-checklist.md`;
- do not call the incomplete directory or ZIP final.

## Reproduction check

Copy the assembled implementation to a new temporary directory and follow only the Developer Manual:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
python tools/model_coverage.py
python src/main.py
```

Run the User Manual's principal workflow. Open/render all PDFs. Search the release tree for cache files, virtual environments, secrets, personal absolute paths, `TODO`, `TBD`, and stale placeholders.

## Manifest

For every artifact record:

| Relative path | Requirement | Source commit/version | SHA-256 | Verified by |
|---|---|---|---|---|

Do not mark human artifacts verified until they exist and are checked.

## Human closeout

After the group supplies the real files:

- insert `System_Demo.mp4` and verify duration at most 4 minutes;
- insert `Presentation_Recording.mp4` and verify duration at most 5 minutes;
- confirm each member's one-minute speaking allocation and identity/face rules by human review;
- insert the official signed Honour Declaration at ZIP root;
- verify real member data, contributions totaling 100%, and GenAI disclosure;
- recompute manifest hashes;
- repeat the clean extraction check;
- create the final ZIP and open it once more before upload.

## Gate G8

Before human closeout:

- all Agent-producible artifacts are assembled and verified;
- exactly the human artifacts are listed as missing;
- implementation reproduces from the release directory;
- manifest and AI-use log are current.

Final-ready status requires the human closeout checks as well.

## Copy-ready prompt

```text
在 D:\comp3211\COMP3211-PIM 执行 WP08。读取 master plan、WP08、交付物矩阵、code-freeze、final-audit-resolution和全部最终材料。组装干净的 output/COMP3211_Group_Project，确保03_Implementation就是源码根目录，两份coverage报告位于其根部。没有真实视频或正式签署声明时不要生成假文件，也不要称为最终ZIP；在human-closeout-checklist中准确列出缺项。对实现做全新目录复现，打开/渲染所有PDF，生成manifest和SHA-256，检查缓存、密钥、绝对路径和占位符。通过G8后提交清单类文件、推送并创建PR，报告本地release candidate路径和剩余人工事项。
```
