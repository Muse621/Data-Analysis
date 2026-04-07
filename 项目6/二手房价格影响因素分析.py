import pymysql
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
# 全局配置：解决中文乱码+负号显示异常（Windows/Mac/Linux通用）
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Zen Hei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150  # 统一图片清晰度
engine = create_engine('mysql+pymysql://root:ym1478523690@localhost:3306/house_analysis?charset=utf8mb4')

df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目6数据集\new.csv', encoding='gbk')
print(df.info())
print(f"原始数据：{len(df)}条")
print(f"缺失条数：{df.isnull().sum()}条")
#定义楼层
def prase_floor(s):
    if pd.isnull(s):
        return None,None
    s = str(s)
    if'高' in s :
        floor_type = '高'
    elif '中' in s:
        floor_type = '中'
    elif '低' in s:
        floor_type = '低'
    total = re.findall(r'(\d+)', s)  
    total_floor = int(total[-1]) if total else None
    return floor_type ,total_floor
