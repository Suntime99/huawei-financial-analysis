# 华为财务分析技能包

基于《华为财务管理（第7版）》核心框架的系统化财务分析方法论技能包，涵盖从财务报表解读到经营洞察生成的完整分析链条。

> **核心定位：从数据呈现到洞察分析，从事后复盘到事前预测。**

## 特性

- 华为四大能力分析模型（盈利 / 偿债 / 营运 / 发展）
- 财务金三角诊断工具与量化框架
- 预算执行分析完整方法论
- 经营仪表盘（R&A 体系）构建指南
- 从数据到洞察的分析路径
- 财务预测模型与方法
- 财务分析报告标准结构
- **生产型架构**：KB-HFA-01~19 编号知识库（kb-index.md 登记）+ CAP 四层能力矩阵（capabilities.md，20项能力）
- **6个 Python 分析脚本**（金三角/预算偏差/杜邦/预测/仪表盘/Excel生成）
- **质量护栏**：19项单元测试 + 冒烟测试（14项检查）
- **5个 Excel 实操模板**（金三角评分卡/预算跟踪/杜邦拆解/滚动预测/偏差复盘）
- **华为真实财务案例库**（6大案例验证方法论）
- **行业适配**（10大行业差异化指标体系）
- **培训体系**（入门→进阶→实战→专家认证 + 考核题库）

## 目录结构

```
.
├── SKILL.md                       # 技能入口与核心分析框架
├── README.md                      # 项目说明
├── cheatsheet.md                  # 附录A：核心指标速查表
├── glossary.md                    # 附录B：财务分析术语表
├── patterns.md                    # 附录C：财务分析模式库
├── scripts/                       # Python 分析工具
│   ├── golden_triangle.py             # 金三角诊断
│   ├── budget_variance.py             # 预算偏差分解
│   ├── duPont.py                      # 杜邦分析
│   ├── forecast_accuracy.py           # 预测准确性评估
│   ├── dashboard_generator.py         # 经营仪表盘生成（可视化增强版）
│   ├── generate_excel_templates.py    # Excel模板生成
│   └── tests/                         # 单元测试（19个用例）
├── templates/                     # 模板库
│   ├── excel/                         # Excel实操模板（5个）
│   └── reports/                       # 报告模板（月度/季度/专项）
│   ├── 金三角评分卡.xlsx
│   ├── 预算执行跟踪表.xlsx
│   ├── 杜邦分析拆解表.xlsx
│   ├── 滚动预测日历.xlsx
│   └── 预测偏差复盘表.xlsx
├── examples/                      # 示例数据
│   ├── sample_dashboard_data.csv
│   └── sample_dashboard.html
└── chapters/                      # 13 章分主题教程
    ├── ch01-analysis-overview.md      # 第1章 财务分析总论
    ├── ch02-profitability.md          # 第2章 盈利能力分析
    ├── ch03-solvency.md               # 第3章 偿债能力分析
    ├── ch04-efficiency.md             # 第4章 营运能力分析
    ├── ch05-growth.md                 # 第5章 发展能力分析
    ├── ch06-golden-triangle.md        # 第6章 财务金三角综合诊断
    ├── ch07-budget-analysis.md        # 第7章 预算执行分析
    ├── ch08-dashboard.md              # 第8章 经营仪表盘构建
    ├── ch09-forecasting.md            # 第9章 财务预测模型
    ├── ch10-report-writing.md         # 第10章 财务分析报告撰写
    ├── ch11-bp-analysis.md            # 第11章 财务BP数据分析实战
    ├── ch12-benchmarking.md           # 第12章 行业对标分析
    ├── ch13-huawei-cases.md           # 第13章 华为财务案例库
    ├── ch14-industry-adaptation.md    # 第14章 行业适配分析
    ├── ch15-interactive-analysis.md   # 第15章 对话引导·交互式分析
    └── ch16-industry-extension.md     # 第16章 行业适配扩展
├── training/                      # 培训体系
    ├── README.md                   # 四阶段培训总览
    ├── course-outline.md           # 详细课程大纲
    ├── core-lecture.md             # 核心讲义（浓缩版）
    └── assessment-bank.md          # 考核题库
```

