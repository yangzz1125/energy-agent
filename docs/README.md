# Energy Agent 项目导航

能源场景 Agent 的学习工程，当前已实现按日期计算负荷统计。命令行工具调用循环是后续开发目标，现阶段可以独立运行统计函数和离线测试。

## 从这里开始

| 目的 | 入口 |
| --- | --- |
| 查看功能与运行说明 | [项目首页](../README.md) |
| 了解模拟负荷的字段与生成规则 | [数据说明](../data/README.md) |
| 阅读统计工具 | [tools/load_tools.py](../tools/load_tools.py) |
| 对照输入边界和预期结果 | [tests/test_load_tools.py](../tests/test_load_tools.py) |
| 继续开发 | [项目约定](../AGENTS.md) |

## 第一次运行

需要 Python 3.12 以上和 uv。以下命令均在仓库根目录执行：

```powershell
uv sync
uv run python -c "from tools.load_tools import get_load_stats; print(get_load_stats('2026-09-21'))"
```

返回日期、单位、最大值、最小值、平均值和峰谷差。这里读取的是仓库中的模拟数据，不需要模型密钥。

## 代码如何衔接

`data/load_sample.csv` → `tools/load_tools.py` → 统计结果字典。

`config/` 负责读取模型配置，`scripts/check_api.py` 用于验证模型连接；两者与离线负荷统计分开。模型调用的配置与协议说明见项目首页。

## 开发检查

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

这些检查不调用真实模型。API 连通性测试会发出实际请求并产生费用，按首页的“运行 API 测试”单独执行。
