#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冒烟测试 smoke_test.py
======================
每次采集/分析前快速检查环境可用性（对齐数集采集工具链的冒烟测试机制）：

1. 依赖检查：Python 版本、openpyxl（Excel模板生成需要）
2. 脚本可执行性：逐个调用 6 个脚本的关键路径
3. 示例数据完整性：examples/sample_dashboard_data.csv 存在且列齐全
4. KB/CAP 文件完整性：19个KB文件含编号行、kb-index.md / capabilities.md 存在

退出码：0 全部通过；1 存在失败项。

用法：
    python scripts/smoke_test.py
"""

import importlib.util
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(BASE, "scripts")

passed, failed = 0, 0


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name}  {detail}")


def run(cmd, cwd=BASE):
    """运行命令，返回 (是否成功, 输出)"""
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode == 0, ((r.stdout or "") + (r.stderr or "")).strip()


def main():
    print("=" * 60)
    print("华为财务分析技能包 · 冒烟测试")
    print("=" * 60)

    print("\n[1/4] 依赖检查")
    check("Python >= 3.9", sys.version_info >= (3, 9),
          f"当前 {sys.version.split()[0]}")
    check("openpyxl 已安装", importlib.util.find_spec("openpyxl") is not None,
          "pip install openpyxl")

    print("\n[2/4] 脚本可执行性")
    ok, _ = run([sys.executable, "golden_triangle.py", "--growth", "0.15",
                 "--roe", "0.12", "--ocf-ni", "0.6", "--json"], cwd=SCRIPTS)
    check("golden_triangle.py", ok)

    ok, out = run([sys.executable, "budget_variance.py",
                   "--actual-revenue", "9500", "--budget-revenue", "10000",
                   "--actual-qty", "900", "--budget-qty", "1000",
                   "--actual-price", "10.5", "--budget-price", "10"], cwd=SCRIPTS)
    check("budget_variance.py（收入模式）", ok, out[:120])

    ok, _ = run([sys.executable, "budget_variance.py", "--cost-mode",
                 "--actual-qty", "110", "--budget-qty", "100",
                 "--actual-price", "9", "--budget-price", "10"], cwd=SCRIPTS)
    check("budget_variance.py（成本模式）", ok)

    ok, _ = run([sys.executable, "duPont.py", "--net-profit", "120",
                 "--revenue", "1000", "--total-assets", "800",
                 "--equity", "400"], cwd=SCRIPTS)
    check("duPont.py", ok)

    # 杜邦非法输入应返回退出码2
    r = subprocess.run([sys.executable, "duPont.py", "--net-profit", "120",
                        "--revenue", "0", "--total-assets", "800",
                        "--equity", "400"], cwd=SCRIPTS,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    check("duPont.py 输入校验（退出码2）", r.returncode == 2,
          f"实际退出码 {r.returncode}")

    ok, _ = run([sys.executable, "forecast_accuracy.py",
                 "--forecast", "950", "--actual", "1000",
                 "--type", "revenue"], cwd=SCRIPTS)
    check("forecast_accuracy.py", ok)

    ok, _ = run([sys.executable, "dashboard_generator.py",
                 "--csv", os.path.join(BASE, "examples", "sample_dashboard_data.csv"),
                 "--output", os.path.join(BASE, "examples", "_smoke_dashboard.html")],
                cwd=SCRIPTS)
    smoke_html = os.path.join(BASE, "examples", "_smoke_dashboard.html")
    check("dashboard_generator.py", ok)
    if os.path.exists(smoke_html):
        os.remove(smoke_html)

    ok, _ = run([sys.executable, "generate_excel_templates.py"], cwd=SCRIPTS)
    check("generate_excel_templates.py", ok)

    # 使用统计/复盘（CAP-D-03/04）：指向临时 HOME，避免污染用户真实使用数据
    smoke_home = os.path.join(BASE, "examples", "_smoke_usage_home")
    os.makedirs(smoke_home, exist_ok=True)
    env_smoke = dict(os.environ, HOME=smoke_home, USERPROFILE=smoke_home)
    r = subprocess.run([sys.executable, "usage_tracker.py", "record",
                        "--scenario", "全面诊断",
                        "--capabilities", "golden_triangle:1:1"],
                       cwd=SCRIPTS, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env_smoke)
    check("usage_tracker.py（record）", r.returncode == 0,
          (r.stdout + r.stderr).strip()[:120])
    r = subprocess.run([sys.executable, "insights.py", "rank"],
                       cwd=SCRIPTS, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env_smoke)
    check("insights.py（rank）", r.returncode == 0,
          (r.stdout + r.stderr).strip()[:120])
    r = subprocess.run([sys.executable, "insights.py", "monthly"],
                       cwd=SCRIPTS, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env_smoke)
    check("insights.py（monthly）", r.returncode == 0,
          (r.stdout + r.stderr).strip()[:120])
    # 清理临时数据
    import shutil
    shutil.rmtree(smoke_home, ignore_errors=True)

    print("\n[3/4] 示例数据完整性")
    csv_path = os.path.join(BASE, "examples", "sample_dashboard_data.csv")
    if os.path.exists(csv_path):
        with open(csv_path, encoding="utf-8-sig") as f:
            header = f.readline().strip()
        cols = [c.strip() for c in header.split(",")]
        need = ["指标名称", "类别", "数值", "预算", "单位", "预警阈值"]
        check("sample_dashboard_data.csv 列齐全",
              all(c in cols for c in need),
              f"缺: {[c for c in need if c not in cols]}")
    else:
        check("sample_dashboard_data.csv 存在", False)

    print("\n[4/4] KB/CAP 文件完整性")
    check("kb-index.md 存在", os.path.exists(os.path.join(BASE, "kb-index.md")))
    check("capabilities.md 存在",
          os.path.exists(os.path.join(BASE, "capabilities.md")))
    kb_missing = []
    kb_files = [os.path.join(BASE, "chapters", f"ch{i:02d}-{s}.md")
                for i, s in [
                    (1, "analysis-overview"), (2, "profitability"),
                    (3, "solvency"), (4, "efficiency"), (5, "growth"),
                    (6, "golden-triangle"), (7, "budget-analysis"),
                    (8, "dashboard"), (9, "forecasting"),
                    (10, "report-writing"), (11, "bp-analysis"),
                    (12, "benchmarking"), (13, "huawei-cases"),
                    (14, "industry-adaptation"), (15, "interactive-analysis"),
                    (16, "industry-extension")]]
    for p in kb_files + [os.path.join(BASE, f) for f in
                         ("cheatsheet.md", "patterns.md", "glossary.md")]:
        if not os.path.exists(p):
            kb_missing.append(os.path.basename(p))
        else:
            with open(p, encoding="utf-8") as f:
                head = "".join(f.readlines()[:6])
            if "KB-HFA-" not in head:
                kb_missing.append(os.path.basename(p) + "(缺KB编号)")
    check("19个KB文件均含KB编号", not kb_missing,
          f"缺失: {kb_missing}")

    print("\n" + "=" * 60)
    total = passed + failed
    print(f"冒烟测试完成：{passed}/{total} 通过" + (f"，{failed} 项失败" if failed else ""))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()