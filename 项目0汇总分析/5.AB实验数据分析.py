import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全局清洗标准宽表.csv")

# AB分组：A组自然流量organic_search / B组付费搜索paid_search
group_a = df[df["投放渠道"]=="organic_search"]["payment_value"].dropna()
group_b = df[df["投放渠道"]=="paid_search"]["payment_value"].dropna()

# 基础指标对比
ab_summary = pd.DataFrame({
    "组别":["A组自然流量","B组付费搜索"],
    "样本量":[len(group_a), len(group_b)],
    "客单价均值":[group_a.mean(), group_b.mean()],
    "客单价中位数":[group_a.median(), group_b.median()]
})
print("===== AB分组基础指标 =====")
print(ab_summary)

# 独立样本T检验
t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)
print(f"\nT检验统计量：{t_stat:.3f}，P值：{p_value:.4f}")
if p_value < 0.05:
    print("结论：两组客单价存在统计学显著差异")
else:
    print("结论：两组客单价无显著差异")

# 箱线图对比分布
plt.figure(figsize=(8,5))
plt.boxplot([group_a, group_b], labels=["A组自然流量","B组付费搜索"])
plt.title("AB实验客单价分布对比")
plt.ylabel("订单支付金额")
plt.tight_layout()
plt.savefig(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\AB实验箱线图.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 导出实验报告
ab_summary["T检验P值"] = p_value
ab_summary.to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\AB实验分析报告.csv", index=False, encoding="utf-8-sig")