#statsmodels库 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 全局配置：解决中文乱码+负号显示异常（Windows/Mac/Linux通用）
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Zen Hei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150  # 统一图片清晰度
from statsmodels.stats.power import NormalIndPower #.stats.power统计检验能力 #NormalIndPower样本量计算工具
from statsmodels.stats.proportion import proportions_ztest #.stats.proportion比例转化率模块 #proportions_ztest检验AB转化率


#调取数据
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目4数据集\ab_data.csv',encoding = 'gbk')
# 看两组各多少人、转化率多少
result = df.groupby('group')['converted'].agg(['count','mean'])#按组查看人数和转化率，由于converted只有01，求均值就是转化率
print("当前数据情况")
print(result)#对照组147202，转化率12.04%   # 实验组147276，转化率11.89%

# ==================================================
# 第一部分：A/B测试【上线前】—— 样本量预估
# 逻辑：只用对照组数据作为「历史基线」，预设提升，计算所需样本
# ==================================================
print("【第一部分：上线前 —— 样本量预估】")

# 1. 提取基线：对照组 = 线上原有版本历史数据
p_baseline = result.loc["control", "mean"]  # 基线转化率

# 2. 手动设置你想要检测的提升
target_lift = 0.02    # 预期相对提升 2%
alpha = 0.05          # 显著性水平
power = 0.8           # 检验效力

# 3. 计算目标转化率 & 效应量
p_treat_target = p_baseline * (1 + target_lift)
effect_size = 2 * (np.arcsin(np.sqrt(p_treat_target)) - np.arcsin(np.sqrt(p_baseline)))

# 4. 计算每组理论最少需要样本量
power_analysis = NormalIndPower()
min_sample = power_analysis.solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    alternative="two-sided"
)

# 输出上线前结果
print(f"基线转化率：{p_baseline:.4%}")
print(f"预设预期提升：{target_lift:.2%}")
print(f"每组理论最少需要样本量：{int(min_sample)} 人")
print("-" * 70)
