import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目2数据集\Sample - Superstore.csv', encoding='cp1252')
print(df.info()) # 数据信息
top5 = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(5)
print(top5)#groupby按照(子类别)分组，sales选取销售额，sum求销售额和，sort_values9()按照要求排序，ascending=False降序排列，head选取前5