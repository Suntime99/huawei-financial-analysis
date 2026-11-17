#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预算偏差分析工具 budget_variance.py
===================================
基于华为"计划-预算-核算三位一体"框架，对预算执行偏差进行自动分解。

功能：
1. 销售收入偏差分解：销量影响 + 价格影响 + 结构影响
2. 成本偏差分解：产量影响 + 单价影响 + 效率影响
3. 偏差等级判断（绿/黄/橙/红）

用法：
    python budget_variance.py --actual-revenue 9500 --budget-revenue 10000
    python budget_variance.py --revenue-mode

    python budget_variance.py --cost-mode \
        --actual-qty 110 --budget-qty 100 \
        --actual-price 9 --budget-price 10

输入说明（收入模式）：
    --actual-revenue   实际收入
    --budget-revenue   预算收入
    --actual-qty       实际销量
    --budget-qty       预算销量
    --actual-price     实际单价
    --budget-price     预算单价

输入说明（成本模式）：
    --cost-mode        启用成本偏差分解
    --actual-qty       实际产量
    --budget-qty       预算产量
    --actual-price     实际单位成本
    --budget-price     预算单位成本
"""

import argparse
import json
import sys


def variance_level(relative_deviation):
    """偏差等级判断"""
    abs_dev = abs(relative_deviation)
    if abs_dev <= 0.05:
        return "绿色（正常）", "常规监控"
    elif abs_dev <= 0.10:
        return "黄色（关注）", "加强跟踪"
    elif abs_dev <= 0.20:
        return "橙色（预警）", "专项分析"
    else:
        return "红色（告警）", "紧急干预"


def analyze_revenue(actual_revenue, budget_revenue,
                    actual_qty, budget_qty, actual_price, budget_price):
    """销售收入偏差分解：量差 + 价差 + 结构差"""
    revenue_deviation = actual_revenue - budget_revenue
    quantity_impact = (actual_qty - budget_qty) * budget_price
    price_impact = (actual_price - budget_price) * actual_qty
    structure_impact = revenue_deviation - quantity_impact - price_impact

    return {
        "分析模式": "销售收入偏差分解",
        "预算收入": budget_revenue,
        "实际收入": actual_revenue,
        "收入偏差": revenue_deviation,
        "偏差率": revenue_deviation / budget_revenue if budget_revenue else None,
        "偏差等级": variance_level(revenue_deviation / budget_revenue if budget_revenue else 0),
        "销量偏差影响": quantity_impact,
        "价格偏差影响": price_impact,
        "结构偏差影响": structure_impact,
        "责任归属": {
            "销量偏差": "销售部门",
            "价格偏差": "定价部门",
            "结构偏差": "产品/市场部门",
        },
    }


def analyze_cost(actual_qty, budget_qty, actual_price, budget_price):
    """成本偏差分解：产量差 + 单价差 + 效率差"""
    budget_cost = budget_qty * budget_price
    actual_cost = actual_qty * actual_price
    cost_deviation = actual_cost - budget_cost

    quantity_impact = (actual_qty - budget_qty) * budget_price
    price_impact = (actual_price - budget_price) * actual_qty
    efficiency_impact = cost_deviation - quantity_impact - price_impact

    return {
        "分析模式": "成本偏差分解",
        "预算成本": budget_cost,
        "实际成本": actual_cost,
        "成本偏差": cost_deviation,
        "偏差率": cost_deviation / budget_cost if budget_cost else None,
        "偏差等级": variance_level(cost_deviation / budget_cost if budget_cost else 0),
        "产量偏差影响": quantity_impact,
        "单价偏差影响": price_impact,
        "效率偏差影响": efficiency_impact,
        "责任归属": {
            "产量偏差": "生产/运营部门",
            "单价偏差": "采购部门",
            "效率偏差": "生产/流程管理部门",
        },
    }


def main():
    parser = argparse.ArgumentParser(description="华为预算偏差分析工具")
    parser.add_argument("--actual-revenue", type=float, help="实际收入")
    parser.add_argument("--budget-revenue", type=float, help="预算收入")
    parser.add_argument("--actual-qty", type=float, help="实际销量/产量")
    parser.add_argument("--budget-qty", type=float, help="预算销量/产量")
    parser.add_argument("--actual-price", type=float, help="实际单价/单位成本")
    parser.add_argument("--budget-price", type=float, help="预算单价/单位成本")
    parser.add_argument("--cost-mode", action="store_true", help="启用成本偏差分解")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    # 输入校验：必需参数缺失时给出明确提示（退出码1）
    required = (
        ("actual_qty", "budget_qty", "actual_price", "budget_price")
        if args.cost_mode else
        ("actual_revenue", "budget_revenue",
         "actual_qty", "budget_qty", "actual_price", "budget_price")
    )
    missing = [f"--{k.replace('_', '-')}" for k in required if getattr(args, k) is None]
    if missing:
        print(f"输入错误：缺少必需参数 {', '.join(missing)}", file=sys.stderr)
        print("示例：" + ("--cost-mode --actual-qty 110 --budget-qty 100 --actual-price 9 --budget-price 10"
                          if args.cost_mode else
                          "--actual-revenue 9500 --budget-revenue 10000 --actual-qty 900 --budget-qty 1000 --actual-price 10.5 --budget-price 10"),
              file=sys.stderr)
        sys.exit(1)

    if args.cost_mode:
        result = analyze_cost(
            args.actual_qty, args.budget_qty,
            args.actual_price, args.budget_price,
        )
    else:
        result = analyze_revenue(
            args.actual_revenue, args.budget_revenue,
            args.actual_qty, args.budget_qty,
            args.actual_price, args.budget_price,
        )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("=" * 60)
    print(f"          华为预算偏差分析报告（{result['分析模式']}）")
    print("=" * 60)
    print(f"预算值 : {result['预算成本' if '预算成本' in result else '预算收入']}")
    print(f"实际值 : {result['实际成本' if '实际成本' in result else '实际收入']}")
    print(f"偏差值 : {result['成本偏差' if '成本偏差' in result else '收入偏差']}")
    print(f"偏差率 : {result['偏差率']:.2%}" if result["偏差率"] else "偏差率 : N/A")
    level, action = result["偏差等级"]
    print(f"偏差等级 : {level}  →  {action}")
    print("-" * 60)
    if args.cost_mode:
        print(f"产量偏差影响 : {result['产量偏差影响']}")
        print(f"单价偏差影响 : {result['单价偏差影响']}")
        print(f"效率偏差影响 : {result['效率偏差影响']}")
    else:
        print(f"销量偏差影响 : {result['销量偏差影响']}")
        print(f"价格偏差影响 : {result['价格偏差影响']}")
        print(f"结构偏差影响 : {result['结构偏差影响']}")
    print("-" * 60)
    print("【责任归属】")
    for k, v in result["责任归属"].items():
        print(f"  {k} → {v}")
    print("=" * 60)


if __name__ == "__main__":
    main()