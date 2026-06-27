import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全局清洗标准宽表.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# RFM基准日期：数据集最后一日+1天
snapshot_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

# 计算R/F/M三指标
rfm = df.groupby("customer_id").agg({
    "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
    "order_id": "nunique",
    "payment_value": "sum"
}).reset_index()
rfm.columns = ["customer_id","R最近消费间隔","F消费频次","M总消费金额"]

# 5档分层打分，R反向打分
rfm["R分"] = pd.qcut(rfm["R最近消费间隔"], 5, labels=[5,4,3,2,1])
rfm["F分"] = pd.qcut(rfm["F消费频次"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["M分"] = pd.qcut(rfm["M总消费金额"], 5, labels=[1,2,3,4,5])
rfm["RFM分层码"] = rfm["R分"].astype(str) + rfm["F分"].astype(str) + rfm["M分"].astype(str)

# 用户价值分层规则
def user_segment(code):
    r,f,m = int(code[0]), int(code[1]), int(code[2])
    if r>=4 and f>=4 and m>=4:
        return "高价值核心用户"
    elif r>=3 and f>=3 and m>=3:
        return "潜力增长用户"
    elif r<=2 and f>=3:
        return "沉睡高消费用户"
    elif r>=4 and f<=2:
        return "新客一次性用户"
    else:
        return "低价值流失风险用户"
rfm["用户价值分层"] = rfm["RFM分层码"].apply(user_segment)

# 分层饼图可视化
seg_count = rfm["用户价值分层"].value_counts()
plt.figure(figsize=(10,5))
plt.pie(seg_count.values, labels=seg_count.index, autopct="%.1f%%")
plt.title("RFM用户价值分层占比", fontsize=14)
plt.tight_layout()
plt.savefig(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\RFM分层饼图.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 导出RFM分层结果
rfm.to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\RFM用户分层结果.csv", index=False, encoding="utf-8-sig")
print("RFM分层完成，用户分层分布：")
print(seg_count)