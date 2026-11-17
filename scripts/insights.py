#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为财务分析 SKILL — 使用洞察与能力退化预警（CAP-D-04）
========================================================

Layer D 平台治理层：基于 usage_tracker 的记录数据，提供复盘与进化能力，
对齐数集采集工具链的 insights.py 机制。

功能：
    1. 能力效能排行榜（rank）—— 按成功率/调用量评估各 Layer B 能力模块
    2. 能力退化预警（alert）—— 检测成功率下滑/低于阈值的能力模块
    3. 月度复盘（monthly）—— 自动生成当月使用摘要与改进建议
    4. 季度复盘（quarterly）—— 对比上季度能力成功率变化，给出迭代建议

设计参照 CAP 能力矩阵"自我迭代"：
    每月复盘 → 能力排行榜 → 退化预警 → 迭代改进 → 测试验证 → 数据回流

用法：
    python scripts/insights.py rank      [--days 30] [--json]
    python scripts/insights.py alert     [--days 30] [--warn-below 80] [--json]
    python scripts/insights.py monthly   [--output report.md] [--json]
    python scripts/insights.py quarterly [--output report.md] [--json]

纯 Python 标准库实现，无第三方依赖。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

# 兼容导入：优先同目录，其次上两级
try:
    from usage_tracker import analyze, load_records
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from usage_tracker import analyze, load_records

DEFAULT_WARN_BELOW = 80.0   # 能力成功率低于80% → 预警
DEFAULT_MIN_CALLS = 3       # 调用少于3次不计入预警（样本不足）
TOP_N = 5


def _rate(success: int, calls: int) -> float:
    return (success / calls * 100) if calls else 0.0


def _by_capability(records: list[dict]) -> dict:
    """按能力模块聚合调用/成功。"""
    agg = defaultdict(lambda: {"calls": 0, "success": 0})
    for r in records:
        for c in r.get("capabilities", []):
            name = c.get("name", "未知")
            agg[name]["calls"] += c.get("calls", 0)
            agg[name]["success"] += c.get("success", 0)
    return dict(agg)


def _records_in_window(records, start: datetime, end: datetime) -> list[dict]:
    out = []
    for r in records:
        try:
            dt = datetime.strptime(r["timestamp"][:19], "%Y-%m-%dT%H:%M:%S")
        except Exception:
            continue
        if start <= dt <= end:
            out.append(r)
    return out


# ---------- rank ----------
def capability_ranking(records, days=None, top_n=TOP_N, min_calls=1):
    filtered = records
    if days:
        cutoff = datetime.now() - timedelta(days=days)
        filtered = _records_in_window(records, cutoff, datetime.now())
    agg = _by_capability(filtered)
    ranked = []
    for name, a in agg.items():
        if a["calls"] < min_calls:
            continue
        ranked.append({
            "name": name,
            "calls": a["calls"],
            "success": a["success"],
            "rate": round(_rate(a["success"], a["calls"]), 1),
        })
    ranked.sort(key=lambda x: (-x["rate"], -x["calls"]))
    return ranked[:top_n]


def cmd_rank(args: argparse.Namespace) -> int:
    records = load_records()
    ranked = capability_ranking(records, days=args.days, top_n=args.top)
    if args.json:
        print(json.dumps(ranked, ensure_ascii=False, indent=2))
        return 0
    print("【能力模块效能排行榜】")
    if not ranked:
        print("  (无数据，先用 usage_tracker.py record 记录使用)")
        return 0
    print(f"{'排名':<5}{'模块':<20}{'成功率':>8}{'调用':>8}")
    print("-" * 45)
    for i, item in enumerate(ranked, 1):
        print(f"{i:<5}{item['name']:<20}{item['rate']:>7.1f}%{item['calls']:>8}")
    return 0


# ---------- alert ----------
def degradation_alerts(records, days=None, warn_below=DEFAULT_WARN_BELOW,
                       min_calls=DEFAULT_MIN_CALLS):
    filtered = records
    if days:
        cutoff = datetime.now() - timedelta(days=days)
        filtered = _records_in_window(records, cutoff, datetime.now())
    agg = _by_capability(filtered)
    alerts = []
    for name, a in agg.items():
        if a["calls"] < min_calls:
            continue
        rate = _rate(a["success"], a["calls"])
        if rate < warn_below:
            alerts.append({
                "name": name, "calls": a["calls"], "success": a["success"],
                "rate": round(rate, 1), "threshold": warn_below,
                "suggestion": "排查近期失败原因，必要时降级或回滚该模块",
            })
    alerts.sort(key=lambda x: x["rate"])
    return alerts


def cmd_alert(args: argparse.Namespace) -> int:
    records = load_records()
    alerts = degradation_alerts(records, days=args.days,
                                warn_below=args.warn_below, min_calls=args.min_calls)
    if args.json:
        print(json.dumps(alerts, ensure_ascii=False, indent=2))
        return 0
    print(f"【能力退化预警】（成功率 < {args.warn_below}% 且调用 >= {args.min_calls}）")
    if not alerts:
        print("  ✅ 无预警项")
        return 0
    for a in alerts:
        print(f"  🔴 {a['name']}: 成功率 {a['rate']}%（{a['success']}/{a['calls']}）"
              f" → {a['suggestion']}")
    return 0


