#这是一个跨国数据集，包含了2010年12月1日至2011年12月9日期间发生的所有交易，涉及一家英国注册的非实体在线零售商。
# 该公司主要销售独特的日常礼品。该公司的许多客户是批发商。
#Cohort分析是把用户按首次购买时间分组，追踪同一批用户在后续每个周期的活跃购买情况，用来衡量用户留存、复购和生命周期价值。
#导入系统
import pandas as pd
import numpy as np
from sqlalchemy import create_engine #连接sql数据库引擎
engine = create_engine('mysql+pymysql://root:ym1478523690@localhost:3306/retail_db?charset=utf8mb4')

#查看数据
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目5数据集\data.csv', encoding='gbk')
print(df.info())
print(f"退货订单: {df['InvoiceNo'].astype(str).str.startswith('C').sum()} 条")
print(f"原始数据：{len(df)} 条") #len统计总条数
print(f"缺失 CustomerID：{df['CustomerID'].isnull().sum()} 条")
print(f"缺失 Description：{df['Description'].isnull().sum()} 条")

#清洗数据
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df = df.dropna(subset = ['CustomerID']) #指定CustomerID列删除空白行
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)] #数量价格>0
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')] # ~ 代表取反 # 转为字符串，判断这一串文字，是否以某个字母 / 某段话开头
print(f"清洗后：{len(df)} 条") 

#导入SQL
df.to_sql('orders', engine, if_exists='replace', index=False, chunksize=5000, method = 'multi') 
#if_exists='append'如果表里已经有数据了，就在后面接着加，不删掉原来的
#index=False不要把 pandas 自动生成的行号存进去，让数据库表干净一点
#chunksize=5000一次存 5000 行，分批存，防止一次性存太多卡住
print("导入完成")

#SQL 计算留存率
#  """。。。""" 用于写多行的sql代码   #COUNT计数  #DISTINCT去重  #join将表拼接在一起   #on拼接条件   #ORDER BY排序
#CohortMonth：用户第一次来的月份  #InvoiceMonth：用户这次消费的月份 #MonthIndex：距离第一次来过了几个月
#从user_cohort表，按照CohortMonth和MonthIndex分组查看用户人数生成为 a.active_users
#join将a和b两个表拼接在一起 
#从user_cohort表，只要在第一次消费后本月再消费的用户，按照用户第一次来的月份分组查看用户人数，生成为 b.cohort_size
#按照a.CohortMonth = b.CohortMonth的拼接条件拼接
#ROUND(a.active_users / b.cohort_size * 100, 1) AS retention_pct 留存率公式
#按照a.CohortMonth排, 再按照a.MonthIndex排序,生成a.CohortMonth,a.MonthIndex,a.active_users,b.cohort_size,retention_pct
cohort_data = pd.read_sql("""   
    SELECT 
        a.CohortMonth,
        a.MonthIndex,
        a.active_users,
        b.cohort_size,
        ROUND(a.active_users / b.cohort_size * 100, 1) AS retention_pct
    FROM (
        SELECT CohortMonth, MonthIndex, COUNT(DISTINCT CustomerID) AS active_users
        FROM user_cohort
        GROUP BY CohortMonth, MonthIndex 
    ) a
    JOIN (
        SELECT CohortMonth, COUNT(DISTINCT CustomerID) AS cohort_size
        FROM user_cohort
        WHERE MonthIndex = 0
        GROUP BY CohortMonth
    ) b ON a.CohortMonth = b.CohortMonth
    ORDER BY a.CohortMonth, a.MonthIndex
""", engine)
print(cohort_data.head(20))

#把 cohort_data 写入 SQL，生成新表 cohort_result
cohort_data.to_sql(
    name='cohort_result',  # 新表的名字，你可以自己改
    con=engine,            # 复用你已经创建好的数据库连接
    if_exists='replace',   # 如果表已经存在，就覆盖；也可以用 'append' 追加
    index=False            # 不把 pandas 的行号存进数据库，保持表干净
)
print("导入成功")


### 第六步：Python 画热力图

import matplotlib.pyplot as plt
import seaborn as sns
# 全局配置：解决中文乱码+负号显示异常（Windows/Mac/Linux通用）
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Zen Hei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150  # 统一图片清晰度

pivot = cohort_data.pivot_table(
    index='CohortMonth',
    columns='MonthIndex',
    values='retention_pct'
)

# 确认第 0 列全是 100%（首月留存率定义上是 100%）
print("MonthIndex=0 的留存率：")
print(pivot[0])

fig, ax = plt.subplots(figsize=(16,10))
sns.heatmap(
    pivot,
    annot=True,
    fmt='.1f',
    cmap='Blues',
    vmin=0, vmax=50,
    ax=ax,
    annot_kws={'size': 9},
    linewidths=0.5
)
ax.set_title('用户月度留存率热力图（%）', fontsize=14, pad=12)
ax.set_xlabel('距首次购买月数（月）')
ax.set_ylabel('用户注册月份（Cohort）')
plt.tight_layout()
plt.savefig('cohort_heatmap.png', dpi=150)
plt.show()
cohort_data.to_csv('cohort_result.csv', index=False, encoding='utf-8-sig')