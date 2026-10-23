# COMP3211 第 89 组｜四人分工表

**组会日期：2026-10-23。A：________　B：________　C：________　D：________**

共同目标：在已经完成的 AI 辅助候选版上复核、改进和完成录制。每个人对自己的部分负责，并能说明为什么这样做；不用为了“有改动”而重写已经正确的内容。

**统一版本：** `output/COMP3211_Group_Project-review-2026-10-23.zip`。解压后可直接看到 `01_SRS`、`02_Design`、`03_Implementation`、`05_Presentation`。下表未标“仓库”的路径均相对这个解压目录。脚本、Markdown、图源和可编辑 PPTX 需从完整项目仓库取得，不在候选 ZIP 中。开始前由 B 确保四人都拿到这些资料。

当前基础：45 项测试已在 Python 3.11.9、3.12.3、3.13.5 通过；Python 3.13.5 下模型行覆盖率 416/430（96.74%）。这是已有实测结果，各人仍需完成自己的复核。NFR-01 的特定断网/无图形会话环境仍未验证。

| 人员与主责 | 先看哪些文件 | 重点改进什么 | 最后交付与复核人 |
|---|---|---|---|
| A｜需求与一致性 | 01_SRS/SRS.pdf<br>03_Implementation/Requirements_Coverage.pdf<br>03_Implementation/User_Manual.pdf<br>另看官方 Project Description 的 Appendix B<br>Lecture 04 第 27、31-32 页 | 核对 11 条用户故事是否完整，需求是否明确、可验证。<br>重点确认：提醒时间只存数据、退出不自动保存、时间格式与搜索规则。<br>用真实操作核对 SRS、手册和覆盖表；发现矛盾时给出输入及期待结果。 | 一份确认或修订后的 SRS、需求覆盖表。<br>一份问题清单：需求编号、例子、建议改法；没有问题可明确写“已核对”。<br>汇总真实姓名、学号及声明所需资料，交全组确认。<br>交叉复核：C 检查需求能否照着操作。 |
| B｜设计与代码 | 02_Design/Design_Document.pdf<br>03_Implementation/src/main.py<br>src/model/manager.py、search.py<br>src/controller/cli.py<br>src/storage/pim_file.py<br>上述 src/ 均在 03_Implementation 内 | 对照代码核对三类图的模块、箭头、接口和异常。<br>讲清“搜索后修改”“加载失败为何不破坏数据”。<br>审阅架构取舍和职责划分；只改有具体理由的问题。 | 一份确认或修订后的设计文档及对应图源。<br>能向其他成员讲清一次正常流程和一次错误流程。<br>若需改代码，记录关联需求，并交 D 加测、C 实测。<br>负责最终文件整合；D 复核代码与图，C 复核解压包。 |
| C｜独立试用与演示 | 03_Implementation/Developer_Manual.pdf<br>03_Implementation/User_Manual.pdf<br>03_Implementation/README.md<br>仓库 media/demo/demo-script.md<br>demo-commands.txt、demo-expected-output.txt<br>media/demo/demo-checklist.md | 在自己的电脑上只按手册启动，不依赖作者口头补充。<br>完成四类记录、组合搜索、修改、删除、保存、退出及新进程加载。<br>记录错误日期、损坏文件等异常；检查命令、输出和手册一致。 | 一次独立运行记录：系统/Python 版本、步骤、结果、问题。<br>两份手册的确认意见或具体修订。<br>真实 System_Demo.mp4，实测不超过 4 分钟。<br>交叉复核：A 检查演示覆盖功能及手册可读性。 |
| D｜测试与汇报 | 03_Implementation/tests/model/<br>tests/controller/、tests/storage/<br>03_Implementation/tools/model_coverage.py<br>03_Implementation/Test_Coverage.pdf<br>05_Presentation/Presentation.pdf<br>仓库 media/presentation/ 内讲稿与检查表 | 运行全部 45 项测试；理解新增字段修改、时间边界、真假组合和文件校验断言。<br>复核报告数据和口径，不能把模型行覆盖率说成全项目覆盖率。<br>整合幻灯片，组织四人试讲、计时和录制；经历描述符合实际 AI 辅助过程。 | 测试与覆盖率运行记录、确认或修订后的覆盖报告。<br>最终演讲 PDF、可编辑 PPTX、四人确认的讲稿。<br>组织完成 Presentation_Recording.mp4；四人各自负责发言和露脸。<br>交叉复核：B 检查测试证据，四人共同回看录像。 |

