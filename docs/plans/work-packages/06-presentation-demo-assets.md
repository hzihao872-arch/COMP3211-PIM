# WP06 - Presentation and Recording Materials

## Purpose

Create the final Presentation PDF plus fully rehearsable scripts and data for the 4-minute system demo and 5-minute group presentation. The Agents do not impersonate students or fabricate the required MP4 recordings.

## Dependencies

Gate G5 passed. Group size is known; member names may remain clearly marked placeholders until supplied.

## Read first

- Final SRS and Design Document
- User and Developer Manuals
- Requirements and Test Coverage reports
- Frozen program
- Official presentation and video rules

## Files to create

```text
artifacts/presentation/Presentation.pptx
artifacts/presentation/Presentation.pdf
media/demo/demo-script.md
media/demo/demo-commands.txt
media/demo/demo-checklist.md
media/presentation/presentation-script.md
media/presentation/recording-checklist.md
```

## Parallel roles

- Slides/content Agent: creates the editable deck and PDF.
- Demo Agent: creates and executes the deterministic system-demo script.
- Speaker-script Agent: allocates the 5-minute presentation and identity/face checklist.

The primary Agent checks factual consistency and timing estimates. Actual durations are recorded only after a real timed rehearsal.

## Presentation content

The deck and script must cover:

1. One requirement concerning PIR creation.
2. One requirement concerning definition of a search criterion.
3. One requirement concerning searching for PIRs.
4. Overall architecture plus main code components.
5. One real lesson from requirements engineering, API design, or unit testing.

Use roughly 5-7 slides. Keep screenshots or short clips subordinate to the explanation.

## System demo script

The fixed command sequence should demonstrate:

- start;
- create representative PIRs;
- print one/all;
- define and execute a compound search;
- update a search result;
- delete a record;
- save `.pim`;
- start with a new session and load;
- print restored data.

Run every command against the freeze build and capture the actual expected output. Keep a short recovery note for likely recording mistakes.

## Presentation recording script

- Total target: about 4:30, with a hard maximum of 5:00.
- Each member receives at least 1:00 of speaking time.
- For four members, transitions must be very short.
- Opening checklist requires all members to show student ID cards and faces.
- The current speaker's face remains visible while speaking.

Do not invent names, IDs, or contribution claims. Use `MEMBER_A`, etc., until the group supplies them.

## Verification

- Render the PDF and inspect every slide.
- Check slide facts, diagrams, code names, and coverage numbers against final documents.
- Execute `demo-commands.txt` against the frozen program.
- Time a text rehearsal or read-through, labeling it an estimate until humans rehearse.
- Confirm the presentation script allocates at least 1 minute per real member.
- Run `git diff --check`.

## Gate G6

- Presentation PDF and editable source exist.
- Demo command sequence runs without improvisation.
- Both recording checklists include every official timing/identity rule.
- Only human names/IDs and actual rehearsal durations remain for the group.

## Copy-ready prompt

```text
在 D:\comp3211\COMP3211-PIM 执行 WP06。读取 master plan、WP06、六份最终文档和冻结程序。使用presentations技能创建可编辑Presentation和PDF；可用三个子Agent分别处理幻灯片、4分钟系统演示脚本、5分钟小组讲稿。系统演示命令必须在冻结程序上真实运行；幻灯片必须覆盖创建PIR、定义criterion、搜索PIR、整体设计和一个真实经验。不要编造姓名、学号或视频时长，使用明确占位符。逐页检查PDF并完成G6验证，提交、推送并创建PR。
```
