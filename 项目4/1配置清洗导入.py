import pymysql
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# 替换成你自己的 MySQL 配置
engine = create_engine('mysql+pymysql://root:ym1478523690@localhost:3306/?charset=utf8mb4')

# 测试连接
df = pd.read_sql("SELECT 1 AS test", engine)
print("MySQL 连接成功")

# 解决中文和负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows 用 SimHei
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题


#清洗数据
import pandas as pd
import re #re正则表达从字符串里提取数字
from sqlalchemy import create_engine #
engine = create_engine('mysql+pymysql://root:ym1478523690@localhost:3306/job_analysis?charset=utf8mb4')
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目4数据集\postings.csv', encoding = 'utf-8')

# 提取薪资数字（单位统一为千元/月）
def parse_salary(s):
    if pd.isna(s) or '面议' in str(s):
        return None, None
    nums = re.findall(r'\d+\.?\d*', str(s))
    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    return None, None

df[['salary_min', 'salary_max']] = df['salary'].apply(
    lambda x: pd.Series(parse_salary(x))
)
df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2
df['salary_raw'] = df['salary']

# 删掉薪资为空的行
df_clean = df.dropna(subset=['salary_avg']).copy()

print(f"清洗前：{len(df)} 条，清洗后：{len(df_clean)} 条")
print(df_clean['salary_avg'].describe())

# 导入 MySQL
df_clean[['job_title','city','company','salary_raw','salary_min','salary_max','salary_avg','education','experience']].to_sql(
    'jobs', engine, if_exists='append', index=False
)
print("数据导入完成")