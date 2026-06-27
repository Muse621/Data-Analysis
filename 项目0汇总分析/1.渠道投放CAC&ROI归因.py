import matplotlib
# 无界面后端，防止多脚本运行卡死
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 中文乱码设置
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 读取全线索原始宽表（已内置is_order字段）
df = pd.read_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全线索原始宽表.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# 模拟各渠道投放成本（可替换真实预算）
channel_cost = {
    "unknown": 12000,
    "organic_search": 28000,
    "paid_search": 45000,
    "social": 32000,
    "email": 18000,
    "display": 22000
}
df["投放成本"] = df["投放渠道"].map(channel_cost)

# 兼容低版本pandas聚合写法
channel_metric = df.groupby("投放渠道").agg({
    "mql_id": "nunique",
    "is_order": "sum",
    "投放成本": "mean",
    "payment_value": "sum"
}).reset_index()
# 手动重命名列
channel_metric.columns = ["投放渠道","总线索数","成交线索数","渠道总投放成本","渠道总收入"]

# 衍生核心指标
channel_metric["线索转化率"] = channel_metric["成交线索数"] / channel_metric["总线索数"]
channel_metric["CAC单线索获客成本"] = channel_metric["渠道总投放成本"] / channel_metric["总线索数"]
channel_metric["成交CAC获客成本"] = channel_metric["渠道总投放成本"] / channel_metric["成交线索数"]
channel_metric["ROI投资回报率"] = channel_metric["渠道总收入"] / channel_metric["渠道总投放成本"]

# ROI可视化柱状图
plt.figure(figsize=(12,6))
bars = plt.bar(channel_metric["投放渠道"], channel_metric["ROI投资回报率"], color="#2E86AB")
plt.title("各投放渠道ROI投资回报率", fontsize=14)
plt.xlabel("投放渠道")
plt.ylabel("ROI倍数")
plt.xticks(rotation=30)
# 数值标注
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x()+bar.get_width()/2, height, f"{height:.2f}", ha="center", va="bottom")
plt.tight_layout()
# 保存图片，不弹窗
plt.savefig(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\渠道ROI图表.png", dpi=150, bbox_inches="tight")
# 释放画布内存，防止卡顿
plt.close("all")

# 输出&导出结果
print("===== 渠道CAC&ROI归因全量指标 =====")
print(channel_metric.round(2))
channel_metric.to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\渠道ROI归因结果.csv", index=False, encoding="utf-8-sig")