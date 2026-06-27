import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 读取全线索原始宽表
df = pd.read_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全线索原始宽表.csv")

# 计算漏斗各层级独立线索量
stage1_total_leads = df["mql_id"].nunique()
stage2_deal_seller = df.dropna(subset=["seller_id"])["mql_id"].nunique()
stage3_create_order = df.dropna(subset=["order_id"])["mql_id"].nunique()
stage4_pay_success = df.dropna(subset=["payment_value"])["mql_id"].nunique()

funnel_data = pd.DataFrame({
    "转化阶段": ["营销线索", "达成合作卖家", "生成订单", "支付完成"],
    "用户数量": [stage1_total_leads, stage2_deal_seller, stage3_create_order, stage4_pay_success]
})
funnel_data["阶段转化率"] = funnel_data["用户数量"].shift(-1) / funnel_data["用户数量"]

# 绘制横向漏斗图
plt.figure(figsize=(10,5))
plt.barh(funnel_data["转化阶段"], funnel_data["用户数量"], color="#A23B72")
plt.title("营销全链路转化漏斗", fontsize=14)
plt.xlabel("线索/客户数量")
# 标注数值与转化率
for idx, val in enumerate(funnel_data["用户数量"]):
    rate = funnel_data["阶段转化率"][idx]
    if not pd.isna(rate):
        text = f"{val} 人 | 下阶段转化率{rate:.1%}"
    else:
        text = f"{val} 人"
    plt.text(val, idx, text, va="center")
plt.tight_layout()
plt.savefig(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\转化漏斗图.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 分渠道漏斗明细
channel_funnel = df.groupby("投放渠道").agg({
    "mql_id": "nunique",
    "seller_id": lambda x: x.notna().sum(),
    "order_id": lambda x: x.notna().sum(),
    "payment_value": lambda x: x.notna().sum()
}).reset_index()
channel_funnel.columns = ["投放渠道","总线索","成交线索","下单线索","支付线索"]

print("===== 分渠道转化漏斗明细 =====")
print(channel_funnel)
channel_funnel.to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\分渠道漏斗数据.csv", index=False, encoding="utf-8-sig")