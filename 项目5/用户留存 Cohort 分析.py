#这是一个跨国数据集，包含了2010年12月1日至2011年12月9日期间发生的所有交易，涉及一家英国注册的非实体在线零售商。
# 该公司主要销售独特的日常礼品。该公司的许多客户是批发商。
#Cohort分析是把用户按首次购买时间分组，追踪同一批用户在后续每个周期的活跃购买情况，用来衡量用户留存、复购和生命周期价值。
#导入系统
import pandas as pd
import numpy as np
from sqlalchemy import create_engine #连接sql数据库引擎
engine = create_engine('mysql+pymysql://root:ym1478523690@localhost:3306/retail_db?charset=utf8mb4')

#查看数据
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目5数据集\data.csv', encoding='gbk')
print(df.info())
print(f"退货订单: {df['InvoiceNo'].astype(str).str.startswith('C').sum()} 条")
print(f"原始数据：{len(df)} 条") #len统计总条数
print(f"缺失 CustomerID：{df['CustomerID'].isnull().sum()} 条")
print(f"缺失 Description：{df['Description'].isnull().sum()} 条")

#清洗数据
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df = df.dropna(subset = ['CustomerID']) #指定CustomerID列删除空白行
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)] #数量价格>0
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')] # ~ 代表取反 # 转为字符串，判断这一串文字，是否以某个字母 / 某段话开头
print(f"清洗后：{len(df)} 条") 

#导入SQL
df.to_sql('orders', engine, if_exists='append', index=False, chunksize=5000)
#if_exists='append'如果表里已经有数据了，就在后面接着加，不删掉原来的
#index=False不要把 pandas 自动生成的行号存进去，让数据库表干净一点
#chunksize=5000一次存 5000 行，分批存，防止一次性存太多卡住
print("导入完成")