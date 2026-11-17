#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel 实操模板生成器 generate_excel_templates.py
===============================================
生成华为财务分析技能包配套的 Excel 实操模板：

1. 金三角评分卡模板
2. 预算执行跟踪表模板
3. 杜邦分析拆解表模板
4. 滚动预测日历模板
5. 预测偏差复盘表模板

用法：
    python generate_excel_templates.py

输出到 templates/excel/ 目录。
"""

import os
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# 样式定义
HEADER_FILL = PatternFill(start_color="205081", end_color="205081", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)
TITLE_FONT = Font(bold=True, size=14, color="205081")
SECTION_FONT = Font(bold=True, size=11, color="205081")
THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)
CENTER = Alignment(horizontal="center", vertical="center")
LEFT = Alignment(horizontal="left", vertical="center")
GREEN_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
YELLOW_FILL = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
RED_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
INPUT_FILL = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")


def style_header(ws, row, cols):
    """将一行设为表头样式"""
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = CENTER
        cell.border = THIN_BORDER


def set_widths(ws, widths):
    """设置列宽"""
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def create_golden_triangle(path):
    """金三角评分卡模板"""
    wb = Workbook()
    ws = wb.active
    ws.title = "金三角评分卡"

    ws["A1"] = "华为财务金三角评分卡"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:F1")

    ws["A3"] = "说明：在黄色单元格输入实际值，自动计算评分与综合评级。"
    ws["A3"].font = Font(italic=True, color="888888")

    headers = ["维度", "核心指标", "实际值", "评分（0-10）", "判断标准", "风险信号"]
    for i, h in enumerate(headers, start=1):
        ws.cell(row=5, column=i, value=h)
    style_header(ws, 5, 6)

    rows_data = [
        ("增长性", "销售增长率", ">20%→10分；10-20%→7分；0-10%→4分；<0%→1分", "增长停滞或下滑"),
        ("盈利性", "ROE", ">20%→10分；10-20%→7分；5-10%→4分；<5%→1分", "利润率持续下降"),
        ("流动性", "经营现金流/净利润", ">1.2→10分；0.8-1.2→7分；0.5-0.8→4分；<0.5→1分", "现金流紧张"),
    ]
    for i, (dim, metric, standard, risk) in enumerate(rows_data, start=6):
        ws.cell(row=i, column=1, value=dim).border = THIN_BORDER
        ws.cell(row=i, column=2, value=metric).border = THIN_BORDER
        cell_input = ws.cell(row=i, column=3)
        cell_input.fill = INPUT_FILL
        cell_input.border = THIN_BORDER
        cell_score = ws.cell(row=i, column=4, value=0)
        cell_score.border = THIN_BORDER
        ws.cell(row=i, column=5, value=standard).border = THIN_BORDER
        ws.cell(row=i, column=6, value=risk).border = THIN_BORDER
        ws.cell(row=i, column=1).alignment = CENTER
        ws.cell(row=i, column=2).alignment = CENTER
        ws.cell(row=i, column=5).alignment = LEFT

    # 综合评分
    ws["A10"] = "综合评分"
    ws["A10"].font = SECTION_FONT
    ws["B10"] = "=（D6+D7+D8）/3"
    ws["B10"].border = THIN_BORDER

    ws["A11"] = "综合评级"
    ws["A11"].font = SECTION_FONT
    ws["B11"] = "=IF(A10>=8,\"优秀\",IF(A10>=6,\"良好\",IF(A10>=4,\"一般\",IF(A10>=2,\"较差\",\"危机\"))))"
    ws["B11"].border = THIN_BORDER

    ws["A13"] = "双维度交叉诊断"
    ws["A13"].font = SECTION_FONT
    ws["A14"] = "增长 vs 盈利"
    ws["A15"] = "增长 vs 流动性"
    ws["A16"] = "盈利 vs 流动性"

    set_widths(ws, [18, 20, 16, 12, 42, 24])
    wb.save(path)
    print(f"✅ {path}")


def create_budget_tracking(path):
    """预算执行跟踪表模板"""
    wb = Workbook()
    ws = wb.active
    ws.title = "预算执行跟踪表"

    ws["A1"] = "华为预算执行跟踪表"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:H1")

    ws["A3"] = "说明：填写预算与实际值，自动计算偏差率、等级（绿/黄/橙/红）与因素分解。"
    ws["A3"].font = Font(italic=True, color="888888")

    headers = ["项目", "预算", "实际", "绝对偏差", "相对偏差", "偏差等级", "原因分析", "改进措施"]
    for i, h in enumerate(headers, start=1):
        ws.cell(row=5, column=i, value=h)
    style_header(ws, 5, 8)

    items = ["销售收入", "销售成本", "毛利", "销售费用", "管理费用", "财务费用", "净利润"]
    for i, item in enumerate(items, start=6):
        ws.cell(row=i, column=1, value=item).border = THIN_BORDER
        for c in range(2, 9):
            cell = ws.cell(row=i, column=c)
            cell.border = THIN_BORDER
            if c <= 4:
                cell.fill = INPUT_FILL
        ws.cell(row=i, column=5, value=f"=IF(B{i}=0,\"\",(C{i}-B{i})/B{i})").border = THIN_BORDER
        ws.cell(row=i, column=6, value=f"=IF(ABS(E{i})<=0.05,\"绿·正常\",IF(ABS(E{i})<=0.1,\"黄·关注\",IF(ABS(E{i})<=0.2,\"橙·预警\",\"红·告警\")))").border = THIN_BORDER

    # 因素分解区
    ws["A16"] = "销售收入偏差因素分解"
    ws["A16"].font = SECTION_FONT
    factor_headers = ["因素", "公式", "数值", "责任归属"]
    for i, h in enumerate(factor_headers, start=1):
        ws.cell(row=17, column=i, value=h)
    style_header(ws, 17, 4)

    factors = [
        ("销量偏差", "=(实际销量-预算销量)×预算单价", "销售部门"),
        ("价格偏差", "=(实际单价-预算单价)×实际销量", "定价部门"),
        ("结构偏差", "=收入总偏差-销量偏差-价格偏差", "产品/市场部门"),
    ]
    for i, (name, formula, owner) in enumerate(factors, start=18):
        ws.cell(row=i, column=1, value=name).border = THIN_BORDER
        ws.cell(row=i, column=2, value=formula).border = THIN_BORDER
        ws.cell(row=i, column=3).border = THIN_BORDER
        ws.cell(row=i, column=4, value=owner).border = THIN_BORDER

    set_widths(ws, [16, 12, 12, 12, 12, 12, 20, 20])
    wb.save(path)
    print(f"✅ {path}")


def create_dupont(path):
    """杜邦分析拆解表模板"""
    wb = Workbook()
    ws = wb.active
    ws.title = "杜邦分析"

    ws["A1"] = "华为杜邦分析拆解表"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:D1")

    ws["A3"] = "ROE = 销售净利率 × 总资产周转率 × 权益乘数"
    ws["A3"].font = SECTION_FONT

    headers = ["项目", "数值", "公式", "说明"]
    for i, h in enumerate(headers, start=1):
        ws.cell(row=5, column=i, value=h)
    style_header(ws, 5, 4)

    items = [
        ("净利润", "输入", "利润表净利润", "INPUT"),
        ("销售收入", "输入", "利润表营业收入", "INPUT"),
        ("平均总资产", "输入", "(期初+期末)/2", "INPUT"),
        ("平均净资产", "输入", "(期初+期末)/2", "INPUT"),
        ("销售净利率", "=B6/B7", "净利润/销售收入", "公式"),
        ("总资产周转率", "=B7/B8", "销售收入/平均总资产", "公式"),
        ("权益乘数", "=B8/B9", "平均总资产/平均净资产", "公式"),
        ("ROE", "=B10*B11*B12", "三因素乘积", "公式"),
    ]
    for i, (name, formula, note, kind) in enumerate(items, start=6):
        ws.cell(row=i, column=1, value=name).border = THIN_BORDER
        cell = ws.cell(row=i, column=2, value=formula)
        cell.border = THIN_BORDER
        if kind == "INPUT":
            cell.fill = INPUT_FILL
        ws.cell(row=i, column=3, value=note).border = THIN_BORDER
        ws.cell(row=i, column=4, value=kind).border = THIN_BORDER

    ws["A15"] = "敏感性分析"
    ws["A15"].font = SECTION_FONT
    sens_headers = ["因素变动", "新ROE", "ROE变化"]
    for i, h in enumerate(sens_headers, start=1):
        ws.cell(row=16, column=i, value=h)
    style_header(ws, 16, 3)
    for j, pct in enumerate([-0.2, -0.1, 0.1, 0.2]):
        ws.cell(row=17 + j, column=1, value=f"销售净利率 {pct:+.0%}").border = THIN_BORDER
        ws.cell(row=17 + j, column=2, value=f"=B10*(1+{pct})*B11*B12").border = THIN_BORDER
        ws.cell(row=17 + j, column=3, value=f"=B{18+j}-B13").border = THIN_BORDER

    set_widths(ws, [16, 20, 24, 10])
    wb.save(path)
    print(f"✅ {path}")


def create_rolling_forecast(path):
    """滚动预测日历模板"""
    wb = Workbook()
    ws = wb.active
    ws.title = "滚动预测日历"

    ws["A1"] = "华为滚动预测日历（12个月滚动）"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:F1")

    ws["A3"] = "说明：每月更新全年预测，预测窗口始终覆盖未来12个月。黄色为当月新增列。"
    ws["A3"].font = Font(italic=True, color="888888")

    headers = ["月份", "上月预测", "本月预测", "实际值", "偏差率", "预测准确性等级"]
    for i, h in enumerate(headers, start=1):
        ws.cell(row=5, column=i, value=h)
    style_header(ws, 5, 6)

    months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    for i, m in enumerate(months, start=6):
        ws.cell(row=i, column=1, value=m).border = THIN_BORDER
        for c in range(2, 7):
            cell = ws.cell(row=i, column=c)
            cell.border = THIN_BORDER
            if c <= 4:
                cell.fill = INPUT_FILL
        ws.cell(row=i, column=5, value=f"=IF(D{i}=0,\"\",ABS(C{i}-D{i})/D{i})").border = THIN_BORDER
        ws.cell(row=i, column=6, value=f"=IF(E{i}=\"\",\"\",IF(E{i}<=0.05,\"优秀\",IF(E{i}<=0.1,\"良好\",IF(E{i}<=0.2,\"一般\",\"较差\"))))").border = THIN_BORDER

    ws["A20"] = "全年预测准确性汇总"
    ws["A20"].font = SECTION_FONT
    ws["A21"] = "平均偏差率"
    ws["B21"] = "=AVERAGE(E6:E17)"
    ws["B21"].border = THIN_BORDER
    ws["A22"] = "平均准确率"
    ws["B22"] = "=1-AVERAGE(E6:E17)"
    ws["B22"].border = THIN_BORDER

    set_widths(ws, [12, 12, 12, 12, 12, 18])
    wb.save(path)
    print(f"✅ {path}")


def create_forecast_review(path):
    """预测偏差复盘表模板"""
    wb = Workbook()
    ws = wb.active
    ws.title = "预测偏差复盘"

    ws["A1"] = "华为预测偏差复盘表"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:G1")

    headers = ["预测对象", "预测值", "实际值", "偏差率", "偏差原因分类", "根因说明", "改进措施"]
    for i, h in enumerate(headers, start=1):
        ws.cell(row=5, column=i, value=h)
    style_header(ws, 5, 7)

    for i in range(6, 16):
        for c in range(1, 8):
            cell = ws.cell(row=i, column=c)
            cell.border = THIN_BORDER
            if c <= 3:
                cell.fill = INPUT_FILL
        ws.cell(row=i, column=4, value=f"=IF(C{i}=0,\"\",ABS(B{i}-C{i})/C{i})").border = THIN_BORDER

    # 偏差原因分类说明
    ws["A17"] = "偏差原因分类"
    ws["A17"].font = SECTION_FONT
    reasons = ["模型偏差：预测模型选择不当", "数据偏差：历史数据不准确",
               "假设偏差：关键假设发生变化", "执行偏差：实际执行与计划不符"]
    for i, r in enumerate(reasons, start=18):
        ws.cell(row=i, column=1, value=r).border = THIN_BORDER

    set_widths(ws, [16, 12, 12, 12, 16, 24, 24])
    wb.save(path)
    print(f"✅ {path}")


def main(out_dir=None):
    if out_dir is None:
        out_dir = os.path.join(os.path.dirname(__file__), "..", "templates", "excel")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    print("生成华为财务分析 Excel 实操模板：")
    create_golden_triangle(os.path.join(out_dir, "金三角评分卡.xlsx"))
    create_budget_tracking(os.path.join(out_dir, "预算执行跟踪表.xlsx"))
    create_dupont(os.path.join(out_dir, "杜邦分析拆解表.xlsx"))
    create_rolling_forecast(os.path.join(out_dir, "滚动预测日历.xlsx"))
    create_forecast_review(os.path.join(out_dir, "预测偏差复盘表.xlsx"))
    print("\n全部模板生成完毕！")
    print(f"输出目录：{out_dir}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="生成华为财务分析Excel实操模板")
    p.add_argument("--out-dir", default=None,
                   help="输出目录（默认：项目内 templates/excel）")
    args = p.parse_args()
    main(args.out_dir)