#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金三角诊断工具 golden_triangle.py
=================================
基于华为财务金三角框架（增长性/盈利性/流动性）进行综合诊断。

功能：
1. 单维度评分（0-10分）
2. 双维度交叉定位（明星/成熟/风险/困境等）
3. 八象限综合分类
4. 雷达图数据输出（供可视化）

用法：
    python golden_triangle.py
    python golden_triangle.py --growth 0.15 --roe 0.12 --ocf-ni 0.6

输入指标说明：
    --growth   销售增长率（小数，如 0.15 表示15%）
    --roe      净资产收益率（小数，如 0.12 表示12%）
    --ocf-ni    经营现金流/净利润（小数，如 0.6）
"""

import argparse
import json
import sys


def growth_score(growth_rate):
    """增长性评分（基于销售增长率）"""
    if growth_rate > 0.20:
        return 10
    elif growth_rate > 0.10:
        return 7
    elif growth_rate > 0.00:
        return 4
    else:
        return 1


def profitability_score(roe):
    """盈利性评分（基于ROE）"""
    if roe > 0.20:
        return 10
    elif roe > 0.10:
        return 7
    elif roe > 0.05:
        return 4
    else:
        return 1


def liquidity_score(ocf_to_ni):
    """流动性评分（基于经营现金流/净利润）"""
    if ocf_to_ni > 1.2:
        return 10
    elif ocf_to_ni > 0.8:
        return 7
    elif ocf_to_ni > 0.5:
        return 4
    else:
        return 1


def interpret_composite(score):
    """综合评分解读"""
    if score >= 8:
        return "优秀"
    elif score >= 6:
        return "良好"
    elif score >= 4:
        return "一般"
    elif score >= 2:
        return "较差"
    else:
        return "危机"


def cross_growth_profit(growth_rate, roe):
    """增长性 vs 盈利性 双维度交叉定位"""
    g_high = growth_rate >= 0.10
    p_high = roe >= 0.10
    if g_high and p_high:
        return "明星企业（理想状态）"
    elif g_high and not p_high:
        return "粗放增长（需优化成本）"
    elif not g_high and p_high:
        return "成熟企业（需寻找新增长点）"
    else:
        return "困境企业（需全面改革）"


def cross_growth_liquidity(growth_rate, ocf_to_ni):
    """增长性 vs 流动性 双维度交叉定位"""
    g_high = growth_rate >= 0.10
    l_high = ocf_to_ni >= 0.8
    if g_high and l_high:
        return "健康增长（理想状态）"
    elif g_high and not l_high:
        return "透支增长（需关注现金流）"
    elif not g_high and l_high:
        return "保守经营（需评估机会成本）"
    else:
        return "经营困难（需紧急救助）"


def cross_profit_liquidity(roe, ocf_to_ni):
    """盈利性 vs 流动性 双维度交叉定位"""
    p_high = roe >= 0.10
    l_high = ocf_to_ni >= 0.8
    if p_high and l_high:
        return "优质企业（理想状态）"
    elif p_high and not l_high:
        return "账面富贵（需加强回款）"
    elif not p_high and l_high:
        return "资金闲置（需提升投资效率）"
    else:
        return "经营危机（需全面诊断）"


def quadrant_classify(growth_rate, roe, ocf_to_ni):
    """八象限综合分类（结合流动性判断）"""
    g_high = growth_rate >= 0.10
    p_high = roe >= 0.10
    l_high = ocf_to_ni >= 0.8

    if g_high and p_high and l_high:
        return "健康型（三角均衡）"
    elif g_high and p_high and not l_high:
        return "增长型（关注现金流）"
    elif g_high and not p_high and l_high:
        return "扩张型（关注盈利质量）"
    elif not g_high and p_high and l_high:
        return "现金型（关注增长动力）"
    elif g_high and not p_high and not l_high:
        return "风险型（增长透支+盈利不足）"
    elif not g_high and p_high and not l_high:
        return "风险型（账面富贵）"
    elif not g_high and not p_high and l_high:
        return "风险型（资金闲置）"
    else:
        return "危机型（三角均弱）"


def radar_data(growth_rate, roe, ocf_to_ni):
    """输出雷达图数据（供可视化）"""
    return {
        "维度": ["增长性", "盈利性", "流动性"],
        "评分": [
            growth_score(growth_rate),
            profitability_score(roe),
            liquidity_score(ocf_to_ni),
        ],
        "原始值": {
            "销售增长率": growth_rate,
            "ROE": roe,
            "经营现金流/净利润": ocf_to_ni,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="华为财务金三角诊断工具")
    parser.add_argument("--growth", type=float, default=0.15, help="销售增长率（小数）")
    parser.add_argument("--roe", type=float, default=0.12, help="ROE（小数）")
    parser.add_argument("--ocf-ni", type=float, default=0.60, help="经营现金流/净利润")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    gs = growth_score(args.growth)
    ps = profitability_score(args.roe)
    ls = liquidity_score(args.ocf_ni)
    composite = round((gs + ps + ls) / 3, 1)

    result = {
        "增长性": {
            "原始值": f"{args.growth:.1%}",
            "评分": gs,
        },
        "盈利性": {
            "原始值": f"{args.roe:.1%}",
            "评分": ps,
        },
        "流动性": {
            "原始值": f"{args.ocf_ni:.2f}",
            "评分": ls,
        },
        "综合评分": composite,
        "综合评级": interpret_composite(composite),
        "交叉诊断": {
            "增长vs盈利": cross_growth_profit(args.growth, args.roe),
            "增长vs流动性": cross_growth_liquidity(args.growth, args.ocf_ni),
            "盈利vs流动性": cross_profit_liquidity(args.roe, args.ocf_ni),
        },
        "八象限分类": quadrant_classify(args.growth, args.roe, args.ocf_ni),
        "雷达图数据": radar_data(args.growth, args.roe, args.ocf_ni),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("              华为财务金三角诊断报告")
        print("=" * 60)
        print(f"增长性（销售增长率） : {result['增长性']['原始值']}  →  {gs}分")
        print(f"盈利性（ROE）         : {result['盈利性']['原始值']}  →  {ps}分")
        print(f"流动性（OCF/净利润）  : {result['流动性']['原始值']}  →  {ls}分")
        print("-" * 60)
        print(f"综合评分             : {composite}/10  →  {interpret_composite(composite)}")
        print("-" * 60)
        print("【双维度交叉诊断】")
        print(f"  增长 vs 盈利   : {result['交叉诊断']['增长vs盈利']}")
        print(f"  增长 vs 流动性 : {result['交叉诊断']['增长vs流动性']}")
        print(f"  盈利 vs 流动性 : {result['交叉诊断']['盈利vs流动性']}")
        print("-" * 60)
        print(f"【八象限分类】: {result['八象限分类']}")
        print("=" * 60)


if __name__ == "__main__":
    main()