# Energy Agent 项目约定

能源场景 Agent 学习项目，当前处于 V0：命令行提问，模型调用负荷数据工具（读取、统计、画图），记录完整执行过程。版本规划见上级目录的 `agent.md`。

## 命令

在项目根目录运行：

- 安装依赖：`uv sync`
- 测试：`uv run pytest`
- 检查与格式化：`uv run ruff check .`、`uv run ruff format .`
- API 连通性测试：`uv run python -m scripts.check_api`，会产生 DeepSeek 调用费用，未经用户同意不要运行。

完成一项改动后，先跑 `uv run ruff check .`、`uv run ruff format --check .` 和 `uv run pytest`，全部通过再交给用户审查。

## 目录

- `config/model.py`：从 `.env` 读取 `MODEL_BASE_URL`、`MODEL_API_KEY`、`MODEL_NAME`。
- `tools/`：供 Agent 调用的普通 Python 函数，每个工具配对应测试。
- `scripts/`：可单独运行的脚本，用 `python -m scripts.xxx` 启动。
- `tests/`：pytest 测试，`pyproject.toml` 已把项目根目录加入导入路径。
- `data/`：练习数据，字段和生成规则见 `data/README.md`。

## 模型接口

- 通过 OpenAI Python SDK 的 `client.responses.create(...)` 调用 DeepSeek（Responses API 格式）。
- DeepSeek 的 Responses 接口不在服务端保存会话，历史由客户端保存并每轮通过 `input` 回传，不使用 `previous_response_id`。
- 工具调用的循环逻辑由用户设计，实现时按用户给出的流程写，不引入 Agent 框架。

## 代码约定

- 这是学习项目：代码保持直接，注释用中文解释用途和非显然的原因，风格参照 `tools/load_tools.py`。
- 只在外部输入、文件和接口调用处校验；错误直接抛出，不写空 `except`，不在失败时返回默认值冒充成功。
- 测试不调用真实模型接口，需要模型响应时用假数据。
- 不提交 `.env`、密钥、`.venv/` 和缓存文件；不修改已有测试的期望值来让测试通过。
