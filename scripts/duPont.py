#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杜邦分析工具 duPont.py
======================
基于杜邦分析框架拆解ROE驱动因素：
    ROE = 销售净利率 × 总资产周转率 × 权益乘数

功能：
1. 三因素分解
2. 与基准对比（预算/同期/行业），定位短板
3. 敏感性分析：单一因素变化对ROE的影响

用法：
    python duPont.py --net-profit 120 --revenue 1000 --total-assets 800 --equity 400

输入说明：
    --net-profit   净利润
    --revenue      销售收入
    --total-assets 平均总资产
    --equity       平均净资产
    --benchmark    可选，提供基准ROE进行差距分析
"""

import argparse
import json
import sys


def dupont_decompose(net_profit, revenue, total_assets, equity):
    """杜邦三因素分解"""
    if revenue <= 0 or total_assets <= 0 or equity <= 0:
        raise ValueError("收入、总资产、净资产必须为正数")

    net_margin = net_profit / revenue          # 销售净利率
    asset_turnover = revenue / total_assets    # 总资产周转率
    equity_multiplier = total_assets / equity  # 权益乘数
    roe = net_margin * asset_turnover * equity_multiplier

    return {
        "净利润": net_profit,
        "销售收入": revenue,
        "平均总资产": total_assets,
        "平均净资产": equity,
        "ROE": roe,
        "销售净利率": net_margin,
        "总资产周转率": asset_turnover,
        "权益乘数": equity_multiplier,
    }


def sensitivity_analysis(base, factor_name, pct_changes=(-0.2, -0.1, 0.1, 0.2)):
    """敏感性分析：单一因素变化对ROE的影响"""
    results = []
    for pct in pct_changes:
        modified = dict(base)
        if factor_name == "销售净利率":
            modified["销售净利率"] = base["销售净利率"] * (1 + pct)
        elif factor_name == "总资产周转率":
            modified["总资产周转率"] = base["总资产周转率"] * (1 + pct)
        elif factor_name == "权益乘数":
            modified["权益乘数"] = base["权益乘数"] * (1 + pct)

        new_roe = (modified["销售净利率"] * modified["总资产周转率"]
                   * modified["权益乘数"])
        results.append({
            "因素变动": f"{factor_name} {pct:+.0%}",
            "新ROE": new_roe,
            "ROE变化": new_roe - base["ROE"],
        })
    return results


def identify_weakness(base, benchmark=None):
    """定位ROE短板因素"""
    factors = ["销售净利率", "总资产周转率", "权益乘数"]
    if benchmark:
        gaps = {f: base[f] - benchmark[f] for f in factors}
        weakest = min(gaps, key=gaps.get)
        return weakest, gaps
    return None, None


def main():
    parser = argparse.ArgumentParser(description="华为杜邦分析工具")
    parser.add_argument("--net-profit", type=float, required=True, help="净利润")
    parser.add_argument("--revenue", type=float, required=True, help="销售收入")
    parser.add_argument("--total-assets", type=float, required=True, help="平均总资产")
    parser.add_argument("--equity", type=float, required=True, help="平均净资产")
    parser.add_argument("--benchmark-roe", type=float, help="基准ROE（可选）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    try:
        base = dupont_decompose(args.net_profit, args.revenue,
                                args.total_assets, args.equity)
    except ValueError as e:
        print(f"校验失败：{e}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        output = dict(base)
        output["敏感性分析"] = {
            "销售净利率": sensitivity_analysis(base, "销售净利率"),
            "总资产周转率": sensitivity_analysis(base, "总资产周转率"),
            "权益乘数": sensitivity_analysis(base, "权益乘数"),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    print("=" * 60)
    print("              华为杜邦分析报告")
    print("=" * 60)
    print(f"净利润         : {base['净利润']}")
    print(f"销售收入       : {base['销售收入']}")
    print(f"平均总资产     : {base['平均总资产']}")
    print(f"平均净资产     : {base['平均净资产']}")
    print("-" * 60)
    print(f"ROE            : {base['ROE']:.2%}")
    print(f"  销售净利率   : {base['销售净利率']:.2%}")
    print(f"  总资产周转率 : {base['总资产周转率']:.2f}")
    print(f"  权益乘数     : {base['权益乘数']:.2f}")
    print("-" * 60)

    if args.benchmark_roe:
        gap = base["ROE"] - args.benchmark_roe
        print(f"基准ROE        : {args.benchmark_roe:.2%}")
        print(f"差距           : {gap:+.2%}")
        print(f"结论           : {'高于基准' if gap >= 0 else '低于基准，需诊断短板'}")

    print("=" * 60)


if __name__ == "__main__":
    main()