---
name: huawei-financial-analysis
description: "华为财务分析技能（生产型，KB+CAP四层架构）——基于《华为财务管理（第7版）》核心框架，19项KB编号知识库+22项CAP能力矩阵，提供系统化财务分析方法论、华为四大能力分析模型、财务金三角诊断工具、预算执行分析框架、经营仪表盘构建指南、配套Python分析脚本与Excel实操模板、使用统计与复盘机制、培训体系与考核题库，以及从数据到洞察的完整分析路径。"
version: V2.1-20261118
---

# 华为财务分析技能

## 概述

本技能基于《华为财务管理（第7版）》核心框架，将华为财经管理体系中的分析方法论提炼为可直接应用的财务分析工具。涵盖从财务报表解读到经营洞察生成的完整分析链条，帮助企业财务人员建立系统化、结构化的分析能力。

核心定位：**从数据呈现到洞察分析，从事后复盘到事前预测**。

## 触发条件

- 用户需要进行财务分析、经营分析、报表分析
- 用户询问华为财务分析方法论、分析框架
- 用户需要构建经营仪表盘、财务指标体系
- 用户询问财务预测、预算执行分析
- 用户需要盈利能力、偿债能力、营运能力分析
- 用户询问如何从财务数据中发现业务问题
- 用户需要财务分析报告模板或分析思路
- 用户询问任正非"预测是管理的灵魂"如何落地
- 用户需要财务金三角诊断工具
- 用户询问财务BP如何做数据分析

## 技能能力

- 提供华为四大能力分析模型（盈利/偿债/营运/发展）
- 提供财务金三角诊断框架和量化工具
- 提供预算执行分析的完整方法论
- 提供经营仪表盘构建指南
- 提供从数据到洞察的分析路径
- 提供财务预测模型和方法
- 提供财务分析报告的标准结构
- 提供配套 Python 分析脚本（金三角/预算偏差/杜邦/预测/仪表盘/Excel生成）
- 提供 Excel 实操模板（金三角评分卡/预算跟踪/杜邦拆解/滚动预测/偏差复盘）
- 提供华为真实财务案例库（6大案例验证方法论）
- 提供行业适配分析（10大行业差异化指标体系）
- 提供对话引导协议（场景化交互式分析流程）
- 提供报告模板库（月度/季度/专项三类可填写模板）
- 提供四阶段培训体系与考核题库

## 核心分析框架

### 框架一：华为四大能力分析模型

| 能力维度 | 核心指标 | 分析目的 | 对应华为框架 |
|----------|----------|----------|-------------|
| 盈利能力 | 毛利率、净利率、ROE、ROA | 评估赚钱能力 | 财务金三角-盈利性 |
| 偿债能力 | 流动比率、速动比率、资产负债率 | 评估抗风险能力 | 财务金三角-流动性 |
| 营运能力 | 应收账款周转率、存货周转率、总资产周转率 | 评估运营效率 | IFS变革-流程优化 |
| 发展能力 | 销售增长率、利润增长率、资产增长率 | 评估成长潜力 | 财务金三角-增长性 |

### 框架二：财务金三角诊断工具

```
        增长性（销售收入）
              /\
             /  \
            /    \
           /  平衡  \
          /    区    \
         /____________\
    盈利性 ———————— 流动性
    （利润）          （现金流）
```

**诊断规则**：
- 三角均衡：企业健康，可持续发展
- 增长性过高：可能透支未来，需关注盈利质量
- 盈利性过高：可能忽视现金流，存在账面利润风险
- 流动性过高：可能资金闲置，需关注投资效率

### 框架三：预算执行分析框架

```
计划（目标）→ 预算（量化）→ 执行（实际）→ 核算（校验）→ 分析（偏差）→ 调整（优化）→ 计划（新目标）
```

**分析要点**：
1. 对比分析：实际 vs 预算 vs 同期 vs 行业
2. 结构分析：收入结构、成本结构、费用结构
3. 趋势分析：关键指标的长期变化趋势
4. 因素分析：影响偏差的关键因素

