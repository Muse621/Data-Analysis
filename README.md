# 数据分析实战项目 | Data Analysis Projects

本仓库包含两个数据分析实战项目，涵盖 A/B 测试与用户留存分析两大核心业务场景。

---

## 项目一：A/B 测试效果分析

### 业务背景
对产品界面改动（如按钮颜色、文案、页面布局）进行对照实验，评估实验组与对照组的转化率差异，判断改动是否值得全量上线。

### 技术栈
- **Python**：`pandas`、`numpy`、`statsmodels`、`matplotlib`
- **可视化**：`matplotlib` 柱状图 + 置信区间可视化
- **统计方法**：双样本比例 z 检验、Cohen's h 效应量、统计功效分析

### 核心流程

**1. 样本量校验**
```python
from statsmodels.stats.power import NormalIndPower
effect_size = 2 * (np.arcsin(np.sqrt(p_treat)) - np.arcsin(np.sqrt(p_control)))
analysis = NormalIndPower()
required_n = analysis.solve_power(effect_size=effect_size, alpha=0.05, power=0.8)
```

**2. 双样本比例 z 检验**
```python
from statsmodels.stats.proportion import proportions_ztest
z_stat, p_value = proportions_ztest([conv_control, conv_treatment], [n_control, n_treat])
```

**3. 95% 置信区间计算**
```python
diff = p_treatment - p_control
se = np.sqrt(p_treatment*(1-p_treatment)/n_treatment + p_control*(1-p_control)/n_control)
ci = [diff - 1.96*se, diff + 1.96*se]
```

### 输出结果
- `ab_comparison.png`：两组转化率对比柱状图（含误差棒）
- `ci_plot.png`：置信区间可视化图
- `ab_result.csv`：检验结果数据表（用于 Power BI 可视化）

### 分析结论
- 统计结论：基于 z 检验 p 值判断差异是否显著
- 业务建议：结合置信区间给出是否上线的决策建议
- 注意事项：样本量不足时的风险提示与后续优化方向

---

## 项目二：Cohort 用户留存分析

### 业务背景
基于跨国电商真实交易数据（UCI Retail Dataset），通过 Cohort 分析追踪用户首购后的留存行为，识别流失节点并提出召回策略。

### 技术栈
- **数据库**：`MySQL` + `SQLAlchemy`
- **Python**：`pandas`、`numpy`、`matplotlib`、`seaborn`
- **分析方法**：SQL 窗口函数 + Python 热力图可视化

### 核心流程

**1. 数据清洗**
```python
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df = df.dropna(subset=['CustomerID'])
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]  # 排除退货
```

**2. SQL Cohort 留存率计算**
```sql
SELECT 
    a.CohortMonth,
    a.MonthIndex,
    a.active_users,
    b.cohort_size,
    ROUND(a.active_users / b.cohort_size * 100, 1) AS retention_pct
FROM (
    SELECT CohortMonth, MonthIndex, COUNT(DISTINCT CustomerID) AS active_users
    FROM user_cohort
    GROUP BY CohortMonth, MonthIndex 
) a
JOIN (
    SELECT CohortMonth, COUNT(DISTINCT CustomerID) AS cohort_size
    FROM user_cohort
    WHERE MonthIndex = 0
    GROUP BY CohortMonth
) b ON a.CohortMonth = b.CohortMonth
```

**3. 热力图可视化**
```python
import seaborn as sns
pivot = cohort_data.pivot_table(index='CohortMonth', columns='MonthIndex', values='retention_pct')
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='Blues', vmin=0, vmax=50)
```

### 输出结果
- `cohort_heatmap.png`：用户月度留存率热力图
- `cohort_result.csv`：留存率数据表

### 分析结论
- 整体次月留存率评估
- 最忠诚 Cohort 识别
- 流失最快的关键节点定位
- 业务建议：基于流失节点制定召回策略（如第 7/14/30 天邮件召回）

---

## 数据可视化

两个项目的分析结果均导出为 CSV 格式，可接入 Power BI 进行交互式仪表盘制作。

### Power BI 可视化示例
详见 [My Resume 作品集网站](https://github.com/Muse621/My_Resume) 中的数据分析实战项目展示。

---

## 工具与技能

| 类别 | 工具 |
|------|------|
| 数据处理 | Python (pandas, numpy) |
| 统计分析 | statsmodels, scipy |
| 数据库 | MySQL, SQLAlchemy |
| 可视化 | matplotlib, seaborn, Power BI |
| 版本控制 | Git, GitHub |
