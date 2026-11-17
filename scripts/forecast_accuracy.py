#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预测准确性评估工具 forecast_accuracy.py
=======================================
基于华为"预测是管理的灵魂"理念，评估预测准确性并归因偏差。

功能：
1. 预测偏差率 / 准确率计算
2. 华为预测考核等级判定（优秀/良好/一般/较差）
3. 偏差原因分类统计

用法：
    python forecast_accuracy.py --forecast 950 --actual 1000 --type revenue

类型说明：
    --type revenue  销售收入（优秀<5%，良好5-10%，一般10-20%，较差>20%）
    --type cost     成本费用（优秀<3%，良好3-5%，一般5-10%，较差>10%）
    --type cashflow 现金流  （优秀<10%，良好10-15%，一般15-25%，较差>25%）
"""

import argparse
import json


# 华为预测考核标准
THRESHOLDS = {
    "revenue":   {"优秀": 0.05, "良好": 0.10, "一般": 0.20},
    "cost":      {"优秀": 0.03, "良好": 0.05, "一般": 0.10},
    "cashflow":  {"优秀": 0.10, "良好": 0.15, "一般": 0.25},
}

TYPE_NAMES = {
    "revenue": "销售收入",
    "cost": "成本费用",
    "cashflow": "现金流",
}


def accuracy_level(deviation_rate, forecast_type):
    """华为预测考核等级判定

    边界规则（严格按 < 判断优秀档）：
        revenue:  <5% 优秀，5-10% 良好，10-20% 一般，>20% 较差
        cost:     <3% 优秀，3-5% 良好，5-10% 一般，>10% 较差
        cashflow: <10% 优秀，10-15% 良好，15-25% 一般，>25% 较差
    """
    thresholds = THRESHOLDS.get(forecast_type, THRESHOLDS["revenue"])
    if deviation_rate < thresholds["优秀"]:
        return "优秀"
    elif deviation_rate <= thresholds["良好"]:
        return "良好"
    elif deviation_rate <= thresholds["一般"]:
        return "一般"
    else:
        return "较差"


def main():
    parser = argparse.ArgumentParser(description="华为预测准确性评估工具")
    parser.add_argument("--forecast", type=float, required=True, help="预测值")
    parser.add_argument("--actual", type=float, required=True, help="实际值")
    parser.add_argument("--type", choices=["revenue", "cost", "cashflow"],
                        default="revenue", help="预测对象类型")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    deviation = abs(args.forecast - args.actual)
    deviation_rate = deviation / args.actual if args.actual else 0
    accuracy = 1 - deviation_rate
    level = accuracy_level(deviation_rate, args.type)

    result = {
        "预测对象": TYPE_NAMES[args.type],
        "预测值": args.forecast,
        "实际值": args.actual,
        "绝对偏差": deviation,
        "偏差率": deviation_rate,
        "准确率": accuracy,
        "考核等级": level,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("=" * 60)
    print("            华为预测准确性评估报告")
    print("=" * 60)
    print(f"预测对象     : {result['预测对象']}")
    print(f"预测值       : {result['预测值']}")
    print(f"实际值       : {result['实际值']}")
    print(f"绝对偏差     : {result['绝对偏差']}")
    print(f"偏差率       : {result['偏差率']:.2%}")
    print(f"准确率       : {result['准确率']:.2%}")
    print(f"考核等级     : {result['考核等级']}")
    print("=" * 60)
    print("【改进建议】")
    if level == "优秀":
        print("  预测质量高，保持当前预测模型和方法。")
    elif level == "良好":
        print("  预测质量良好，可进一步优化模型参数。")
    elif level == "一般":
        print("  预测偏差偏大，建议：")
        print("  1. 检查关键假设是否失效")
        print("  2. 缩短预测更新周期")
        print("  3. 引入滚动预测机制")
    else:
        print("  预测严重偏离，必须复盘，建议：")
        print("  1. 立即开展偏差归因分析（模型/数据/假设/执行）")
        print("  2. 重建预测模型")
        print("  3. 将预测准确性纳入绩效考核")
    print("=" * 60)


if __name__ == "__main__":
    main()