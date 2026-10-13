"""负荷统计工具：读取本地 CSV，筛选指定日期，再计算统计值。

这里是普通的 Python 函数，不调用模型；后续由 Agent 根据模型的请求执行它。
"""

import csv  # Python 标准库，用于读取逗号分隔的表格文件。
from datetime import datetime
from pathlib import Path


def get_load_stats(date: str) -> dict:
    """查询指定日期的负荷统计。

    参数：date 是 YYYY-MM-DD 格式的字符串，例如 "2026-09-21"。
    返回：包含日期、单位、最大值、最小值、平均值和峰谷差的字典。
    无数据时：返回 {"date": date, "error": "该日期无数据"}。

    date: str 和 -> dict 是类型提示，帮助阅读和编辑器检查，
    Python 不会仅凭这些提示自动校验或转换传入的数据。
    """
    # strptime 按指定格式把字符串解析成 datetime 对象。
    # %Y、%m、%d 分别表示年、月、日；.date() 只保留日期部分。
    # 无法解析的日期会直接报 ValueError，不会被误当成“该日期无数据”。
    target_date = datetime.strptime(date, "%Y-%m-%d").date()

    # 从当前文件向上找到项目根目录，再定位固定的数据文件。
    # 文件路径由程序确定，因此调用者只需提供日期。
    csv_path = Path(__file__).resolve().parents[1] / "data" / "load_sample.csv"

    # loads 用来收集当天的负荷数值，最初是空列表。
    loads = []
    # with 会在代码块结束时自动关闭文件，包括代码块中发生异常的情况。
    # newline="" 将换行处理交给 csv 模块；utf-8-sig 可兼容文件开头的 BOM。
    with csv_path.open(encoding="utf-8-sig", newline="") as file:
        # DictReader 将表头作为键，每一行读取为字典，单元格值仍然是字符串。
        # 例如：{"timestamp": "2026/9/21 0:00", "load_mw": "52"}。
        for row in csv.DictReader(file):
            # CSV 内的时间格式与函数输入的日期格式不同，需要分别解析。
            # %H、%M 表示小时和分钟；比较时只取日期，就能选出当天所有小时。
            timestamp = datetime.strptime(row["timestamp"], "%Y/%m/%d %H:%M")
            if timestamp.date() == target_date:
                # float 将 "52" 转成 52.0，append 把这个数字追加到列表末尾。
                loads.append(float(row["load_mw"]))

    # 空列表在条件判断中为假，not loads 就表示没有找到当天的数据。
    # 提前返回后，下面的统计不会执行，避免对空列表求最大值或平均值。
    if not loads:
        return {"date": date, "error": "该日期无数据"}

    # max/min 是 Python 内置函数。先保存结果，计算峰谷差时可以直接复用。
    max_load = max(loads)
    min_load = min(loads)

    # 返回字典，方便后续转换成 JSON 回传给模型。
    # sum(loads) / len(loads) 是所有小时负荷的算术平均值。
    # 当前数据是等间隔的每小时平均负荷，因此这样计算可得到当天平均负荷。
    # round(..., 2) 将数值舍入到两位小数，但不保证显示时一定带两位小数。
    return {
        "date": date,
        "unit": "MW",
        "max": max_load,
        "min": min_load,
        "average": round(sum(loads) / len(loads), 2),
        "peak_valley_diff": round(max_load - min_load, 2),  # 峰谷差 = 最大值 - 最小值。
    }
