import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目2数据集\Sample - Superstore.csv', encoding='cp1252')
CPF= df.groupby('Sub-Category')[['Profit', 'Sales']].sum()
CPF= CPF[CPF ['Sales'] > 0]#确保除数不为 0
PR = CPF['Profit'] / CPF['Sales']
LPR =PR.sort_values(ascending=True).head(10)#True为倒序排列
print(LPR)