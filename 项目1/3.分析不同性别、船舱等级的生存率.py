import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目1数据集\train.csv')
print(df.groupby('Sex')['Survived'].mean())        # 按性别分析
print(df.groupby('Pclass')['Survived'].mean())     # 按船舱等级分析
print(df.groupby(['Sex','Pclass'])['Survived'].mean())  # 交叉分析,mean平均值，(给函数用),[取数据，取列，取行用]
#女性生存率0.74，男性0.18，头等舱生存率0.62，二等舱0.47，三等舱0.24