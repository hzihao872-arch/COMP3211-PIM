# 独立实现审查：2026-10-23

本审查从 `D:\comp3211\COMP3211-PIM` 当前工作目录出发，先查看 `git status`、`git diff -- src tests`，保留原有未提交文档和三份 `test_requirement_edges.py` 新文件。未 reset、clean 或切换至旧副本。完整阅读原始课程要求的四页提取文本（`Project Description - 2026.pdf`），逐个审查 `src/model/`、`src/controller/cli.py`、`src/storage/pim_file.py`、`src/main.py` 与现有测试；以前的审查通过记录没有代替本次执行证据。

## 发现与修复

### P1：深层 JSON 可在 Python 3.11 终止整个命令会话

- **依据**：课程第 2 页实现评分要求包括错误处理和可靠性；US11 要求加载已存记录。本组 FR-44/47/49 另承诺完整文件验证、失败保留原状态、错误后返回提示符。具体错误分类是本组约定，不是新增教师要求。
- **复现**：将 `"[" * 2000 + "0" + "]" * 2000` 写入 `nested.pim`，在有记录的会话中执行 `load "nested.pim"`。Python 3.11.9 的 `json.loads` 抛出 `RecursionError: maximum recursion depth exceeded while decoding a JSON array from a unicode string`，旧 `load_pim` 未捕获，错误穿过控制器。后续 `show`/`add` 无法执行，未保存记录随进程退出而失去继续操作的机会。
- **版本差异**：同一 2000 层样本在本机 Python 3.12.3/3.13.5 中能被 JSON 解码器读取，再由根对象 schema 验证正常拒绝。因此“在 3.13 通过”不能证明 3.11 的异常分支安全。
- **根因与最小修复**：`src/storage/pim_file.py` 的加载验证异常元组增加 `RecursionError`，统一转换为 `PersistenceError("FORMAT", ...)`。未改变合法文件结构、ID 分配规则或模型行为。
- **有效回归**：新增 `tests/storage/test_independent_review.py` 两项测试，分别要求存储 API 的错误类别为 FORMAT，以及控制器继续 `show 1`、`add note after`，保留同一个 manager、原记录对象，并正确分配 ID 2。修复前 Python 3.11.9 两项均因未捕获 RecursionError 报错；修复后两项均通过。
- **本机过程证据**：`D:\comp3211\tmp\independent-review\storage-red311.txt`、`storage-green311.txt`。这些是审查工作文件，候选提交包不依赖此私人路径；上面的测试可直接在交付项目中复现验证。

### P2：等待输入之前未刷新提示符

- **依据**：课程要求命令行 PIM；本组用户手册承诺显示 `pim> ` 后等待命令，FR-49 承诺错误后回到提示符。可见的提示符是基本交互可用性要求。
- **复现**：把控制器输出接到标准库 `io.TextIOWrapper(io.BytesIO(), encoding="utf-8", line_buffering=True)`，在输入流每次 `readline()` 之前检查底层字节。旧代码的 `write("pim> ")` 没有换行，提示仍在文本缓冲区中，断言失败。
- **根因与最小修复**：`src/controller/cli.py` 的 `CommandController.run` 在提示符 write 后立即调用 `output_stream.flush()`，再读取输入。所有输出文字和命令语义保持一致。
- **有效回归**：新增 `tests/controller/test_independent_review.py` 一项测试，检查初始提示、错误后提示和成功创建后提示都在输入边界可见。使用真实的 Python 缓冲流，不用只记录 flush 调用次数的 mock。修复前 FAIL，修复后通过。
- **附加真实进程验证**：使用普通 `subprocess.Popen` 启动 `src/main.py`（没有 `-u`），在发送任何输入之前读到 `b'pim> '`；然后输入创建和退出命令，进程退出码 0、stderr 为空，输出包含 `Created note 1`。
- **本机过程证据**：`D:\comp3211\tmp\independent-review\prompt-red.txt`、`prompt-green.txt`。

### P3：复杂布尔组合需要更能区分优先级的断言

现有测试已有基础真值表和几条优先级例子。本次新增 `tests/model/test_independent_review.py`，用 Python 布尔运算作为独立的真值判据，对六个三原子表达式各验证全部八种赋值，共 48 个子情景，覆盖 `a || b && c` 与 `(a || b) && c`、原子否定、组否定、双重否定及嵌套组合。新增测试在原有模型实现上通过，没有据此修改已正确的搜索实现。它提升的是断言区分能力，而非只增加执行次数或覆盖率。

