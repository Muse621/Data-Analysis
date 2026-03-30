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
conv_result = df.groupby('group')['converted'].sum()
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


#统计结论部分:实验组转化率为0.118920（11.8920%），对照组转化率为0.120399（12.0399%），二者差异仅为**-0.001479**（-0.1479个百分点），无正向提升；p值 = 0.2161，远大于显著性水平0.05，差异统计不显著。同时，当前每组样本量（147202/147276）远低于所需样本量（755339），样本量严重不足，导致统计效力不足，无法可靠识别真实差异。
#业务建议部分:暂不建议全量上线相关方案，需继续收集实验数据直至达到样本量要求。当前数据未体现实验组与对照组的转化差异，盲目上线无法确认能带来转化提升，反而可能因无效改动影响业务指标。
#注意事项部分
# 1. 本次实验因样本量不足且统计结果不显著，核心结论不可靠：无法证明实验组方案优于对照组，需补足样本量后重新开展A/B测试；
# 2. 若后续补量后仍无显著差异，建议复盘方案设计（如改动幅度、用户感知度、实验周期等），优化方案后再重启测试；
# 3. 需明确：p>0.05不代表“实验组和对照组无差异”，仅代表当前数据无法证明二者有差异；样本量不足会大幅增加“第二类错误”概率，即遗漏真实的差异效果，因此必须补量验证；
# 4. 若补量后仍无正向提升，建议放弃该方案，避免无效改动占用实验流量资源，优先保留原有方案或探索其他优化方向。


    
### 第七步：写业务决策建议（第 6–7 天）
#统计结论部分：实验组转化率为 12.31%，对照组为 10.08%，提升 2.23 个百分点（相对提升 22.1%），z 统计量为 X，p 值为 0.003，小于显著性水平 0.05，差异统计显著。95% 置信区间为 [0.81%, 3.65%]，即使最保守的估计也有 0.81 个百分点的提升。
#业务建议部分：建议全量上线橙色按钮方案。按当前日均流量 10 万 UV 计算，2.23 个百分点的转化提升每日约带来 2230 个增量转化，按客单价 150 元估算，月增 GMV 约 1000 万元。
#注意事项部分：本次实验存在一个需要关注的问题，实验仅运行了 14 天，建议在正式上线后持续监测两周，确认效果稳定后再推全量，避免新奇效应导致的短期虚高。
#另外p<0.05 不是说"95% 概率实验组更好"，置信区间也不是"真实提升有 95% 的概率落在这个范围里"。