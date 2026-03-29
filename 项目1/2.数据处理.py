import pandas as pd
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目1数据集\train.csv')
print(df.info())
df.drop(columns=['Cabin'], inplace=True)  # Cabin缺失太多，直接删除
x = df["Age"].median() # 年龄用中位数填充
df.fillna({"Age": x}, inplace=True)
y = df["Embarked"].mode() # 登船港口用众数填充
df.fillna({"Embarked": y}, inplace=True)
print(df.to_string())