# 输入流故障修正与验证记录

日期：2026-10-23。依据：对根目录 `suggestion_v3.md` 的审查及用户明确授权。

## 修改结果

- 在 `controller/cli.py` 的 `readline()` 边界捕获 OSError/UnicodeError，转换为专用致命异常 `InputReadError`，不会误进入可恢复的命令错误分支。
- 输入故障停止会话；顶层 `main.cli()` 向 stderr 尝试写入 `Error: IO: cannot read input: ...`，明确返回 1，不再把故障当作 EOF 或成功退出。
- 原有 diagnostics 提供长度限制与安全转义，非法 UTF-8、终端控制字符和超大错误信息均不造成 traceback 或错误刷屏。
- controller 持有 dirty 状态并尝试提示一次。提示失败不覆盖原始读取失败；不重试失效输入、不修改记录/计数器、不自动保存。
- 对失效的 stdout/stderr 管道执行尽力清理，避免解释器关闭时再次 flush 导致错误或改变退出码。普通命令恢复、Ctrl+C 的 130、正常 EOF/exit 的 0、一般输出管道关闭行为保持原有约定；无关编程异常仍然暴露。

## 回归测试

新增 7 个方法：

| 文件 | 新增方法数 | 验证内容 |
|---|---:|---|
| `tests/controller/test_input_failures.py` | 4 | 只读一次、保留状态与 dirty 标记、干净会话不警告、提示失败不掩盖原错误、无关 RuntimeError 继续传播 |
| `tests/test_input_failures.py` | 3 | 真实非法 UTF-8 stdin、dirty 后 I/O/解码错误、ASCII stderr 长度与转义、stdout/stderr 单独或同时失效仍退出 1 |

现有 `test_input_error_is_not_mistaken_for_a_closed_output_pipe` 加强为同时断言退出 1、stderr 的 IO 分类和没有 traceback。原始代码上的新增进程检查已复现失败，修正后通过。故障注入局限在输入/输出边界，没有把普通命令错误改成致命错误。

## 实测结果

| Windows 环境 | 全套测试 | 全套对 model 行覆盖率 | 两个新进程的演示 |
|---|---:|---:|---|
| Python 3.11.9 | 112/112 | 488/488，100.00% | 完整输出匹配 |
| Python 3.12.14 | 112/112 | 488/488，100.00% | 完整输出匹配 |
| Python 3.13.0 | 112/112 | 488/488，100.00% | 完整输出匹配 |

3.11.9 的独立 model 单元测试为 37/37，487/488 行，99.80%；model 源码及这 37 个测试与上一轮 3.12/3.13 验证的内容没有变化。行覆盖率不代表全部分支与输入组合已覆盖。

- 本轮 15 个产品模块编译与 Python 3.11 语法检查通过；63 处导入引用仅包含本地模块与标准库，没有 model 对 controller/storage 的反向依赖。
- 日志：`input-io-coverage-2026-10-23-python311.txt`、`python312.txt`、`python313.txt`（相同前缀），及对应 `input-io-demo` 日志。每份日志包含解释器、参数和退出码。
- model-only 日志：`input-io-model-only-2026-10-23-python311.txt`。
- 审计：`input-io-import-audit-2026-10-23.txt`。
- 本轮源码、测试与工具哈希：`input-io-source-sha256-2026-10-23.json`。上一轮 `hardening-*` 记录保留为历史快照。

## Python 3.11 运行环境

为关闭上一轮的验证缺口，从 [Python 3.11.9 官方发布页](https://www.python.org/downloads/release/python-3119/) 下载 Windows 64 位 embeddable package，放在项目临时目录 `tmp/python311`。下载归档与官网发布的 MD5 `6d9aa08531d48fcc261ba667e2df17c4` 一致；SHA-256 与本地配置记录在 `input-io-python311-runtime-2026-10-23.json`。未安装到系统或修改注册表。

将该临时运行时的 `python311._pth` 改名为 `python311._pth.disabled`，使程序目录、PYTHONPATH 和 PYTHONIOENCODING 按普通命令行运行方式生效。标准库仍来自发行包自身，没有安装第三方包；该运行时用于兼容验证，不属于产品源码或发布包。

可在项目根目录复现：

```powershell
$env:PYTHONPATH = "$PWD\src"
$env:TEMP = "$PWD\tmp\hardening-tests"
$env:TMP = $env:TEMP
.\tmp\python311\python.exe -B tools/model_coverage.py
.\tmp\python311\python.exe -B tools/verify_demo.py
```

测试时使用可写的 `tmp/hardening-tests` 规避本机沙箱默认 TEMP 权限限制。3.12/3.13 的实际解释器路径见各自证据日志。

## 文档与交付范围

已同步 SRS FR-49、需求目录与追溯、决策、用户与开发手册、设计/技术契约、测试覆盖报告和 AI 使用记录。保留路径语法、完整字段输出及现有架构；没有实施 v3 中的可选大规模重构或容量限制。

PDF、演示文稿、ZIP 和旧候选 manifest 未重建。准备下一次候选包时应以当前 Markdown 和源码重新生成并检查交付物。本轮未委派其他代理，也不声称新增独立审查。
