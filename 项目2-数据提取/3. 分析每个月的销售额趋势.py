import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目2数据集\Sample - Superstore.csv', encoding='cp1252')
df['Order Date'] = pd.to_datetime(df['Order Date']) #日期从字符串转为pandas日期类型(datetime)
df['Month'] = df['Order Date'].dt.to_period('M')  # 提取（dt）月，年'Y'月'M'日'D'季度'Q'
monthly_sales = df.groupby('Month')['Sales'].sum()#按(月)分组，选取[销售额]求和
print(monthly_sales)