### 框架四：经营仪表盘（R&A体系）

华为经营仪表盘的核心是**R&A（Reporting & Analysis）体系**，通过分层报告实现管理穿透：

| 层级 | 报告类型 | 频率 | 受众 | 核心内容 |
|------|----------|------|------|----------|
| 战略层 | 经营分析报告 | 季度/年度 | 高管 | 金三角平衡、战略偏差 |
| 管理层 | 管理报表 | 月度 | 中层 | 预算执行、关键指标 |
| 执行层 | 运营报表 | 周/日 | 一线 | 业务数据、异常预警 |

## 章节索引

> 全部知识文件已编号（KB-HFA-01~19），登记索引见 `kb-index.md`；能力矩阵见 `capabilities.md`。

| 章节 | 主题 | 文件 |
|------|------|------|
| 第1章 | 财务分析总论——从数据到洞察 | chapters/ch01-analysis-overview.md |
| 第2章 | 盈利能力分析——赚钱能力诊断 | chapters/ch02-profitability.md |
| 第3章 | 偿债能力分析——抗风险能力评估 | chapters/ch03-solvency.md |
| 第4章 | 营运能力分析——运营效率度量 | chapters/ch04-efficiency.md |
| 第5章 | 发展能力分析——成长潜力预判 | chapters/ch05-growth.md |
| 第6章 | 财务金三角综合诊断 | chapters/ch06-golden-triangle.md |
| 第7章 | 预算执行分析——计划与现实的偏差 | chapters/ch07-budget-analysis.md |
| 第8章 | 经营仪表盘构建——R&A体系落地 | chapters/ch08-dashboard.md |
| 第9章 | 财务预测模型——预测是管理的灵魂 | chapters/ch09-forecasting.md |
| 第10章 | 财务分析报告撰写——从数字到故事 | chapters/ch10-report-writing.md |
| 第11章 | 财务BP数据分析实战 | chapters/ch11-bp-analysis.md |
| 第12章 | 行业对标分析——找到差距与方向 | chapters/ch12-benchmarking.md |
| 第13章 | 华为财务案例库——用真实数据验证方法论 | chapters/ch13-huawei-cases.md |
| 第14章 | 行业适配分析——从通用框架到行业特色 | chapters/ch14-industry-adaptation.md |
| 第15章 | 对话引导——场景化交互式分析流程 | chapters/ch15-interactive-analysis.md |
| 第16章 | 行业适配扩展——建筑/金融/教育/医药/互联网 | chapters/ch16-industry-extension.md |

## 配套工具

### Python 分析脚本（scripts/）

| 脚本 | 功能 | 用法 |
|------|------|------|
| `golden_triangle.py` | 金三角评分+双维度交叉+八象限分类+雷达图数据 | `python scripts/golden_triangle.py --growth 0.15 --roe 0.12 --ocf-ni 0.6` |
| `budget_variance.py` | 预算偏差自动分解（量/价/结构，产量/单价/效率） | `python scripts/budget_variance.py --actual-revenue 9500 --budget-revenue 10000 ...` |
| `duPont.py` | ROE杜邦三因素拆解+敏感性分析 | `python scripts/duPont.py --net-profit 120 --revenue 1000 --total-assets 800 --equity 400` |
| `forecast_accuracy.py` | 预测偏差率/准确率+华为考核等级 | `python scripts/forecast_accuracy.py --forecast 950 --actual 1000 --type revenue` |
| `dashboard_generator.py` | 从CSV生成HTML经营仪表盘（红黄绿预警+摘要卡片+金三角雷达图+进度条） | `python scripts/dashboard_generator.py --csv examples/sample_dashboard_data.csv --output dashboard.html` |
| `generate_excel_templates.py` | 生成5个Excel实操模板 | `python scripts/generate_excel_templates.py` |
| 单元测试 | 覆盖全部脚本核心逻辑（19个测试用例） | `python scripts/tests/test_main_pipeline.py` |
| `smoke_test.py` | 冒烟测试：依赖/脚本/示例数据/KB-CAP完整性（14项检查） | `python scripts/smoke_test.py` |
| `add_kb_numbers.py` | 知识库批量编号（幂等，重跑自动跳过） | `python scripts/add_kb_numbers.py` |
| `usage_tracker.py` | 使用统计跟踪器（CAP-D-03，双维度统计，JSONL本地存储） | `python scripts/usage_tracker.py record --scenario 全面诊断 --capabilities "golden_triangle:1:1"` |
| `insights.py` | 使用洞察与复盘（CAP-D-04，排行/退化预警/月度/季度复盘） | `python scripts/insights.py monthly` |

