#用 RFM 模型对用户分层：
#- R（Recency）：最近一次购买距今多少天，越近越好
import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目3数据集\OnlineRetail.csv',encoding ='gbk')
print(df.info())
print(df.isnull().sum())#查看原数据缺失情况
df = df.dropna(subset=['CustomerID'])#去除ID为空的行
df = df[df['UnitPrice']>0]#清洗价格
df = df[df['Quantity']>0]#清洗数量
print(df.info())
print(df.isnull().sum())#查看清洗后的结果
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])#转为pandas可读取的格式日期
now = df['InvoiceDate'].max()+pd.Timedelta(days=1)#消费日期最大值+1 #pd.Timedelta计算两个时间点的间隔或对时间进行加减
R = df.groupby('CustomerID').agg(R=('InvoiceDate', lambda x: (now- x.max()).days))
print(R)
#按CustomerID分组 
#.agg给分组后的数据自定义计算 
#lambda参数1，参数2：表达式 
#x为参数取自'InvoiceDate'
#x.max()该客户最后一次消费日期
#.days时间差转换为天数