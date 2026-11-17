#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经营仪表盘生成器 dashboard_generator.py（可视化增强版）
======================================================
基于华为R&A体系（Reporting & Analysis），从CSV数据生成HTML经营仪表盘。

v2.0 增强：
1. 摘要卡片（指标总数/正常/关注/预警统计）
2. CSS 横向进度条（预算执行率可视化）
3. 金三角 SVG 雷达图（自动从增长性/盈利性/流动性类别生成）
4. 红黄绿预警标记

CSV输入格式：
    指标名称,类别,数值,预算,单位,预警阈值
    销售收入,增长性,9500,10000,万元,0.10
    毛利率,盈利性,0.22,0.25,%,0.05

用法：
    python dashboard_generator.py --csv data.csv --output dashboard.html
"""

import argparse
import csv
import html
import json
import math
import sys
from collections import defaultdict

# 金三角雷达图颜色
RADAR_COLORS = {"增长性": "#4CAF50", "盈利性": "#2196F3", "流动性": "#FF9800"}
OTHER_COLOR = "#9E9E9E"


def load_csv(path):
    """读取CSV文件"""
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "指标名称": row["指标名称"].strip(),
                "类别": row["类别"].strip(),
                "数值": float(row["数值"]),
                "预算": float(row["预算"]) if row["预算"] else None,
                "单位": row.get("单位", "").strip(),
                "预警阈值": float(row["预警阈值"]) if row.get("预警阈值") else 0.10,
            })
    return rows


def classify(deviation_rate, threshold):
    """红黄绿预警分类"""
    abs_dev = abs(deviation_rate)
    if abs_dev <= threshold * 0.5:
        return "green", "正常"
    elif abs_dev <= threshold:
        return "yellow", "关注"
    else:
        return "red", "预警"


def build_radar_svg(categories):
    """
    生成金三角雷达图（SVG）
    categories: {类别名: 执行率(0-1.5)}，取增长性/盈利性/流动性
    """
    center_x, center_y = 160, 140
    radius_max = 100
    # 三角顶点角度：-90°（上）、30°（右下）、150°（左下）
    angles = [-90, 30, 150]

    # 取金三角三类，若不足三类用其他类别补位
    keys = [k for k in ["增长性", "盈利性", "流动性"] if k in categories]
    others = [k for k in categories if k not in keys]
    for k in others[: 3 - len(keys)]:
        keys.append(k)
    values = [max(0.0, min(categories[k], 1.5)) for k in keys]

    # 背景网格（3层）
    grid = ""
    for level in (0.33, 0.66, 1.0):
        pts = []
        for ang in angles:
            rad = math.radians(ang)
            x = center_x + radius_max * level * math.cos(rad)
            y = center_y + radius_max * level * math.sin(rad)
            pts.append(f"{x:.1f},{y:.1f}")
        grid += f'<polygon points="{" ".join(pts)}" fill="none" stroke="#ddd" stroke-width="1"/>'

    # 轴线
    axes = ""
    for ang in angles:
        rad = math.radians(ang)
        x = center_x + radius_max * math.cos(rad)
        y = center_y + radius_max * math.sin(rad)
        axes += f'<line x1="{center_x}" y1="{center_y}" x2="{x:.1f}" y2="{y:.1f}" stroke="#ccc" stroke-width="1"/>'

    # 数据多边形
    pts = []
    for i, v in enumerate(values):
        rad = math.radians(angles[i])
        x = center_x + radius_max * (v / 1.5) * math.cos(rad)
        y = center_y + radius_max * (v / 1.5) * math.sin(rad)
        pts.append(f"{x:.1f},{y:.1f}")
    data_poly = (
        f'<polygon points="{" ".join(pts)}" fill="rgba(33,150,243,0.25)" '
        f'stroke="#2196F3" stroke-width="2"/>'
    )

    # 顶点标注
    labels = ""
    for i, k in enumerate(keys):
        rad = math.radians(angles[i])
        lx = center_x + (radius_max + 22) * math.cos(rad)
        ly = center_y + (radius_max + 22) * math.sin(rad)
        color = RADAR_COLORS.get(k, OTHER_COLOR)
        pct = categories[k] * 100 if k in categories else 0
        labels += (
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" '
            f'font-size="12" fill="{color}" font-weight="bold">'
            f"{html.escape(k)} {pct:.0f}%</text>"
        )

    # 中心点
    center = f'<circle cx="{center_x}" cy="{center_y}" r="3" fill="#666"/>'

    return (
        f'<svg viewBox="0 0 320 280" width="100%" style="max-width:320px">'
        f"{grid}{axes}{data_poly}{center}{labels}</svg>"
    )


def build_summary(rows):
    """摘要统计卡片"""
    total = len(rows)
    counts = {"正常": 0, "关注": 0, "预警": 0}
    for r in rows:
        if r["预算"]:
            dev = r["数值"] / r["预算"] - 1 if r["预算"] else 0
            _, label = classify(dev, r["预警阈值"])
            counts[label] += 1
        else:
            counts["正常"] += 1
    return f"""
    <div class="cards">
      <div class="card"><div class="card-num">{total}</div><div class="card-label">指标总数</div></div>
      <div class="card green-card"><div class="card-num">{counts['正常']}</div><div class="card-label">正常</div></div>
      <div class="card yellow-card"><div class="card-num">{counts['关注']}</div><div class="card-label">关注</div></div>
      <div class="card red-card"><div class="card-num">{counts['预警']}</div><div class="card-label">预警</div></div>
    </div>"""


def build_table(rows):
    """生成带进度条的分类表格"""
    by_category = defaultdict(list)
    for row in rows:
        by_category[row["类别"]].append(row)

    categories_html = ""
    for category, items in by_category.items():
        categories_html += f'<div class="category"><h2>📌 {html.escape(category)}</h2>'
        categories_html += (
            '<table><tr><th>指标</th><th>数值</th><th>预算</th>'
            '<th>执行率</th><th>可视化</th><th>状态</th></tr>'
        )
        for item in items:
            name = html.escape(item["指标名称"])
            value = item["数值"]
            budget = item["预算"]
            unit = html.escape(item["单位"])
            if budget:
                exec_rate = value / budget if budget else 0
                deviation = exec_rate - 1
                level, label = classify(deviation, item["预警阈值"])
                bar_width = min(int(exec_rate * 100), 100)
                bar_color = {"green": "#4caf50", "yellow": "#ff9800", "red": "#f44336"}[level]
                bar = (
                    f'<div class="bar-bg"><div class="bar" style="width:{bar_width}%;'
                    f'background:{bar_color}"></div></div>'
                )
                status = f'<span class="badge {level}">{label}</span>'
                categories_html += (
                    f'<tr><td>{name}</td>'
                    f'<td>{value:,.2f} {unit}</td>'
                    f'<td>{budget:,.2f} {unit}</td>'
                    f'<td>{exec_rate:.1%}</td>'
                    f'<td>{bar}</td>'
                    f'<td>{status}</td></tr>'
                )
            else:
                categories_html += (
                    f'<tr><td>{name}</td>'
                    f'<td>{value:,.2f} {unit}</td>'
                    f'<td>—</td><td>—</td>'
                    f'<td><div class="bar-bg"><div class="bar gray-bar" style="width:100%"></div></div></td>'
                    f'<td><span class="badge gray">无预算</span></td></tr>'
                )
        categories_html += "</table></div>"
    return categories_html


def build_radar_section(rows):
    """金三角雷达图区域"""
    by_category = defaultdict(list)
    for row in rows:
        by_category[row["类别"]].append(row)

    radar_data = {}
    for category, items in by_category.items():
        if category not in ("增长性", "盈利性", "流动性"):
            continue
        # 用该类别的平均执行率作为雷达值
        rates = []
        for item in items:
            if item["预算"]:
                rates.append(item["数值"] / item["预算"])
        if rates:
            radar_data[category] = sum(rates) / len(rates)

    if len(radar_data) < 2:
        return ""
    svg = build_radar_svg(radar_data)
    return f"""
    <div class="radar-section">
      <h2>🔺 金三角雷达图（预算执行率）</h2>
      <div class="radar-container">{svg}</div>
      <div class="radar-note">图形越接近等边三角形，财务越健康；面积越大，综合实力越强。</div>
    </div>"""


def build_html(rows):
    """生成完整HTML仪表盘"""
    summary = build_summary(rows)
    table = build_table(rows)
    radar = build_radar_section(rows)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>华为经营仪表盘</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: "Microsoft YaHei", sans-serif; margin: 0; padding: 20px; background: #f0f2f5; color: #333; }}
  h1 {{ text-align: center; color: #205081; margin-bottom: 8px; }}
  .subtitle {{ text-align: center; color: #888; font-size: 13px; margin-bottom: 24px; }}
  .cards {{ display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 24px; }}
  .card {{ background: #fff; border-radius: 10px; padding: 16px 28px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.08); min-width: 110px; }}
  .card-num {{ font-size: 28px; font-weight: bold; }}
  .card-label {{ font-size: 12px; color: #888; margin-top: 4px; }}
  .green-card .card-num {{ color: #4caf50; }}
  .yellow-card .card-num {{ color: #ff9800; }}
  .red-card .card-num {{ color: #f44336; }}
  .layout {{ display: flex; gap: 20px; flex-wrap: wrap; }}
  .table-area {{ flex: 1 1 60%; min-width: 480px; }}
  .radar-section {{ flex: 0 0 360px; background: #fff; border-radius: 10px; padding: 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
  .radar-container {{ display: flex; justify-content: center; }}
  .radar-note {{ font-size: 12px; color: #888; text-align: center; margin-top: 8px; }}
  .category {{ background: #fff; border-radius: 10px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
  .category h2 {{ margin-top: 0; color: #205081; font-size: 16px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ padding: 8px 10px; text-align: left; border-bottom: 1px solid #eee; font-size: 13px; }}
  th {{ background: #f0f4f8; color: #205081; }}
  .badge {{ padding: 2px 10px; border-radius: 12px; color: #fff; font-size: 11px; font-weight: bold; }}
  .green {{ background: #4caf50; }}
  .yellow {{ background: #ff9800; }}
  .red {{ background: #f44336; }}
  .gray {{ background: #9e9e9e; }}
  .bar-bg {{ width: 100px; height: 14px; background: #eee; border-radius: 7px; overflow: hidden; }}
  .bar {{ height: 100%; border-radius: 7px; }}
  .gray-bar {{ background: #ddd !important; }}
  .footer {{ text-align: center; color: #999; margin-top: 24px; font-size: 12px; }}
</style>
</head>
<body>
<h1>📊 华为经营仪表盘（R&A体系）</h1>
<div class="subtitle">由 dashboard_generator.py v2.0 自动生成 · 战略层/管理层/执行层可配置</div>
{summary}
<div class="layout">
  <div class="table-area">{table}</div>
  {radar}
</div>
<div class="footer">华为财务分析技能包 · 数据为示例/用户输入</div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="华为经营仪表盘生成器（可视化增强版）")
    parser.add_argument("--csv", required=True, help="指标CSV文件路径")
    parser.add_argument("--output", default="dashboard.html", help="输出HTML文件路径")
    parser.add_argument("--json", action="store_true", help="同时输出JSON数据")
    args = parser.parse_args()

    try:
        rows = load_csv(args.csv)
    except FileNotFoundError:
        print(f"错误：找不到CSV文件 {args.csv}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"错误：CSV缺少必要列 {e}", file=sys.stderr)
        print("必需列：指标名称,类别,数值,预算,单位,预警阈值", file=sys.stderr)
        sys.exit(1)

    html_content = build_html(rows)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ 仪表盘已生成：{args.output}")

    if args.json:
        json_path = args.output.replace(".html", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON数据已导出：{json_path}")


if __name__ == "__main__":
    main()