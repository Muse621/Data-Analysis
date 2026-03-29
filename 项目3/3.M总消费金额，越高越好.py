#- M（Monetary）：总消费金额，越高越好
import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目3数据集\OnlineRetail.csv',encoding ='gbk')
print(df.info())
print(df.isnull().sum())#查看原数据缺失情况
df = df.dropna(subset=['CustomerID'])#去除ID为空的行
df = df[df['UnitPrice']>0]#清洗价格
df = df[df['Quantity']>0]#清洗数量
df['total_price'] = df['UnitPrice']*df['Quantity']
M = df.groupby('CustomerID')['total_price'].sum()
print(M)