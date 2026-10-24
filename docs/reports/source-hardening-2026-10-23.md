# COMP3211-PIM 源码修改与验证记录

本记录为上一轮 105 项测试的历史快照；当前输入流修正与最新验证见 [输入流修正报告](input-io-fix-2026-10-23.md)。

日期：2026-10-23。依据：根目录 `suggestion_v2.md`。本次直接修改源码与 Markdown 配套文档；未发布、提交或重新打包候选版本。

## 1. 已实施

| 项目 | 修改位置 | 行为 |
|---|---|---|
| ID 完整边界 | `model/schema.py`、`validation.py`、`manager.py`、CLI/storage | 记录 ID 为 1..9999999999999999999；计数器额外允许 10000000000000000000 作为可保存/加载的耗尽标记。耗尽检查在修改前执行。旧文件中过大的 ID/计数器现在受控拒绝。 |
| 错误尺寸 | `model/diagnostics.py`、`errors.py`，相关调用位置 | 用户输入片段不超过 80 个可见 ASCII 字符，详情不超过 1024；不为报告错误而转换超大整数。控制/Unicode 字符显式转义，搜索位置保留。正常字段显示不截断。 |
| 加载定位 | `manager.from_rows`、`storage/pim_file.py` | 格式错误含有限长度的文件上下文，逐记录错误额外包含 `record #N`；根结构/计数器错误不伪造记录序号。 |
| 公共字段定义 | `model/schema.py`、manager/storage/search/controller/help | 字段顺序与时间/文本字段集合共用，schema 映射只读；帮助总览与详细说明集中在 help 模块。 |
| 死代码清理 | `model/search.py`、设计文档 | 删除没有调用的 `_accept`。 |
| 预期异常 | `PIMError`、controller/storage | 公共基类携带分类并限制详情；CLI 统一捕获。原有类别保留，未细分的新预期子类使用 `APPLICATION`；不吞掉一般编程异常。 |
| BOM | `storage/pim_file.py` | 加载接受带或不带 BOM 的 UTF-8；保存不写 BOM；无效 UTF-8 仍拒绝。 |
| 保存同步 | `storage/pim_file.py`、benchmark | 临时文件 flush、fsync、关闭后再原子替换；同步失败保留原文件、内存与 dirty 状态，并清理临时文件。没有新增跨平台完整掉电保证。 |
| Ctrl+C | `controller/cli.py`、`main.py` | dirty 会话尝试提示一次后退出 130；警告输出遇到管道关闭时仍保持退出 130，避免解释器再次 flush 的错误。 |

现有引号转义规则、literal `~` 路径、list/search 完整首字段、show 完整详情、搜索优先级与 model 独立性保持不变。未实施 Command 框架、独立 view 包、索引和覆盖率算法替换。

## 2. 验证结果

| 环境 | 全套测试 | model 单元测试 | 全套对 model 行覆盖率 | model 单元测试自身行覆盖率 | 演示 | benchmark |
|---|---:|---:|---:|---:|---|---|
| Windows / Python 3.12.14 | 105/105 | 37/37 | 488/488，100.00% | 487/488，99.80% | 两个新进程的完整输出匹配 | 1,000 条混合记录、5 轮通过 |
| Windows / Python 3.13.0 | 105/105 | 37/37 | 488/488，100.00% | 487/488，99.80% | 两个新进程的完整输出匹配 | 1,000 条混合记录、5 轮通过 |

新增 19 个测试方法，保留原 86 个；其中新 model 方法 5 个、storage 6 个、controller 7 个、进程边界 1 个。每个解释器的全套 coverage 运行包含了完整测试执行，日志有实际可执行文件、版本、参数与退出码。

- model 单独运行漏掉的是 `manager.py:18` 的非法类型分支；全套测试覆盖该分支。
- 15 个产品模块完成编译检查及 Python 3.11 语法解析检查；62 处导入引用未发现第三方依赖或 model 对 controller/storage 的反向导入。
- Python 3.11 未提供实际运行环境，因此本次不声称已重新验证 3.11；旧版本日志仅适用于旧候选包。
- 行覆盖率不代表完整分支覆盖或所有输入正确；本次没有额外委派独立审查。

完整证据见同目录 `hardening-coverage`、`hardening-model-only`、`hardening-demo`、`hardening-benchmark`（日期 `2026-10-23`，后缀 `python312`/`python313`）和 `hardening-import-audit-2026-10-23.txt`。[测试覆盖报告](Test_Coverage.md)给出复现命令和逐模块数据。`hardening-source-sha256-2026-10-23.json` 标识本次源码、测试与工具，不是发布包 manifest。

## 3. 文档与交付范围

已同步决策、SRS 与需求目录、需求覆盖映射、技术契约、设计文档、用户/开发手册、测试说明、README 和 AI 使用记录。ID 范围、错误展示、BOM、保存同步与中断行为均有说明；SRS 与 CSV 的条目文本已作一致性检查。

现有 PDF、演示文稿、ZIP 和旧候选包 manifest 保留为历史交付物，未重新生成。准备下一次正式候选包时应根据当前 Markdown 导出并检查 PDF，更新包内源码、测试、报告和哈希，并补做 Python 3.11 实测。录制、声明及真实小组信息仍按原清单处理。
