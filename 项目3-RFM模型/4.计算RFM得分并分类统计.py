#输出每个用户的 RFM 得分，将用户分为"高价值""流失风险""新客户"等类别
import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目3数据集\OnlineRetail.csv',encoding ='gbk')
print(df.info())
print(df.isnull().sum())
df = df.dropna(subset=['CustomerID'])
df = df[df['UnitPrice']>0]
df = df[df['Quantity']>0]
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
now = df['InvoiceDate'].max()+pd.Timedelta(days=1)
df['total_money'] = df['UnitPrice']*df['Quantity']
rfm = df.groupby('CustomerID').agg(
       r = ('InvoiceDate',lambda x: (now - x.max()).days),
       f = ('InvoiceNo','nunique'),
       m = ('total_money','sum')
).reset_index()#把CustomerID从索引转成列

print(rfm.head())
print(rfm.describe())#.describe()数据情况
# 第四步：打分（1-5分，用四分位数分段）
rfm['R_Score'] = pd.qcut(rfm['r'], q=5, labels=[5,4,3,2,1])   # R最近一次购买距今多少天，越近越好越小越好 #.quct()按q=多少来分组分人 #labels分标签
rfm['F_Score'] = pd.qcut(rfm['f'].rank(method='first'), q=5, labels=[1,2,3,4,5])#.rank(method='first')给F重复的购买频次排先后顺序让qcut顺利分组打分
rfm['M_Score'] = pd.qcut(rfm['m'], q=5, labels=[1,2,3,4,5])
# 第五步：用户分层#555高分用户 #111流失用户 #544普通用户
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str) #.astype()将分数转字符串float小数int整数
count = rfm['RFM_Score'].value_counts()#.value_counts()统计每一种值出现的次数
ratio = rfm['RFM_Score'].value_counts(normalize=True)*100 #value_counts(normalize=True)计算次数比例
result = pd.DataFrame({'人数':count,
                '占比':ratio.round(2).astype(str) + '%'})
print(result)