import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 读取清洗后标准宽表（仅成交有效用户）
df = pd.read_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全局清洗标准宽表.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# 计算首购同期群、消费年月
df["首购年月"] = df.groupby("customer_id")["order_purchase_timestamp"].transform("min").dt.to_period("M")
df["消费年月"] = df["order_purchase_timestamp"].dt.to_period("M")
df["间隔月数"] = (df["消费年月"] - df["首购年月"]).apply(lambda x: x.n)

# 构建同期群透视表
cohort_df = df.groupby(["首购年月", "间隔月数"])["customer_id"].nunique().reset_index()
cohort_pivot = cohort_df.pivot(index="首购年月", columns="间隔月数", values="customer_id")

# 计算留存率
cohort_size = cohort_pivot.iloc[:,0]
retention_pivot = cohort_pivot.div(cohort_size, axis=0)

# 留存热力图
plt.figure(figsize=(14,8))
sns.heatmap(retention_pivot, annot=True, fmt=".1%", cmap="Blues", vmin=0, vmax=1)
plt.title("用户同期群Cohort留存热力图", fontsize=14)
plt.xlabel("距离首购间隔月")
plt.ylabel("首购同期群")
plt.tight_layout()
plt.savefig(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\cohort_heatmap.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 导出留存数据
retention_pivot.round(4).to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\同期群留存率表.csv", encoding="utf-8-sig")
print("Cohort留存热力图 & 留存表已生成")