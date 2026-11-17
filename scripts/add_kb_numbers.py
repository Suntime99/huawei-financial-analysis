#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为19个知识库文件批量插入KB编号元数据行"""
import io
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (相对路径, KB编号, 主题简述)
ENTRIES = [
    ("chapters/ch01-analysis-overview.md", "KB-HFA-01", "财务分析总论"),
    ("chapters/ch02-profitability.md", "KB-HFA-02", "盈利能力分析"),
    ("chapters/ch03-solvency.md", "KB-HFA-03", "偿债能力分析"),
    ("chapters/ch04-efficiency.md", "KB-HFA-04", "营运能力分析"),
    ("chapters/ch05-growth.md", "KB-HFA-05", "发展能力分析"),
    ("chapters/ch06-golden-triangle.md", "KB-HFA-06", "财务金三角综合诊断"),
    ("chapters/ch07-budget-analysis.md", "KB-HFA-07", "预算执行分析"),
    ("chapters/ch08-dashboard.md", "KB-HFA-08", "经营仪表盘构建"),
    ("chapters/ch09-forecasting.md", "KB-HFA-09", "财务预测模型"),
    ("chapters/ch10-report-writing.md", "KB-HFA-10", "财务分析报告撰写"),
    ("chapters/ch11-bp-analysis.md", "KB-HFA-11", "财务BP数据分析实战"),
    ("chapters/ch12-benchmarking.md", "KB-HFA-12", "行业对标分析"),
    ("chapters/ch13-huawei-cases.md", "KB-HFA-13", "华为财务案例库"),
    ("chapters/ch14-industry-adaptation.md", "KB-HFA-14", "行业适配分析"),
    ("chapters/ch15-interactive-analysis.md", "KB-HFA-15", "对话引导协议"),
    ("chapters/ch16-industry-extension.md", "KB-HFA-16", "行业适配扩展"),
    ("cheatsheet.md", "KB-HFA-17", "核心指标速查表"),
    ("patterns.md", "KB-HFA-18", "分析模式库"),
    ("glossary.md", "KB-HFA-19", "财务分析术语表"),
]

UPDATED = "2026-11"

for rel, kb_id, topic in ENTRIES:
    path = os.path.join(BASE, rel)
    with io.open(path, encoding="utf-8") as f:
        lines = f.readlines()

    # 找第一个以 # 开头的行（H1标题）
    h1_idx = None
    for i, line in enumerate(lines):
        if line.startswith("# "):
            h1_idx = i
            break
    if h1_idx is None:
        print(f"WARN  {rel}: 未找到H1标题，跳过")
        continue

    # 跳过已有KB编号的文件（幂等）
    if any("KB-HFA-" in lines[j] for j in range(h1_idx, min(h1_idx + 5, len(lines)))):
        print(f"SKIP  {rel} (已有KB编号)")
        continue

    meta = f"\n> **KB编号：{kb_id}** | 主题：{topic} | 更新：{UPDATED} | 依赖：见 kb-index.md\n"
    lines.insert(h1_idx + 1, meta)

    with io.open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"OK    {rel} -> {kb_id}")

print("完成")