## 逐项检查结果与边界

| 范围 | 本次核查与结果 |
|---|---|
| US1–US5 四类 PIR | 构造、必需字段、不可变记录、类型属性、手机号文本保留与对应测试逐项检查；运行通过。 |
| US6/US8/US9 CRUD | 全部九个可修改数据字段、show 的所有字段、删除、非法/不存在 ID、失败更新不改变对象与计数器；运行通过。 |
| US7 搜索 | 五种文本字段、三种时间字段的 `<`/`>`/`=`、缺失字段为 false、否定、优先级、括号、全部输入解析和深度表达式测试；运行通过。 |
| 时间与输入验证 | 检查日期解析和完整格式回写验证；边界测试含闰日、跨日/月/年、历史时间、alarm 在 start 之后。另实际检查年份 0001、0099、0999、1000、9999 的解析/格式化往返，在文档所述 Windows 环境均通过。 |
| ID 与失败原子性 | 验证失败创建不消耗 ID、删除后不复用、载入取旧会话/file 较大 next ID、更新使用验证后的不可变替代对象、载入完整临时 manager 后才切换。合法文件未发现 ID 错误。 |
| US10/US11 文件 | 四类字段往返、根与记录 schema、重复 JSON 键、UTF-8、版本、布尔伪整数、重复/无序 ID、临时文件替换和失败清理测试运行通过；深层 JSON 异常已修复。 |
| 命令解析与恢复 | 引号、转义、大小写、空结果、EOF、超长 ID、错误类别和下一条命令恢复；运行通过。提示刷新问题已修复。 |
| model 包边界 | 数据类、纯验证、ID/集合规则、快照行的领域验证和完整查询语法/求值在 `model`；控制器只负责命令/呈现/协调；storage 负责 JSON、路径和文件替换。逐模块读取未发现模型依赖控制器或 I/O 的倒置引用。 |
| 标准库 | `src/` 所见导入均为本项目模块或 Python 标准库；本次修复没有增加依赖。 |

另用两种类型原子与 `! ( ) && ||` 枚举长度 1–6 的 137,256 个 token 序列，均得到正常求值或 `SearchSyntaxError`，未出现未预期异常。这只是解析鲁棒性探索，不代替真值断言，也不宣称穷尽全部输入。发现 FR-06 文本中“所有字段 trim”与严格时间格式之间有歧义，已通知需求审查者明确文本字段 trim、时间按 FR-07 验证；没有悄悄放宽程序的时间规则。

## 最终执行结果

实际核实解释器版本并执行同一命令：

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -t . -v
```

| 环境 | 本次全套结果 |
|---|---|
| Windows，Python 3.11.9 | 51 tests，OK |
| Windows，Python 3.12.3 | 51 tests，OK |
| Windows，Python 3.13.5 | 51 tests，OK |

51 项包含：model 25、controller 13、storage 7、真实进程 acceptance 4，以及主审查代理同期加入的覆盖率工具测试 2。本审查新增应用测试 4 项，原 45 项均保留。原始模型源文件没有变化，只有 controller 和 storage 各一处最小修复。覆盖率工具与统计结果由主审查独立处理，本报告不以通过数替代行覆盖率，也不把全套测试执行的模型行覆盖误写成仅模型单元测试的覆盖率。

完整本机运行记录位于 `D:\comp3211\tmp\independent-review\implementation-python311.txt`、`implementation-python312.txt`、`implementation-python313.txt`；最终候选包应使用主审查整理的交付内证据路径。此结果针对本次工作区，主审查仍需对最终打包后的干净解压目录重新验证。

## 仍需说明的限制

本次没有制造断网且无图形会话的精确环境，不能据此把 NFR-01 的该项实测标记为通过。没有验证磁盘断电时的持久化承诺，也没有添加该课程未要求的 GUI、网络服务或主动 alarm 通知。正式视频、成员身份/贡献确认与官方声明仍由真人完成。以上不妨碍本次能够由 AI 完成的代码修复和测试工作。

本报告、两处实现修复与四项新增测试均由 AI 协助产生，需纳入本组真实 AI 使用记录及最终人工复核。
