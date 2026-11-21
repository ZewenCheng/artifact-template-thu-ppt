"""复算公开母版的教学序列。仅使用 Python 标准库。"""
import csv
import json
from pathlib import Path
from statistics import mean


def evaluate(series, window, first_target):
    """在共同的目标时点计算单步预测，窗口只读取目标之前的值。"""
    if not 1 <= window <= first_target < len(series):
        raise ValueError("窗口和首个目标索引必须处于序列范围内")
    results = []
    for index in range(first_target, len(series)):
        forecast = mean(series[index - window:index])
        error = abs(series[index] - forecast)
        results.append({"t": index + 1, "forecast": forecast, "error": error})
    return results


def summarize(points):
    errors = [point["error"] for point in points]
    return {"n": len(points), "mae": mean(errors), "max_error": max(errors)}


def main():
    source = Path(__file__).resolve().parents[1] / "assets" / "example-series.csv"
    with source.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if [int(row["t"]) for row in rows] != list(range(1, len(rows) + 1)):
        raise ValueError("示例要求时点连续且从 1 开始")
    series = [int(row["value"]) for row in rows]
    windows = {}
    for window in (1, 2, 3, 4):
        points = evaluate(series, window, first_target=4)
        groups = [points[:4], points[4:]]
        windows[window] = {
            "points": points, "all": summarize(points),
            "early": summarize(groups[0]), "late": summarize(groups[1]),
        }
    print(json.dumps({"series": series, "windows": windows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