# ---------- monthly ----------
def monthly_report(records, days=30, output=None):
    cutoff = datetime.now() - timedelta(days=days)
    window = _records_in_window(records, cutoff, datetime.now())
    agg = _by_capability(window)
    total_calls = sum(a["calls"] for a in agg.values())
    total_success = sum(a["success"] for a in agg.values())
    alerts = degradation_alerts(records, days=days)

    lines = []
    lines.append(f"# 华为财务分析 SKILL · 月度复盘（近{days}天）")
    lines.append(f"\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"\n## 一、总体")
    lines.append(f"- 能力调用：{total_calls} 次，成功 {total_success} 次，"
                 f"成功率 {_rate(total_success, total_calls):.1f}%")
    lines.append(f"- 活跃能力模块：{len(agg)} 个")
    lines.append("\n## 二、能力排行")
    lines.append("| 模块 | 调用 | 成功 | 成功率 |")
    lines.append("|------|------|------|--------|")
    for item in capability_ranking(window):
        lines.append(f"| {item['name']} | {item['calls']} | {item['success']} | {item['rate']}% |")
    lines.append("\n## 三、预警与建议")
    if alerts:
        for a in alerts:
            lines.append(f"- 🔴 {a['name']}（{a['rate']}%）：{a['suggestion']}")
    else:
        lines.append("- ✅ 本期无退化预警")
    lines.append("\n## 四、下月改进")
    lines.append("- [ ] 针对低成功率模块补充单元测试或降级预案")
    lines.append("- [ ] 复核行业基准/阈值是否需按最新业务调整")

    text = "\n".join(lines) + "\n"
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"月度复盘已生成: {output}")
    print(text)
    return 0


def cmd_monthly(args: argparse.Namespace) -> int:
    if args.json:
        records = load_records()
        print(json.dumps({
            "rank": capability_ranking(records, days=30),
            "alerts": degradation_alerts(records, days=30),
        }, ensure_ascii=False, indent=2))
        return 0
    return monthly_report(load_records(), output=args.output)


# ---------- quarterly ----------
def quarterly_report(records, output=None):
    now = datetime.now()
    # 本季度 = 近90天，上季度 = 前90天
    this_q = _records_in_window(records, now - timedelta(days=90), now)
    last_q = _records_in_window(records, now - timedelta(days=180), now - timedelta(days=90))
    this_agg = _by_capability(this_q)
    last_agg = _by_capability(last_q)

    lines = []
    lines.append("# 华为财务分析 SKILL · 季度复盘（对比上季度）")
    lines.append(f"\n生成时间：{now.strftime('%Y-%m-%d %H:%M')}")
    lines.append("\n## 能力成功率环比")
    lines.append("| 模块 | 上季度 | 本季度 | 变化 | 建议 |")
    lines.append("|------|--------|--------|------|------|")
    all_names = sorted(set(this_agg) | set(last_agg))
    for name in all_names:
        lr = _rate(last_agg.get(name, {"success": 0, "calls": 0})["success"],
                   last_agg.get(name, {"success": 0, "calls": 0})["calls"])
        cr = _rate(this_agg.get(name, {"success": 0, "calls": 0})["success"],
                   this_agg.get(name, {"success": 0, "calls": 0})["calls"])
        delta = cr - lr
        if last_agg.get(name, {}).get("calls", 0) == 0:
            sugg = "新增能力"
        elif delta >= 0:
            sugg = "保持"
        elif this_agg.get(name, {}).get("calls", 0) < DEFAULT_MIN_CALLS:
            sugg = "样本不足，观察"
        else:
            sugg = "⚠️ 退化，排查/降级"
        lines.append(f"| {name} | {lr:.1f}% | {cr:.1f}% | {delta:+.1f}% | {sugg} |")
    lines.append("\n## 结论")
    degraded = [n for n in all_names
                if last_agg.get(n, {}).get("calls", 0) >= DEFAULT_MIN_CALLS
                and this_agg.get(n, {}).get("calls", 0) >= DEFAULT_MIN_CALLS
                and _rate(this_agg[n]["success"], this_agg[n]["calls"])
                < _rate(last_agg[n]["success"], last_agg[n]["calls"]) - 10]
    if degraded:
        lines.append(f"需优先处理：{', '.join(degraded)}")
    else:
        lines.append("✅ 无显著退化能力，维持当前能力矩阵")

    text = "\n".join(lines) + "\n"
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"季度复盘已生成: {output}")
    print(text)
    return 0


def cmd_quarterly(args: argparse.Namespace) -> int:
    return quarterly_report(load_records(), output=args.output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="insights.py",
                                    description="华为财务分析 SKILL 使用洞察与复盘（CAP-D-04）")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("rank", help="能力效能排行榜")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--top", type=int, default=5)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_rank)

    p = sub.add_parser("alert", help="能力退化预警")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--warn-below", type=float, default=DEFAULT_WARN_BELOW)
    p.add_argument("--min-calls", type=int, default=DEFAULT_MIN_CALLS)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_alert)

    p = sub.add_parser("monthly", help="月度复盘")
    p.add_argument("--output", default=None, help="输出 markdown 路径")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_monthly)

    p = sub.add_parser("quarterly", help="季度复盘（对比上季度）")
    p.add_argument("--output", default=None, help="输出 markdown 路径")
    p.set_defaults(func=cmd_quarterly)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())