import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 解决matplotlib中文乱码、负号显示问题
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 统一数据集根路径
path_root = r'D:\LI YUTONG\Documents\My Projects\Data-Analysis\数据集\项目0数据集'

# ===================== 第一步：读取所有原始表 + 单表独立清洗（核心改动：清洗前置） =====================
## 1. 营销线索表 leads 单表清洗
leads = pd.read_csv(f"{path_root}\\olist_marketing_qualified_leads_dataset.csv")
# 只保留关键字段、去重、渠道空值预处理
leads = leads[["mql_id", "origin"]].drop_duplicates(subset=["mql_id"])
leads["origin"] = leads["origin"].fillna("unknown")
leads = leads.rename(columns={"origin": "投放渠道"})

## 2. 成交表 deals 单表清洗
deals = pd.read_csv(f"{path_root}\\olist_closed_deals_dataset.csv")
deals = deals[["mql_id", "seller_id"]].drop_duplicates(subset=["mql_id"])

## 3. 支付表 pay 单表清洗 + 聚合（提前聚合，避免合并后冗余）
pay = pd.read_csv(f"{path_root}\\olist_order_payments_dataset.csv")
# 过滤支付金额异常值（≤0直接剔除）
pay = pay[pay["payment_value"] > 0]
# 预聚合单订单总支付金额
pay_sum = pay.groupby("order_id")["payment_value"].sum().reset_index()

## 4. 订单主表 orders 单表清洗
orders = pd.read_csv(f"{path_root}\\olist_orders_dataset.csv")
# 时间格式提前转换
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
# 筛选核心字段、去重订单
orders = orders[["order_id", "customer_id", "order_purchase_timestamp", "order_status"]].drop_duplicates(subset=["order_id"])
# 合并预聚合支付金额
orders = pd.merge(orders, pay_sum, on="order_id", how="left")

## 5. 订单商品表 order_items 单表清洗
order_items = pd.read_csv(f"{path_root}\\olist_order_items_dataset.csv")
# 去重，保留三关联主键
order_items = order_items[["seller_id", "order_id", "product_id"]].drop_duplicates()

## 6. 商品表 products 单表清洗
products = pd.read_csv(f"{path_root}\\olist_products_dataset.csv")
# 过滤尺寸、重量异常为0/负数的无效商品
products = products[
    (products["product_weight_g"] > 0) &
    (products["product_length_cm"] > 0) &
    (products["product_height_cm"] > 0) &
    (products["product_width_cm"] > 0)
]
products = products[["product_id", "product_category_name", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]].drop_duplicates(subset=["product_id"])

## 7. 品类翻译表 cat_trans 单表清洗
cat_trans = pd.read_csv(f"{path_root}\\product_category_name_translation.csv")
cat_trans = cat_trans.drop_duplicates(subset=["product_category_name"])

## 8. 客户表 customers 单表清洗
customers = pd.read_csv(f"{path_root}\\olist_customers_dataset.csv")
customers = customers[["customer_id", "customer_city", "customer_state"]].drop_duplicates(subset=["customer_id"])

## 9. 卖家表 sellers 单表清洗
sellers = pd.read_csv(f"{path_root}\\olist_sellers_dataset.csv")
sellers = sellers[["seller_id", "seller_city", "seller_state"]].drop_duplicates(subset=["seller_id"])

## 10. 评价表 reviews 单表清洗
reviews = pd.read_csv(f"{path_root}\\olist_order_reviews_dataset.csv")
# 去重：一个订单只保留一条评分
reviews = reviews[["order_id", "review_score"]].drop_duplicates(subset=["order_id"])
# 空评分填充0
reviews["review_score"] = reviews["review_score"].fillna(0)

# ===================== 第二步：分层业务合并（全部单表清洗完成后再关联） =====================
# 步骤1：线索 + 成交 关联
lead_seller = pd.merge(
    left=leads,
    right=deals,
    on="mql_id",
    how="left"
)

# 步骤2：渠道卖家 + 订单商品
lead_order = pd.merge(
    left=lead_seller,
    right=order_items,
    on="seller_id",
    how="left"
)

# 步骤3：商品订单 + 订单主表（客户、时间、支付）
user_channel_order = pd.merge(
    left=lead_order,
    right=orders,
    on="order_id",
    how="left"
)

# 步骤4：拼接客户地域
user_channel_order = pd.merge(
    user_channel_order,
    customers,
    on="customer_id",
    how="left"
)

# 步骤5：商品表关联翻译，再合并进总表
df_product = pd.merge(products, cat_trans, on="product_category_name", how="left")
df_product["product_category_name_english"] = df_product["product_category_name_english"].fillna(df_product["product_category_name"])
user_channel_order = pd.merge(user_channel_order, df_product, on="product_id", how="left")

# 步骤6：拼接卖家地域
user_channel_order = pd.merge(
    user_channel_order,
    sellers,
    on="seller_id",
    how="left"
)

# 步骤7：拼接评价分数
user_channel_order = pd.merge(user_channel_order, reviews, on="order_id", how="left")

# ===================== 第三步：合并后全局二次清洗 & 业务衍生标签 =====================
df_clean = user_channel_order.copy()

# 1. 全局去重：避免多商品导致同一订单多条重复
df_clean = df_clean.drop_duplicates(subset=["mql_id", "order_id"])

# 2. 业务衍生标签（适配7项分析）
# 是否成交订单
df_clean["is_order"] = np.where(df_clean["order_id"].isna(), 0, 1)
# 高客单价标识（中位数划分）
price_median = df_clean["payment_value"].median()
df_clean["high_value_order"] = np.where(df_clean["payment_value"] > price_median, 1, 0)

# ===================== 第四步：数据校验 + 导出两套表 =====================
print("========== 原始合并宽表（含未成交线索，漏斗/CAC专用） ==========")
print(f"行数：{user_channel_order.shape[0]}")
print("渠道分布：\n", user_channel_order["投放渠道"].value_counts(dropna=False))

print("\n========== 全局清洗后宽表（干净无异常，RFM/AB/看板专用） ==========")
print(f"清洗后行数：{df_clean.shape[0]}")
print("清洗后渠道分布：\n", df_clean["投放渠道"].value_counts(dropna=False))

# 1. 导出原始全线索宽表（渠道转化漏斗、CAC归因，保留所有线索）
path_raw = r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全线索原始宽表.csv"
user_channel_order.to_csv(path_raw, index=False, encoding="utf-8-sig")

# 2. 导出深度清洗完成宽表（无异常值、带业务标签，用户分层/可视化）
path_clean = r"D:\LI YUTONG\Documents\My Projects\Data-Analysis\项目0汇总分析\全局清洗标准宽表.csv"
df_clean.to_csv(path_clean, index=False, encoding="utf-8-sig")

print(f"\n导出完成：\n1. 漏斗分析表：{path_raw}\n2. 干净分析宽表：{path_clean}")