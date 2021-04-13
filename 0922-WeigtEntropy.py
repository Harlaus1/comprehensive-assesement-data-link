import pandas as pd
import numpy as np

data = pd.read_excel('0922加入warn数据预处理.xlsx',index_col=0,header=0)
# data_old = data.copy(deep=True)
data_1 = pd.read_excel('0922加入warn数据预处理_max-min归一化.xlsx')


# print('数据:')
# print(data)

# print(data.shape[1])

row_num = data.shape[0]  # 选项的数目
column_num = data.shape[1]  # 指标的数目
zhibiao_name = list(data.columns)  # 指标的名字
k = 1 / np.log(row_num)


print('选项数目', row_num)
print('指标数目', column_num)
print('指标名', zhibiao_name)
print('k的值', k)

grade_sum = list(data.apply(lambda x:x.sum(),axis =0)) # 各个指标的和
print('各个指标的和', grade_sum)


# 构建p矩阵
for i in range(column_num) :
    data[zhibiao_name[i]] = data[zhibiao_name[i]].map(lambda x: x / grade_sum[i])
# print(data)

# 处理p矩阵中的0
for i in range(column_num) :
    data[zhibiao_name[i]] = data[zhibiao_name[i]].map(lambda x: x + 0.000001)

# p矩阵的各个值和其ln值相乘
for i in range(column_num) :
    data[zhibiao_name[i]] = data[zhibiao_name[i]].map(lambda x: x * np.log(x))
# print(data)



# # 构建p矩阵
# for i in range(row_num):
#     for j in range(column_num):
#         data.loc[i, zhibiao_name[j]] = data.loc[i][j] / grade_sum[i]
# # print(data)

# # 矩阵的各个值和其ln值相乘
# for i in range(row_num):
#     for j in range(1, column_num):
#         data.loc[i, zhibiao_name[j]] = (data.loc[i][j]) * (np.log(data.loc[i][j]))
# # print(data)

# 新矩阵每行求和；求Ej和Dj，一步到位
Dj = list(data.apply(lambda x: 1 - k * x.sum(),axis =0)) # 各个指标的和
print('Dj:', Dj)

# 求权重
Wj = []
for i in range(column_num):
    Wj.append(Dj[i] / sum(Dj))
print('权重Wj:', Wj)

for i in range(column_num) :
    data_1[zhibiao_name[i]] = data_1[zhibiao_name[i]].map(lambda x: x * Wj[i])
# print(data_1)
data_1['熵权法得分'] = (1 - (data_1['本地错误率'] +data_1['错误占比']+data_1['警告率'])) * 100
# print(data_1)
data_1 = data_1.drop(columns=['本地错误率','错误占比','警告率'])
data_1.to_excel('0922加入warn得分.xlsx')
