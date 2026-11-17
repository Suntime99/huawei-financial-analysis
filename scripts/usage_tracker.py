#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为财务分析 SKILL — 使用统计跟踪器（CAP-D-03）
================================================

Layer D 平台治理层：记录并分析 SKILL 的每次使用，支持双维度统计，
对齐数集采集工具链的 usage_tracker 机制（数据 → 洞察 → 行动 闭环）。

两个统计维度：
1. **场景维度**（Layer A）：全面诊断 / 专项分析 / 管理汇报 / 前瞻预测
2. **能力维度**（Layer B）：golden_triangle / budget_variance / duPont /
   forecast_accuracy / dashboard / excel_templates

存储格式（JSONL，追加写入，纯本地，不上报）：
    ~/.huawei-financial-analysis/usage/usage.jsonl

每条记录：
{
  "timestamp": "2026-11-18T10:30:00",
  "scenario": "全面诊断",
  "capabilities": [
    {"name": "golden_triangle", "calls": 1, "success": 1},
    {"name": "duPont", "calls": 1, "success": 1}
  ],
  "status": "success" | "partial" | "fail",
  "note": "完成某公司季度金三角诊断"
}

用法：
    python scripts/usage_tracker.py record --scenario 全面诊断 \
        --capabilities "golden_triangle:1:1,duPont:1:1" [--status success] [--note "..."]
    python scripts/usage_tracker.py analyze [--days 30] [--scenario 诊断] [--capability duPont] [--json]
    python scripts/usage_tracker.py report [--days 30] [--output report.html]
    python scripts/usage_tracker.py list  [--days 30]

纯 Python 标准库实现，无第三方依赖。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta

# ---------- 常量 ----------
BASE_DIR = os.path.expanduser("~/.huawei-financial-analysis/usage")
DATA_FILE = os.path.join(BASE_DIR, "usage.jsonl")
TS_FMT = "%Y-%m-%dT%H:%M:%S"

# Layer B 能力模块的合法短名（用于校验，未知名称也允许记录）
KNOWN_CAPABILITIES = [
    "golden_triangle", "budget_variance", "duPont",
    "forecast_accuracy", "dashboard", "excel_templates",
]
KNOWN_SCENARIOS = ["全面诊断", "专项分析", "管理汇报", "前瞻预测"]


# ---------- 工具函数 ----------
def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def now_str() -> str:
    return datetime.now().strftime(TS_FMT)


def parse_ts(ts: str) -> datetime:
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")


def load_records() -> list[dict]:
    records = []
    if not os.path.isfile(DATA_FILE):
        return records
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def save_record(record: dict) -> None:
    ensure_dir(BASE_DIR)
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ---------- record ----------
def cmd_record(args: argparse.Namespace) -> int:
    if not args.scenario:
        print("错误：--scenario 必填", file=sys.stderr)
        return 2
    caps = []
    if args.capabilities:
        for item in args.capabilities.split(","):
            item = item.strip()
            if not item:
                continue
            parts = item.split(":")
            if len(parts) == 1:
                name, calls, success = parts[0], 1, 1
            elif len(parts) == 2:
                name, calls = parts[0], int(parts[1])
                success = int(parts[1])
            else:
                name, calls, success = parts[0], int(parts[1]), int(parts[2])
            caps.append({"name": name, "calls": calls, "success": success})

    status = args.status if args.status in ("success", "partial", "fail") else "success"
    record = {
        "timestamp": now_str(),
        "scenario": args.scenario.strip(),
        "capabilities": caps,
        "status": status,
        "note": (args.note or "").strip(),
    }
    save_record(record)
    total_calls = sum(c["calls"] for c in caps)
    total_success = sum(c["success"] for c in caps)
    print(f"已记录: scenario={record['scenario']} status={status} "
          f"caps={len(caps)} total_calls={total_calls} success={total_success}")
    if args.scenario.strip() not in KNOWN_SCENARIOS:
        print(f"提示: 场景 '{args.scenario.strip()}' 不在标准四类"
              f"（{'/'.join(KNOWN_SCENARIOS)}）中，仍已记录。", file=sys.stderr)
    return 0


