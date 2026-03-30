#这个实验改了什么（按钮颜色、文案、页面布局）、对照组和实验组是怎么分的（随机分配还是按地区分）、实验跑了多长时间、转化是怎么定义的（点击、注册还是购买）。

#statsmodels库 
import pandas as pd
import numpy as np
from statsmodels.stats.power import NormalIndPower #.stats.power统计检验能力 #NormalIndPower样本量计算工具
from statsmodels.stats.proportion import proportions_ztest #.stats.proportion比例转化率模块 #proportions_ztest检验AB转化率


#调取数据
df = pd.read_csv(r'D:\LI YUTONG\Documents\python projects\文件夹\数据分析项目\数据集\项目5数据集\ab_data.csv',encoding = 'utf-8')
# 看两组各多少人、转化率多少
result = df.groupby('group')['converted'].agg(['count','mean'])#按组查看人数和转化率，由于converted只有01，求均值就是转化率
print("当前数据情况")
print(result)#对照组147202，转化率12.04%   # 实验组147276，转化率11.89%


n_control = result['count'].iloc[0]  #取对照组人数赋值给n
n_treat = result['count'].iloc[1]  #取实验组人数赋值给m
p_control = result.loc['control', 'mean']   # 取对照组实际转化率赋值给p1
p_treat = result.loc['treatment', 'mean'] # 取实验组实际转化率赋值给p2
# iloc[行号，列号] ,iloc[]取整行  # loc[行名，列名]



# 计算效应量（Cohen's h）
#effect_size量化差异大小  #np.sqrt()平方根  #np.arcsin()反正弦函数
effect_size = 2 * (np.arcsin(np.sqrt(p_treat)) - np.arcsin(np.sqrt(p_control))) #实验组减对照组获得差异大小
analysis = NormalIndPower() #NormalIndPower()算两组比例样本量
required_n = analysis.solve_power(   #.solve_power()需要多少样本量
    effect_size=effect_size,
    alpha=0.05,   # 显著性水平 5%
    power=0.8,    # 检验效力 80%
    alternative='two-sided'  # 双侧检验
) #required_n代表每组至少需要多少样本量实验才有效，结论才可信
# 假设：基线转化率 10%，希望能检测到2%的提升，显著性 5%，检验效力 80%


#输出结果判断
print("\n=== 样本量校验结果 ===") #\n代表换行符，与上一段结果空一行
print(f"每组至少需要样本量：{int(required_n) + 1} 人") #f"..."把变量值嵌入之前的字符串 #int(required_n) + 1计算出的最小样本量向上取整，int()取整
print(f"对照组: {n_control:.0f}") #.0f显示为整数
print(f"实验组: {n_treat:.0f}")
if n_control >= required_n and n_treat >= required_n: #required_n代表每组至少需要多少样本量
    print("✅ 样本量充足，可以放心进行 A/B 检验，结论可信")
else:
    print("⚠️  警告：样本量不足，当前差异可能测不出来，建议继续收集数据")


# 5. A/B 检验（分别传入两组人数！）
conv_result = df.groupby('group')['concertde'].sum()
conv_control = conv_result['control']
conv_treat   = conv_result['treatment']

z_stat, p_value = proportions_ztest(
    [conv_control, conv_treat], # [conv_control, conv_treat]转换成功的人数
    [n_control,   n_treat]
) # p_value为核心结果


#输出检验结果
print("\n=== A/B 检验结果 ===")
print(f"p值 = {p_value:.4f}") #.4f 保留4位小数 #.2f 保留2位小数 #.of 输出为整数
if p_value < 0.05:
    print("✅ 显著！新版本更好")
else:
    print("⚠️ 不显著，不能下结论")