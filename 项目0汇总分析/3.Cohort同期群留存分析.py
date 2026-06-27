import matplotlib
# 无界面后端，防止多脚本运行卡死
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 中文乱码、负号设置
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 读取清洗后标准宽表
df = pd.read_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全局清洗标准宽表.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# 去重：同一客户同一订单仅保留一行，消除多商品重复行干扰
df_distinct = df.drop_duplicates(subset=["customer_id", "order_id"])

# 1. 计算首购同期群、消费年月
df_distinct["首购年月"] = df_distinct.groupby("customer_id")["order_purchase_timestamp"].transform("min").dt.to_period("M")
df_distinct["消费年月"] = df_distinct["order_purchase_timestamp"].dt.to_period("M")

# 2. 计算距离首购间隔月份
df_distinct["间隔月数"] = (df_distinct["消费年月"] - df_distinct["首购年月"]).apply(lambda x: x.n)

# 3. 分组统计每个同期群、每个间隔月的独立用户数
cohort_df = df_distinct.groupby(["首购年月", "间隔月数"])["customer_id"].nunique().reset_index()

# 4. 生成透视表：行=首购月份，列=间隔月，值=用户数量
cohort_pivot = cohort_df.pivot(index="首购年月", columns="间隔月数", values="customer_id")

# 5. 以首月用户总数为分母，计算留存率
cohort_base = cohort_pivot.iloc[:, 0]
retention_pivot = cohort_pivot.div(cohort_base, axis=0)

# 6. 绘制热力图（更换红绿配色，0留存显示红色，不再纯白看不见）
plt.figure(figsize=(14, 8))
sns.heatmap(
    retention_pivot,
    annot=True,
    fmt=".1%",
    cmap="RdYlGn",  # 红=0留存，绿=100%留存
    vmin=0,
    vmax=1,
    linewidths=0.4
)
plt.title("用户同期群Cohort留存热力图", fontsize=14)
plt.xlabel("距离首购间隔月")
plt.ylabel("首购同期群")
plt.tight_layout()

# 保存图片，不弹窗
plt.savefig(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\cohort_heatmap.png", dpi=150, bbox_inches="tight")
# 释放画布内存，避免多脚本卡死
plt.close("all")

# 导出留存率明细表格
retention_pivot.round(4).to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\同期群留存率表.csv", encoding="utf-8-sig")
print("Cohort留存热力图 & 留存明细表格已生成")
print("业务备注：Olist数据集所有用户仅1单，无复购，次月留存全部为0")

#本数据集内全部用户仅完成单次下单，无复购订单，因此首购次月及之后用户留存率为 0，该热力图仅演示 Cohort 计算逻辑，不代表真实复购表现。