# ---------- analyze ----------
def analyze(records, days=None, scenario=None, capability=None):
    cutoff = (datetime.now() - timedelta(days=days)) if days else None
    filtered = []
    for r in records:
        try:
            dt = parse_ts(r.get("timestamp", ""))
        except Exception:
            continue
        if cutoff and dt < cutoff:
            continue
        if scenario and scenario.lower() not in r.get("scenario", "").lower():
            continue
        if capability:
            names = [c["name"].lower() for c in r.get("capabilities", [])]
            if capability.lower() not in names:
                continue
        filtered.append(r)

    by_day = OrderedDict()
    for r in sorted(filtered, key=lambda x: x.get("timestamp", "")):
        day = r.get("timestamp", "")[:10]
        agg = by_day.setdefault(day, {"calls": 0, "success": 0,
                                      "tasks": 0, "succeeded_tasks": 0})
        agg["tasks"] += 1
        if r.get("status") == "success":
            agg["succeeded_tasks"] += 1
        for c in r.get("capabilities", []):
            agg["calls"] += c.get("calls", 0)
            agg["success"] += c.get("success", 0)

    by_capability = OrderedDict()
    for r in filtered:
        for c in r.get("capabilities", []):
            name = c.get("name", "未知")
            agg = by_capability.setdefault(name, {"calls": 0, "success": 0, "tasks": 0})
            agg["calls"] += c.get("calls", 0)
            agg["success"] += c.get("success", 0)
            agg["tasks"] += 1

    by_scenario = OrderedDict()
    for r in filtered:
        sc = r.get("scenario", "未分类")
        agg = by_scenario.setdefault(sc, {"calls": 0, "success": 0, "tasks": 0,
                                           "succeeded_tasks": 0})
        agg["tasks"] += 1
        if r.get("status") == "success":
            agg["succeeded_tasks"] += 1
        for c in r.get("capabilities", []):
            agg["calls"] += c.get("calls", 0)
            agg["success"] += c.get("success", 0)

    total_calls = sum(a["calls"] for a in by_day.values())
    total_success = sum(a["success"] for a in by_day.values())
    total_tasks = len(filtered)
    succeeded_tasks = sum(1 for r in filtered if r.get("status") == "success")

    return {
        "total_records": len(filtered),
        "total_tasks": total_tasks,
        "succeeded_tasks": succeeded_tasks,
        "task_success_rate": round(succeeded_tasks / total_tasks * 100, 1) if total_tasks else 0.0,
        "total_calls": total_calls,
        "total_success": total_success,
        "call_success_rate": round(total_success / total_calls * 100, 1) if total_calls else 0.0,
        "by_day": dict(by_day),
        "by_capability": dict(by_capability),
        "by_scenario": dict(by_scenario),
    }


def cmd_analyze(args: argparse.Namespace) -> int:
    result = analyze(load_records(), days=args.days,
                     scenario=args.scenario, capability=args.capability)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    print("=" * 60)
    print("华为财务分析 SKILL 使用统计")
    print("=" * 60)
    print(f"时间范围: {args.days} 天" if args.days else "时间范围: 全部")
    print(f"任务总数: {result['total_tasks']}  (成功 {result['succeeded_tasks']}, "
          f"成功率 {result['task_success_rate']}%)")
    print(f"能力调用: {result['total_calls']} 次  (成功 {result['total_success']} 次, "
          f"成功率 {result['call_success_rate']}%)")
    print("\n【按能力模块统计】")
    if result["by_capability"]:
        print(f"{'模块':<20}{'调用次数':>10}{'成功次数':>10}{'成功率':>10}")
        print("-" * 52)
        for name, agg in sorted(result["by_capability"].items(),
                                key=lambda x: x[1]["calls"], reverse=True):
            rate = (agg["success"] / agg["calls"] * 100) if agg["calls"] else 0
            print(f"{name:<20}{agg['calls']:>10}{agg['success']:>10}{rate:>9.1f}%")
    else:
        print("  (无数据)")
    print("\n【按场景统计】")
    if result["by_scenario"]:
        for sc, agg in sorted(result["by_scenario"].items(),
                              key=lambda x: x[1]["tasks"], reverse=True):
            rate = (agg["succeeded_tasks"] / agg["tasks"] * 100) if agg["tasks"] else 0
            print(f"  {sc}: {agg['tasks']} 个任务, 调用 {agg['calls']} 次, 成功率 {rate:.1f}%")
    else:
        print("  (无数据)")
    return 0


# ---------- report ----------
def _esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _rate(n: int, d: int) -> str:
    return f"{n / d * 100:.1f}%" if d else "0.0%"


def cmd_report(args: argparse.Namespace) -> int:
    result = analyze(load_records(), days=args.days,
                     scenario=args.scenario, capability=args.capability)
    gen_at = now_str()

    cap_rows = ""
    for name, agg in sorted(result["by_capability"].items(),
                            key=lambda x: x[1]["calls"], reverse=True):
        cap_rows += (
            f"<tr><td>{_esc(name)}</td><td>{agg['calls']}</td>"
            f"<td>{agg['success']}</td><td>{_rate(agg['success'], agg['calls'])}</td>"
            f"<td>{agg['tasks']}</td></tr>\n")
    if not cap_rows:
        cap_rows = "<tr><td colspan='5' style='text-align:center;color:#999'>暂无数据</td></tr>"

    sc_rows = ""
    for sc, agg in sorted(result["by_scenario"].items(),
                          key=lambda x: x[1]["tasks"], reverse=True):
        sc_rows += (
            f"<tr><td>{_esc(sc)}</td><td>{agg['tasks']}</td>"
            f"<td>{agg['succeeded_tasks']}</td>"
            f"<td>{_rate(agg['succeeded_tasks'], agg['tasks'])}</td>"
            f"<td>{agg['calls']}</td></tr>\n")
    if not sc_rows:
        sc_rows = "<tr><td colspan='5' style='text-align:center;color:#999'>暂无数据</td></tr>"

    day_rows = ""
    for d in sorted(result["by_day"].keys()):
        agg = result["by_day"][d]
        day_rows += (
            f"<tr><td>{_esc(d)}</td><td>{agg['tasks']}</td>"
            f"<td>{agg['calls']}</td><td>{agg['success']}</td>"
            f"<td>{_rate(agg['success'], agg['calls'])}</td></tr>\n")
    if not day_rows:
        day_rows = "<tr><td colspan='5' style='text-align:center;color:#999'>暂无数据</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<title>华为财务分析 SKILL 使用统计报表</title>
