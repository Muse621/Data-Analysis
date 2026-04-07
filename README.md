# 数据分析实战项目 | Data Analysis Projects

本仓库包含 5 个数据分析实战项目，涵盖探索性分析、商业洞察、用户运营等核心业务场景。

---

## 项目一：Titanic 生存率分析

**数据集**：Kaggle 泰坦尼克号乘客数据

**分析目标**：探索哪些因素影响乘客生存率

**核心方法**：
```python
# 按性别、船舱等级分组计算生存率
print(df.groupby('Sex')['Survived'].mean())           # 女性 74%，男性 18%
print(df.groupby('Pclass')['Survived'].mean())        # 头等舱 62%，二等舱 47%，三等舱 24%
print(df.groupby(['Sex','Pclass'])['Survived'].mean()) # 交叉分析
```

**分析结论**：
- 女性生存率（74%）远高于男性（18%）
- 船舱等级越高，生存率越高
- 头等舱女性生存率最高

**涉及技能**：pandas 分组聚合、交叉表分析

---

## 项目二：Superstore 零售数据分析

**数据集**：全球超市订单数据（Sales, Profit, Region 等字段）

**分析目标**：挖掘销售趋势、高利润品类与亏损原因

**核心方法**：
```python
# 销售额 Top 5 子类别
top5 = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(5)

# 按地区分析利润
region_profit = df.groupby('Region')['Profit'].sum()

# 月度销售趋势
monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()

# 亏损商品识别
loss_products = df[df['Profit'] < 0].groupby('Product Name')['Profit'].sum().sort_values()
```

**分析维度**：
- 销售额排名、利润分析
- 地区对比、时间序列趋势
- 亏损商品定位

**涉及技能**：pandas 数据清洗、分组聚合、时间序列分析

---

## 项目三：RFM 用户价值分析

**数据集**：Online Retail 跨国电商交易数据

**分析目标**：基于 RFM 模型对用户进行分层，识别高价值用户与流失风险用户

**核心方法**：
```python
# 计算 RFM 指标
rfm = df.groupby('CustomerID').agg(
    r = ('InvoiceDate', lambda x: (now - x.max()).days),  # 最近购买距今天数
    f = ('InvoiceNo', 'nunique'),                          # 购买频次
    m = ('total_money', 'sum')                             # 总消费金额
)

# RFM 打分（1-5分）
rfm['R_Score'] = pd.qcut(rfm['r'], q=5, labels=[5,4,3,2,1])  # R越小分数越高
rfm['F_Score'] = pd.qcut(rfm['f'].rank(method='first'), q=5, labels=[1,2,3,4,5])
rfm['M_Score'] = pd.qcut(rfm['m'], q=5, labels=[1,2,3,4,5])

# 用户分层（高价值、流失风险、新客户等）
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
```

**用户分层策略**：
- **高价值用户**（R↑ F↑ M↑）：重点维护，提供VIP服务
- **流失风险用户**（R↓ F↓）：推送召回活动
- **新客户**（R高 F低 M低）：引导复购

**涉及技能**：RFM 模型、四分位数打分、用户分层

---

## 项目四：A/B 测试效果分析

**业务背景**：评估产品界面改动（按钮颜色、文案等）对转化率的影响，判断是否值得全量上线

**核心方法**：
```python
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.power import NormalIndPower

# 样本量校验
effect_size = 2 * (np.arcsin(np.sqrt(p_treat)) - np.arcsin(np.sqrt(p_control)))
required_n = analysis.solve_power(effect_size=effect_size, alpha=0.05, power=0.8)

# 双样本比例 z 检验
z_stat, p_value = proportions_ztest([conv_control, conv_treatment], [n_control, n_treat])

# 95% 置信区间
ci = [diff - 1.96*se, diff + 1.96*se]
```

**输出结果**：
- 转化率对比柱状图（带误差棒）
- 置信区间可视化
- 统计检验报告（用于 Power BI 仪表盘）

**涉及技能**：统计检验、效应量分析、置信区间、可视化

---

## 项目五：Cohort 用户留存分析

**数据集**：UCI Retail 跨国电商交易数据（2010-2011）

**业务背景**：追踪用户首购后的留存行为，识别流失节点并制定召回策略

**核心方法**：
```python
# SQL Cohort 留存率计算
cohort_sql = """
    SELECT a.CohortMonth, a.MonthIndex,
        ROUND(a.active_users / b.cohort_size * 100, 1) AS retention_pct
    FROM (...) a JOIN (...) b ON a.CohortMonth = b.CohortMonth
"""

# 热力图可视化
import seaborn as sns
pivot = cohort_data.pivot_table(index='CohortMonth', columns='MonthIndex', values='retention_pct')
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='Blues')
```

**分析维度**：
- 整体次月留存率评估
- 各 Cohort 留存曲线对比
- 流失最快节点定位

**业务建议**：基于流失节点制定召回策略（第 7/14/30 天邮件触达）

**涉及技能**：MySQL 窗口函数、Cohort 分析、热力图可视化

---

## 项目文件结构

```
├── 项目1代码/     # Titanic 生存率分析
├── 项目2代码/     # Superstore 零售分析
├── 项目3代码/     # RFM 用户价值分析
├── 项目4代码/     # A/B 测试效果分析
└── 项目5代码/     # Cohort 用户留存分析
```

---

## 技能清单

| 类别 | 工具/方法 |
|------|----------|
| 数据处理 | pandas, numpy |
| 统计分析 | statsmodels, scipy |
| 数据库 | MySQL, SQLAlchemy |
| 可视化 | matplotlib, seaborn, Power BI |
| 分析模型 | RFM, Cohort, A/B Test |
| 版本控制 | Git, GitHub |
