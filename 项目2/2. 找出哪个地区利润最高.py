import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目2数据集\Sample - Superstore.csv', encoding='cp1252')
region_profit = df.groupby('Profit')['Region'].sum().sort_values(ascending=False).head(1)#False为正序排列
print(region_profit)