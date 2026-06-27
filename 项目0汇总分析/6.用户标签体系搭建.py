import pandas as pd
import numpy as np

# 读取清洗后宽表
df = pd.read_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全局清洗标准宽表.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# 内置计算RFM，不再读取外部csv文件
snapshot_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
rfm = df.groupby("customer_id").agg({
    "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
    "order_id": "nunique",
    "payment_value": "sum"
}).reset_index()
rfm.columns = ["customer_id","R最近消费间隔","F消费频次","M总消费金额"]

# RFM打分分层
rfm["R分"] = pd.qcut(rfm["R最近消费间隔"], 5, labels=[5,4,3,2,1])
rfm["F分"] = pd.qcut(rfm["F消费频次"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["M分"] = pd.qcut(rfm["M总消费金额"], 5, labels=[1,2,3,4,5])
rfm["RFM分层码"] = rfm["R分"].astype(str) + rfm["F分"].astype(str) + rfm["M分"].astype(str)

# 用户分层规则
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

# 合并用户基础数据与RFM分层
user_label = df.merge(rfm[["customer_id","用户价值分层"]], on="customer_id", how="left").drop_duplicates(subset=["customer_id"])

# 标签1：地域分层
def area_tag(state):
    if state in ["SP","RJ","MG"]:
        return "东南核心经济区"
    elif state in ["PR","SC","RS"]:
        return "南部区域"
    else:
        return "其他区域"
user_label["地域标签"] = user_label["customer_state"].apply(area_tag)

# 标签2：用户偏好一级品类
top_cat = df.groupby(["customer_id","product_category_name_english"])["order_id"].nunique().reset_index()
top_cat = top_cat.sort_values(["customer_id","order_id"], ascending=[True,False]).drop_duplicates(subset=["customer_id"])
top_cat.columns = ["customer_id","偏好一级品类","购买次数"]
user_label = user_label.merge(top_cat[["customer_id","偏好一级品类"]], on="customer_id", how="left")

# 标签3：满意度分层
def score_tag(score):
    if score >=4:
        return "高满意用户"
    elif score ==3:
        return "中性用户"
    else:
        return "低满意投诉风险"
user_label["满意度标签"] = user_label["review_score"].apply(score_tag)

# 标签4：获客渠道标签
user_label["获客渠道标签"] = user_label["投放渠道"]

# 整合最终用户标签表
final_user_tag = user_label[["customer_id","用户价值分层","地域标签","偏好一级品类","满意度标签","获客渠道标签"]].drop_duplicates()

# 导出全量用户标签
final_user_tag.to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\全量用户标签表.csv", index=False, encoding="utf-8-sig")
print("用户标签体系构建完成，前10条样本：")
print(final_user_tag.head(10))