## 修改原稿的位置

下面的路径相对完整仓库 `COMP3211-PIM`；改原稿后重新导出 PDF，并同步到提交包。

| 人员 | 可编辑源文件 |
|---|---|
| A | docs/srs/SRS.md；docs/srs/requirements-catalog.csv；docs/reports/Requirements_Coverage.md |
| B | docs/design/Design_Document.md；docs/design/diagrams/*.mmd；程序源文件 src/ |
| C | docs/manuals/Developer_Manual.md、User_Manual.md；media/demo/；submission/release-README.md |
| D | tests/；docs/reports/Test_Coverage.md；artifacts/presentation/Presentation.pptx；media/presentation/ |

## 四人汇报怎么安排

先沿用现成讲稿，复核主责与发言内容可以不同：A 讲第 1-2 页（介绍与创建 PIR）；B 讲第 3 页（定义搜索条件）；C 讲第 4 页（搜索结果与后续操作）；D 讲第 5-6 页（架构与测试经验），B 协助 D 理解设计。D 的段落内容较多，可精简或经全组同意重新分配，之后同步讲稿。

- 每人实际发言至少 1 分钟，建议先按 65-70 秒准备；完整汇报视频最多 5 分钟，需给学生证展示和切换留时间。
- 每个人开始自己的部分时展示本人学生证和脸，发言期间脸持续可见。四人都参加，D 只是协调人。
- 两个视频分别提交：系统演示 MP4 ≤4 分钟；四人汇报 MP4 ≤5 分钟。最终以导出文件的实测时长和回看结果为准。

## 时间与完成标准

| 时间节点 | 应完成什么 |
|---|---|
| 今天组会结束前 | 填好 A/B/C/D 的姓名；每人确认负责文件和首轮交付时间；确定统一版本、录制日期及最终上传人。 |
| 会后两天内（建议） | 每人提交首轮问题/认可记录。所有问题写明文件页码或代码位置、实际结果、期待结果和建议；没有问题也记录核对范围。 |
| 录制前 | 合并已确认修改，重跑测试与覆盖率，同步相关 PDF/幻灯片；四人试讲并测量各自时长。 |
| 正式提交前 | B 整合最终 ZIP，C 在全新解压目录复测，A 核对材料齐全和声明位置，D 检查报告与录像；全组确认后由会上指定的人上传并保存回执。 |

“完成”意味着有可查看的文件或操作记录，并由表中复核人确认；只说“看过了”不算。修改功能规则时先全组确认，再同步 SRS、代码、测试、手册和演示，避免文件互相矛盾。

## 共同收尾

1. A 汇总官方 Honour Declaration 和成员资料；四人共同确认真实贡献比例、AI 使用说明及所需签署。比例合计 100%，不能由 A/B/C/D 标签自动推定均分。AI 记录见 `submission/ai-use-log.md`。
2. B 整合一个 ZIP；需求覆盖报告和测试覆盖率报告放在 `03_Implementation` 根目录，官方声明放在 ZIP 根目录，加入两段正式 MP4。详细步骤见 `submission/human-closeout-checklist.md`。
3. 官方提交截止：**2026-11-20（周五）20:00**。建议至少提前一天完成最终检查；以下内部时间由今天组会填写。

首轮复核完成：________　统一录制：________　最终包检查：________　上传负责人：________

问题记录格式：负责人｜文件/页码/命令｜实际结果｜期待结果或建议｜处理人/期限｜复核结论。

本表是建议分工，等待组员填写姓名和内部日期；不代表已完成真人复核、录像、声明或上传。