<style>
 body{{font-family:"Segoe UI","Microsoft YaHei",sans-serif;margin:24px;background:#f6f8fa;color:#24292f}}
 h1{{font-size:22px;border-bottom:2px solid #205081;padding-bottom:8px}}
 .cards{{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}}
 .card{{background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:14px 20px;flex:1;min-width:140px}}
 .card .num{{font-size:26px;font-weight:600;color:#205081}}
 .card .lbl{{font-size:12px;color:#57606a;margin-top:4px}}
 table{{border-collapse:collapse;width:100%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
 th,td{{padding:8px 12px;text-align:left;border-bottom:1px solid #eaeef2;font-size:13px}}
 th{{background:#eef3f8}}
 .meta{{color:#57606a;font-size:12px;margin-bottom:8px}}
</style></head><body>
<h1>📊 华为财务分析 SKILL 使用统计报表</h1>
<div class="meta">生成时间：{gen_at} ｜ 数据文件：{DATA_FILE}</div>
<div class="cards">
 <div class="card"><div class="num">{result['total_tasks']}</div><div class="lbl">任务总数</div></div>
 <div class="card"><div class="num">{result['task_success_rate']}%</div><div class="lbl">任务成功率</div></div>
 <div class="card"><div class="num">{result['total_calls']}</div><div class="lbl">能力调用次数</div></div>
 <div class="card"><div class="num">{result['call_success_rate']}%</div><div class="lbl">调用成功率</div></div>
 <div class="card"><div class="num">{len(result['by_capability'])}</div><div class="lbl">使用能力模块数</div></div>
</div>
<h2>🛠️ 能力模块使用统计（Layer B 维度）</h2>
<table><thead><tr><th>模块</th><th>调用次数</th><th>成功次数</th><th>成功率</th><th>涉及任务数</th></tr></thead>
<tbody>{cap_rows}</tbody></table>
<h2>🗂️ 场景分布（Layer A 维度）</h2>
<table><thead><tr><th>场景</th><th>任务数</th><th>成功任务</th><th>任务成功率</th><th>能力调用</th></tr></thead>
<tbody>{sc_rows}</tbody></table>
<h2>📅 每日明细</h2>
<table><thead><tr><th>日期</th><th>任务数</th><th>调用次数</th><th>成功次数</th><th>成功率</th></tr></thead>
<tbody>{day_rows}</tbody></table>
<footer style="margin-top:24px;color:#57606a;font-size:12px;">
 由 <code>scripts/usage_tracker.py report</code> 生成 · 纯标准库 · 数据本地存储</footer>
</body></html>"""
    out = args.output or os.path.join(BASE_DIR, "usage_report.html")
    ensure_dir(os.path.dirname(out) or ".")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"报表已生成: {out}")
    return 0


# ---------- list ----------
def cmd_list(args: argparse.Namespace) -> int:
    cutoff = (datetime.now() - timedelta(days=args.days)) if args.days else None
    shown = 0
    for r in load_records():
        try:
            dt = parse_ts(r.get("timestamp", ""))
        except Exception:
            continue
        if cutoff and dt < cutoff:
            continue
        caps = ",".join(
            f"{c.get('name')}({c.get('calls',0)}/{c.get('success',0)})"
            for c in r.get("capabilities", []))
        print(f"{r.get('timestamp','')}  [{r.get('status','')}]  "
              f"{r.get('scenario','')}  :: {caps}")
        shown += 1
    if not shown:
        print("(无记录)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="usage_tracker.py",
        description="华为财务分析 SKILL 使用统计跟踪器（CAP-D-03）")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("record", help="记录一次使用")
    p.add_argument("--scenario", required=True, help="使用场景（如：全面诊断）")
    p.add_argument("--capabilities", default="",
                   help="能力模块，格式 name:calls:success，逗号分隔，"
                        "如 golden_triangle:1:1,duPont:1:1")
    p.add_argument("--status", choices=["success", "partial", "fail"], default="success")
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_record)

    p = sub.add_parser("analyze", help="分析汇总")
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--scenario", default=None)
    p.add_argument("--capability", default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_analyze)

    p = sub.add_parser("report", help="生成 HTML 报表")
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--scenario", default=None)
    p.add_argument("--capability", default=None)
    p.add_argument("--output", default=None)
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("list", help="列出记录")
    p.add_argument("--days", type=int, default=30)
    p.set_defaults(func=cmd_list)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())