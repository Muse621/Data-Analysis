import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目2数据集\Sample - Superstore.csv', encoding='cp1252')
negative_profit = df.groupby('Sub-Category')['Profit'].sum()
negative_profit_categories = negative_profit [negative_profit < 0]#变量名不能包含空格，可以用_衔接
print(negative_profit_categories)