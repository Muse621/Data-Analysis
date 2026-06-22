import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目1数据集\train.csv')
print(df.isnull().sum()) # 数值
print((df.isnull().sum() / len(df) * 100).round(2).astype(str) + '%') # 比例