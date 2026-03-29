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
import re
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:ym1478523690@localhost:3306/job_analysis?charset=utf8mb4')
df = pd.read_csv('D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\postings.csv', encoding='utf-8')