## 章节速览

| 章节 | 主题 | 章节 | 主题 |
|------|------|------|------|
| 第1章 | 财务分析总论 | 第8章 | 经营仪表盘构建 |
| 第2章 | 盈利能力分析 | 第9章 | 财务预测模型 |
| 第3章 | 偿债能力分析 | 第10章 | 财务分析报告撰写 |
| 第4章 | 营运能力分析 | 第11章 | 财务BP数据分析实战 |
| 第5章 | 发展能力分析 | 第12章 | 行业对标分析 |
| 第6章 | 财务金三角综合诊断 | 第13章 | 华为财务案例库 |
| 第7章 | 预算执行分析 | 第14章 | 行业适配分析 |
| 第8章 | 经营仪表盘构建 | 第15章 | 对话引导·交互式分析 |
| 第9章 | 财务预测模型 | 第16章 | 行业适配扩展 |
| 第10章 | 财务分析报告撰写 | | |
| 第11章 | 财务BP数据分析实战 | | |
| 第12章 | 行业对标分析 | | |

## 🎓 培训体系（training/）

四阶段学习路径：入门（2h）→ 进阶（8h）→ 实战（16h）→ 专家认证（3h）。

| 文件 | 内容 |
|------|------|
| `training/README.md` | 培训体系总览 + 学习路径图 + 讲师指南 |
| `training/course-outline.md` | 详细课程大纲（10课 + 3实战项目 + 认证） |
| `training/core-lecture.md` | 核心讲义（浓缩版，课堂分发用） |
| `training/assessment-bank.md` | 考核题库（入门20题 + 进阶8题 + 专家综合案例） |

## 快速开始：Python 工具

```bash
# 1. 安装依赖（Excel模板需要）
pip install openpyxl

# 2. 金三角诊断（示例：增长率15%，ROE 12%，现金流/净利润 0.6）
python scripts/golden_triangle.py --growth 0.15 --roe 0.12 --ocf-ni 0.6

# 3. 预算偏差分解（示例：实际收入9500 vs 预算10000）
python scripts/budget_variance.py \
    --actual-revenue 9500 --budget-revenue 10000 \
    --actual-qty 900 --budget-qty 1000 \
    --actual-price 10.5 --budget-price 10

# 4. 杜邦分析（示例：净利润120，收入1000，总资产800，净资产400）
python scripts/duPont.py --net-profit 120 --revenue 1000 --total-assets 800 --equity 400

# 5. 预测准确性评估
python scripts/forecast_accuracy.py --forecast 950 --actual 1000 --type revenue

# 6. 生成经营仪表盘
python scripts/dashboard_generator.py \
    --csv examples/sample_dashboard_data.csv \
    --output examples/sample_dashboard.html

# 7. 生成5个Excel实操模板
python scripts/generate_excel_templates.py
```

## 使用方式

本技能包以 Claude 技能形式使用：

```
/huawei-financial-analysis                    # 加载核心分析框架
/huawei-financial-analysis 盈利能力            # 进入盈利能力分析
/huawei-financial-analysis 金三角诊断          # 进入财务金三角诊断
/huawei-financial-analysis 预算执行            # 进入预算执行分析
/huawei-financial-analysis 预测模型            # 进入财务预测
/huawei-financial-analysis 经营仪表盘          # 进入仪表盘构建
/huawei-financial-analysis 分析报告            # 进入报告撰写
```

## 核心分析框架

### 华为四大能力分析模型

| 能力维度 | 核心指标 | 分析目的 | 对应华为框架 |
|----------|----------|----------|-------------|
| 盈利能力 | 毛利率、净利率、ROE、ROA | 评估赚钱能力 | 财务金三角-盈利性 |
| 偿债能力 | 流动比率、速动比率、资产负债率 | 评估抗风险能力 | 财务金三角-流动性 |
| 营运能力 | 应收账款周转率、存货周转率、总资产周转率 | 评估运营效率 | IFS变革-流程优化 |
| 发展能力 | 销售增长率、利润增长率、资产增长率 | 评估成长潜力 | 财务金三角-增长性 |

