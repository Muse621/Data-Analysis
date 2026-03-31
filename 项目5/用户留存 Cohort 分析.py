import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:ym1478523690@localhost:3306/retail_db?charset=utf8mb4')
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目6数据集\data.csv', encoding='utf-8')
print(f"原始数据：{len(df)} 条")
print(f"缺失 CustomerID：{df['CustomerID'].isna().sum()} 条")

# 清洗
df = df.dropna(subset=['CustomerID'])
df['CustomerID'] = df['CustomerID'].astype(int)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# 去掉退货单（InvoiceNo 以 C 开头的是取消订单）
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

# 去掉数量或单价为负的异常数据
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
print(f"清洗后：{len(df)} 条")
df.to_sql('orders', engine, if_exists='append', index=False, chunksize=5000)
print("导入完成")