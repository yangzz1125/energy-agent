"""get_load_stats 的单元测试，只读取本地 CSV，不调用模型。

在项目根目录运行：uv run pytest
期望值来自 data/README.md 的生成规则，可以手算核对。
"""

import pytest

from tools.load_tools import get_load_stats


def test_weekday_stats():
    # 2026-09-21 是周一，倍数 1.00，统计值就是 24 小时基础曲线本身。
    # 基础曲线合计 1864 MW，1864 / 24 = 77.666...，舍入为 77.67。
    assert get_load_stats("2026-09-21") == {
        "date": "2026-09-21",
        "unit": "MW",
        "max": 113.0,
        "min": 46.0,
        "average": 77.67,
        "peak_valley_diff": 67.0,
    }


def test_date_without_data():
    # 数据只覆盖 2026-09-21 至 2026-09-27，范围外的日期返回 error。
    assert get_load_stats("2026-10-01") == {
        "date": "2026-10-01",
        "error": "该日期无数据",
    }


def test_invalid_date_format_raises():
    # 格式错误应直接报错，不能被当成“该日期无数据”。
    # pytest.raises 断言代码块内抛出指定异常，没抛出则测试失败。
    with pytest.raises(ValueError):
        get_load_stats("2026/09/21")
