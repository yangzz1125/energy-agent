# Energy Agent

能源场景 Agent 学习项目。V0 目标是通过命令行提问，让模型调用负荷数据读取、统计和画图工具，并记录执行过程。

## 阅读入口

| 目的 | 入口 |
| --- | --- |
| 第一次运行与代码关系 | [项目导航](docs/README.md) |
| 查看模拟负荷 | [数据说明](data/README.md) |
| 继续开发 | [项目约定](AGENTS.md) |

## 当前进度

- 已使用 uv 初始化 Python 3.12 项目，创建虚拟环境和本地 Git 仓库。
- 已准备 168 条模拟负荷数据，详见 [数据说明](data/README.md)。
- 已添加 Responses API 连通性测试程序；工具调用循环尚未实现。
- 已实现 `get_load_stats(date)`，按日期查询负荷统计，尚未接入模型。
- 已配置 ruff 和 pytest，`get_load_stats` 有 3 个单元测试。

## 开发检查

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

测试只读取本地数据，不调用模型接口。Codex 和 Claude Code 共用的项目约定写在 `AGENTS.md`，`CLAUDE.md` 通过 `@AGENTS.md` 引用它。

## 负荷统计工具

在项目目录运行：

```powershell
uv run python -c "from tools.load_tools import get_load_stats; print(get_load_stats('2026-09-21'))"
```

输入日期格式为 `YYYY-MM-DD`，数据固定读取 `data/load_sample.csv`。返回日期、单位、最大值、最小值、平均值和峰谷差；该日期无数据时返回包含 `error` 的字典。

## 运行 API 测试

在项目目录执行 `uv sync` 安装锁定的依赖，在 `.env` 中填写模型配置，然后运行：

```powershell
uv run python -m scripts.check_api
```

程序发送一次请求，预期输出 `API_OK`、模型名称、耗时和 Token 用量。测试会产生少量 API 调用费用；失败时以非零退出码结束。

## 模型接口

- 使用 OpenAI Responses API 格式，通过 OpenAI Python SDK 的 `client.responses.create(...)` 调用 DeepSeek 模型。
- `.env` 中配置 `MODEL_BASE_URL`、`MODEL_API_KEY` 和 `MODEL_NAME`，由 `config/model.py` 统一读取。具体模型名称以实际配置为准。
- 直连 DeepSeek 官方服务时，Base URL 为 `https://api.deepseek.com`。
- DeepSeek 的 Responses 接口无服务端会话存储；后续实现需在客户端保存历史，每轮通过 `input` 回传，不能依赖 `previous_response_id`。
- 工具调用使用 `function`，由本地 Python 执行工具并回传结果。

兼容性依据：[DeepSeek Responses API 官方说明](https://api-docs.deepseek.com/guides/responses_api/)。

## 目录

- `data/`：练习数据及其说明。
- `config/`：模型配置读取，实际密钥保存在根目录 `.env` 中。
- `tools/`：供 Agent 调用的工具函数，`load_tools.py` 实现负荷统计。
- `scripts/check_api.py`：Responses API 连通性测试。
- `tests/`：pytest 单元测试。
- `AGENTS.md`、`CLAUDE.md`：给 AI 编程工具的项目约定。
- `pyproject.toml`、`uv.lock`：项目配置与依赖锁定文件。
- `.env`：本地模型配置，已加入 Git 忽略规则。
- `.venv/`：由 uv 创建的虚拟环境，已加入 Git 忽略规则。
