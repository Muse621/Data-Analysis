import pandas as pd
import os

# 统一使用原始字符串r""，避免\转义报错
path_raw = r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全线索原始宽表.csv"
path_clean = r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全局清洗标准宽表.csv"
path_user_tag = r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\全量用户标签表.csv"

# 前置文件存在校验，缺失则明确提示
miss_file = []
if not os.path.exists(path_raw):
    miss_file.append("全线索原始宽表.csv")
if not os.path.exists(path_clean):
    miss_file.append("全局清洗标准宽表.csv")
if not os.path.exists(path_user_tag):
    miss_file.append("全量用户标签表.csv")

if len(miss_file) > 0:
    raise FileNotFoundError(f"缺失以下文件，请按顺序运行前置脚本生成：{','.join(miss_file)}")

# 读取两套宽表
df_raw = pd.read_csv(path_raw)
df_clean = pd.read_csv(path_clean)
df_clean["order_purchase_timestamp"] = pd.to_datetime(df_clean["order_purchase_timestamp"])

# 看板1：渠道运营数据源
channel_dashboard = df_raw.groupby("投放渠道").agg({
    "mql_id":"nunique",
    "customer_id":lambda x:x.notna().sum(),
    "payment_value":"sum",
    "order_id":"nunique"
}).reset_index()
channel_dashboard.columns = ["投放渠道","总线索","成交用户数","总营收","订单量"]
channel_dashboard["平均客单价"] = channel_dashboard["总营收"] / channel_dashboard["订单量"]
channel_dashboard.to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\PowerBI_渠道看板.csv", index=False, encoding="utf-8-sig")

# 看板2：商品品类运营数据源
product_dashboard = df_clean.groupby("product_category_name_english").agg({
    "order_id":"nunique",
    "payment_value":"sum",
    "review_score":"mean"
}).reset_index()
product_dashboard.columns = ["商品品类","订单量","销售额","平均评分"]
product_dashboard.to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\PowerBI_商品品类看板.csv", index=False, encoding="utf-8-sig")

# 看板3：月度时序营收数据源
df_clean["年月"] = df_clean["order_purchase_timestamp"].dt.to_period("M")
time_dashboard = df_clean.groupby("年月").agg({
    "customer_id":"nunique",
    "order_id":"nunique",
    "payment_value":"sum"
}).reset_index()
time_dashboard["年月"] = time_dashboard["年月"].astype(str)
time_dashboard.columns = ["年月","下单用户数","订单总量","月度总营收"]
time_dashboard.to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\PowerBI_月度时序看板.csv", index=False, encoding="utf-8-sig")

# 看板4：用户分层看板
user_tag = pd.read_csv(path_user_tag)
user_segment_dashboard = user_tag["用户价值分层"].value_counts().reset_index()
user_segment_dashboard.columns = ["用户分层","用户数量"]
user_segment_dashboard.to_csv(r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\PowerBI_用户分层看板.csv", index=False, encoding="utf-8-sig")

print("==== PowerBI四份看板数据源全部导出完成 ====")
print("1.渠道看板 2.商品品类看板 3.月度时序看板 4.用户分层看板")
print("打开PowerBI直接导入4份csv，即可搭建全维度运营可视化看板")