### 财务金三角

盈利性（利润）、流动性（现金流）、增长性（销售收入）三角平衡，是企业健康可持续发展的关键。

- **三角均衡**：企业健康，可持续发展
- **增长性过高**：可能透支未来，需关注盈利质量
- **盈利性过高**：可能忽视现金流，存在账面利润风险
- **流动性过高**：可能资金闲置，需关注投资效率

### 预算执行分析框架

```
计划（目标）→ 预算（量化）→ 执行（实际）→ 核算（校验）→ 分析（偏差）→ 调整（优化）→ 计划（新目标）
```

## 🧰 配套工具链

### Python 分析脚本（scripts/）

| 脚本 | 功能 | 对应章节 |
|------|------|---------|
| `golden_triangle.py` | 金三角评分+双维度交叉+八象限分类+雷达图数据 | 第6章 |
| `budget_variance.py` | 预算偏差自动分解（量/价/结构，产量/单价/效率） | 第7章 |
| `duPont.py` | ROE杜邦三因素拆解+敏感性分析 | 第2章 |
| `forecast_accuracy.py` | 预测偏差率/准确率+华为考核等级 | 第9章 |
| `dashboard_generator.py` | 从CSV生成HTML经营仪表盘（红黄绿预警+摘要卡片+金三角雷达图+进度条） | 第8章 |
| `generate_excel_templates.py` | 生成5个Excel实操模板 | 全部 |
| `tests/test_main_pipeline.py` | 单元测试（19个用例覆盖全部脚本） | 全部 |

### 报告模板库（templates/reports/）

| 模板 | 功能 | 对应章节 |
|------|------|---------|
| `monthly-report-template.md` | 月度经营分析（金三角+偏差+风险+下月重点） | 第10章 |
| `quarterly-report-template.md` | 季度战略评估（里程碑+对标+资源配置） | 第10章 |
| `special-report-template.md` | 专项分析（应收账款示例，含5Why根因） | 第10章 |

### Excel 实操模板（templates/excel/）

| 模板 | 功能 | 对应章节 |
|------|------|---------|
| 金三角评分卡.xlsx | 输入三项指标，自动评分+综合评级 | 第6章 |
| 预算执行跟踪表.xlsx | 自动计算偏差率+颜色标记+因素分解 | 第7章 |
| 杜邦分析拆解表.xlsx | 输入三要素，自动拆ROE驱动因素+敏感性分析 | 第2章 |
| 滚动预测日历.xlsx | 12个月滚动预测+准确性汇总 | 第9章 |
| 预测偏差复盘表.xlsx | 预测vs实际对比+偏差归因+改进措施 | 第9章 |

### 华为财务案例库（chapters/ch13-huawei-cases.md）

6大案例验证方法论：IFS变革、金三角平衡、深淘滩低作堰、R&A体系、预算三位一体、预测考核。

## 注意事项

- 财务分析的前提是数据真实准确——"不能反映业务真实状况的财务数据是不准确的"（任正非）
- 分析不是目的，洞察和行动才是——"预测准确与否是检验财务分析价值的试金石"
- 财务分析要深入业务源头——"要追溯到业务环节，从业务源头找出病灶"
- 不同行业、不同发展阶段的企业，分析重点和指标阈值应有所差异
- 华为模式适用于大型企业集团，中小企业需结合自身规模灵活应用
- 运行Python脚本需 `python 3.9+`；生成/使用Excel模板需 `pip install openpyxl`

## 许可证

本项目仅用于学习与内部培训参考。华为财务体系相关内容版权归华为及其相关方所有。

## 贡献

欢迎提交改进建议、新增章节或修正内容。请通过 Pull Request 或 Issue 与我们联系。