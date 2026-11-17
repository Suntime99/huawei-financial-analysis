#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为财务分析脚本单元测试
========================
覆盖 scripts/ 下全部分析脚本的核心函数：
- golden_triangle.py（金三角诊断）
- budget_variance.py（预算偏差分解）
- duPont.py（杜邦分析）
- forecast_accuracy.py（预测准确性）

用法：
    python -m pytest scripts/tests/test_main_pipeline.py -v
    或
    python scripts/tests/test_main_pipeline.py
"""

import os
import sys
import unittest

# 将 scripts 目录加入导入路径
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import golden_triangle
import budget_variance
import duPont
import forecast_accuracy


class TestGoldenTriangle(unittest.TestCase):
    """金三角诊断测试"""

    def test_growth_score(self):
        self.assertEqual(golden_triangle.growth_score(0.25), 10)
        self.assertEqual(golden_triangle.growth_score(0.15), 7)
        self.assertEqual(golden_triangle.growth_score(0.05), 4)
        self.assertEqual(golden_triangle.growth_score(-0.01), 1)

    def test_profitability_score(self):
        self.assertEqual(golden_triangle.profitability_score(0.25), 10)
        self.assertEqual(golden_triangle.profitability_score(0.15), 7)
        self.assertEqual(golden_triangle.profitability_score(0.08), 4)
        self.assertEqual(golden_triangle.profitability_score(0.03), 1)

    def test_liquidity_score(self):
        self.assertEqual(golden_triangle.liquidity_score(1.5), 10)
        self.assertEqual(golden_triangle.liquidity_score(1.0), 7)
        self.assertEqual(golden_triangle.liquidity_score(0.6), 4)
        self.assertEqual(golden_triangle.liquidity_score(0.3), 1)

    def test_interpret_composite(self):
        self.assertEqual(golden_triangle.interpret_composite(9), "优秀")
        self.assertEqual(golden_triangle.interpret_composite(7), "良好")
        self.assertEqual(golden_triangle.interpret_composite(5), "一般")
        self.assertEqual(golden_triangle.interpret_composite(3), "较差")
        self.assertEqual(golden_triangle.interpret_composite(1), "危机")

    def test_quadrant_healthy(self):
        # 三维度都高 → 健康型
        result = golden_triangle.quadrant_classify(0.15, 0.12, 1.5)
        self.assertEqual(result, "健康型（三角均衡）")

    def test_quadrant_risk(self):
        # 增长高但盈利低、流动性低 → 风险型
        result = golden_triangle.quadrant_classify(0.15, 0.03, 0.3)
        self.assertIn("风险型", result)

    def test_quadrant_crisis(self):
        # 三维度都低 → 危机型
        result = golden_triangle.quadrant_classify(0.01, 0.03, 0.3)
        self.assertEqual(result, "危机型（三角均弱）")

    def test_cross_diagnosis(self):
        self.assertEqual(
            golden_triangle.cross_growth_profit(0.15, 0.12),
            "明星企业（理想状态）"
        )
        self.assertEqual(
            golden_triangle.cross_growth_liquidity(0.15, 0.3),
            "透支增长（需关注现金流）"
        )
        self.assertEqual(
            golden_triangle.cross_profit_liquidity(0.12, 0.3),
            "账面富贵（需加强回款）"
        )

    def test_radar_data(self):
        radar = golden_triangle.radar_data(0.15, 0.12, 0.6)
        self.assertEqual(radar["维度"], ["增长性", "盈利性", "流动性"])
        self.assertEqual(radar["评分"], [7, 7, 4])


class TestBudgetVariance(unittest.TestCase):
    """预算偏差分解测试"""

    def test_revenue_decomposition(self):
        result = budget_variance.analyze_revenue(
            actual_revenue=9500,
            budget_revenue=10000,
            actual_qty=900,
            budget_qty=1000,
            actual_price=10.5,
            budget_price=10,
        )
        # 收入偏差 = -500
        self.assertEqual(result["收入偏差"], -500)
        # 销量偏差 = (900-1000)*10 = -1000
        self.assertEqual(result["销量偏差影响"], -1000)
        # 价格偏差 = (10.5-10)*900 = 450
        self.assertEqual(result["价格偏差影响"], 450)
        # 结构偏差 = -500 - (-1000) - 450 = 50
        self.assertEqual(result["结构偏差影响"], 50)
        # 偏差率 = -5%
        self.assertAlmostEqual(result["偏差率"], -0.05)

    def test_cost_decomposition(self):
        result = budget_variance.analyze_cost(
            actual_qty=110,
            budget_qty=100,
            actual_price=9,
            budget_price=10,
        )
        # 预算成本 = 1000
        self.assertEqual(result["预算成本"], 1000)
        # 实际成本 = 990
        self.assertEqual(result["实际成本"], 990)
        # 成本偏差 = -10
        self.assertEqual(result["成本偏差"], -10)
        # 产量偏差 = (110-100)*10 = 100
        self.assertEqual(result["产量偏差影响"], 100)
        # 单价偏差 = (9-10)*110 = -110
        self.assertEqual(result["单价偏差影响"], -110)
        # 效率偏差 = -10 - 100 - (-110) = 0
        self.assertEqual(result["效率偏差影响"], 0)

    def test_variance_level(self):
        self.assertEqual(budget_variance.variance_level(0.02)[0], "绿色（正常）")
        self.assertEqual(budget_variance.variance_level(0.08)[0], "黄色（关注）")
        self.assertEqual(budget_variance.variance_level(0.15)[0], "橙色（预警）")
        self.assertEqual(budget_variance.variance_level(0.25)[0], "红色（告警）")


class TestDuPont(unittest.TestCase):
    """杜邦分析测试"""

    def test_decompose(self):
        result = duPont.dupont_decompose(
            net_profit=120,
            revenue=1000,
            total_assets=800,
            equity=400,
        )
        # ROE = 120/400 = 30%
        self.assertAlmostEqual(result["ROE"], 0.30)
        # 净利率 = 12%
        self.assertAlmostEqual(result["销售净利率"], 0.12)
        # 总资产周转率 = 1.25
        self.assertAlmostEqual(result["总资产周转率"], 1.25)
        # 权益乘数 = 2.0
        self.assertAlmostEqual(result["权益乘数"], 2.0)

    def test_sensitivity(self):
        base = duPont.dupont_decompose(120, 1000, 800, 400)
        results = duPont.sensitivity_analysis(base, "销售净利率")
        self.assertEqual(len(results), 4)
        # -20% 净利率 → ROE 应下降
        self.assertAlmostEqual(results[0]["新ROE"], 0.30 * 0.8)
        self.assertAlmostEqual(results[0]["ROE变化"], -0.06)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            duPont.dupont_decompose(100, 0, 800, 400)


class TestForecastAccuracy(unittest.TestCase):
    """预测准确性评估测试"""

    def test_accuracy_level_revenue(self):
        # 收入：<5% 优秀，5-10% 良好，10-20% 一般，>20% 较差
        self.assertEqual(forecast_accuracy.accuracy_level(0.03, "revenue"), "优秀")
        self.assertEqual(forecast_accuracy.accuracy_level(0.08, "revenue"), "良好")
        self.assertEqual(forecast_accuracy.accuracy_level(0.15, "revenue"), "一般")
        self.assertEqual(forecast_accuracy.accuracy_level(0.25, "revenue"), "较差")

    def test_accuracy_level_cost(self):
        # 成本：<3% 优秀，3-5% 良好，5-10% 一般，>10% 较差
        self.assertEqual(forecast_accuracy.accuracy_level(0.02, "cost"), "优秀")
        self.assertEqual(forecast_accuracy.accuracy_level(0.04, "cost"), "良好")
        self.assertEqual(forecast_accuracy.accuracy_level(0.08, "cost"), "一般")
        self.assertEqual(forecast_accuracy.accuracy_level(0.12, "cost"), "较差")

    def test_accuracy_level_cashflow(self):
        # 现金流：<10% 优秀，10-15% 良好，15-25% 一般，>25% 较差
        self.assertEqual(forecast_accuracy.accuracy_level(0.08, "cashflow"), "优秀")
        self.assertEqual(forecast_accuracy.accuracy_level(0.12, "cashflow"), "良好")
        self.assertEqual(forecast_accuracy.accuracy_level(0.20, "cashflow"), "一般")
        self.assertEqual(forecast_accuracy.accuracy_level(0.30, "cashflow"), "较差")

    def test_threshold_boundary(self):
        # 边界：5% 偏差在收入类型中应为"良好"（>5% 才算一般）
        self.assertEqual(forecast_accuracy.accuracy_level(0.05, "revenue"), "良好")


if __name__ == "__main__":
    unittest.main()