### Excel 实操模板（templates/excel/）

| 模板 | 功能 |
|------|------|
| 金三角评分卡.xlsx | 输入三项指标，自动评分+综合评级 |
| 预算执行跟踪表.xlsx | 自动计算偏差率+颜色标记+因素分解 |
| 杜邦分析拆解表.xlsx | 输入三要素，自动拆ROE驱动因素+敏感性分析 |
| 滚动预测日历.xlsx | 12个月滚动预测+准确性汇总 |
| 预测偏差复盘表.xlsx | 预测vs实际对比+偏差归因+改进措施 |

### 示例数据（examples/）

- `sample_dashboard_data.csv`：经营仪表盘示例数据
- `sample_dashboard.html`：生成的示例仪表盘

### 报告模板库（templates/reports/）

| 模板 | 适用场景 | 频率 |
|------|---------|------|
| `monthly-report-template.md` | 月度经营分析（金三角+偏差+风险+下月重点） | 月度 |
| `quarterly-report-template.md` | 季度战略评估（里程碑+对标+资源配置） | 季度 |
| `special-report-template.md` | 专项分析（应收账款示例，含5Why根因） | 按需 |

## 培训体系（training/）

| 文件 | 内容 |
|------|------|
| `training/README.md` | 四阶段培训体系总览（入门/进阶/实战/专家） |
| `training/course-outline.md` | 详细课程大纲（10课+3实战项目+认证） |
| `training/core-lecture.md` | 核心讲义（浓缩版，适合课堂分发） |
| `training/assessment-bank.md` | 考核题库（入门20题+进阶8题+专家综合案例） |

## 架构与知识库索引

| 文件 | 内容 |
|------|------|
| `kb-index.md` | KB-HFA-01~19 知识库登记索引（编号/依赖/更新频率/变更历史） |
| `capabilities.md` | CAP 四层能力矩阵（A场景识别/B工具执行/C工程策略/D平台治理，22项能力登记） |

## 附录

- **附录A**：华为财务分析核心指标速查表（cheatsheet.md）
- **附录B**：财务分析术语表（glossary.md）
- **附录C**：财务分析模式库——从场景到方法（patterns.md）

## 使用方式

```
/huawei-financial-analysis                    # 加载核心分析框架
/huawei-financial-analysis 盈利能力            #  dive into 盈利能力分析
/huawei-financial-analysis 金三角诊断          #  dive into 财务金三角诊断
/huawei-financial-analysis 预算执行            #  dive into 预算执行分析
/huawei-financial-analysis 预测模型            #  dive into 财务预测
/huawei-financial-analysis 经营仪表盘          #  dive into 仪表盘构建
/huawei-financial-analysis 分析报告            #  dive into 报告撰写
```

## 注意事项

- 财务分析的前提是数据真实准确——"不能反映业务真实状况的财务数据是不准确的"（任正非）
- 分析不是目的，洞察和行动才是——"预测准确与否是检验财务分析价值的试金石"
- 财务分析要深入业务源头——"要追溯到业务环节，从业务源头找出病灶"
- 不同行业、不同发展阶段的企业，分析重点和指标阈值应有所差异
- 华为模式适用于大型企业集团，中小企业需结合自身规模灵活应用
- 脚本与模板依赖：运行Python脚本需 `python 3.9+`；生成/使用Excel模板需 `pip install openpyxl`

## 依赖安装

```bash
pip install openpyxl   # Excel模板生成（脚本无需额外依赖，仅用标准库）
```
