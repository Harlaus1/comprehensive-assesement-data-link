import pandas as pd
import numpy as np

data = pd.read_excel('0922加入warn得分.xlsx', index_col=0)
data_1 = pd.read_excel('0922加入warn数据预处理_max-min归一化.xlsx', index=False)
data_2 = pd.read_excel('加入warn本地错误率.xlsx')

list_zhibiao = ['本地错误率', '错误占比', '告警率']
list_xuguanxi = [1.0, 1.2, 1.2]

list_quanzhong = []
last = 1/(1+1.2+1.2*1.2)
for i in range(len(list_xuguanxi)) :
    list_quanzhong.insert(0, last)
    last = last*list_xuguanxi[len(list_xuguanxi)-1-i]
# print(sum(list_quanzhong))
data['序关系法得分'] = (1 - (data_1['本地错误率']*list_quanzhong[0]
                       +data_1['错误占比']*list_quanzhong[1]
                       +data_1['警告率']*list_quanzhong[2])) * 100
data['综合得分'] = data['熵权法得分']*0.6 + data['序关系法得分']*0.4

data['本地错误率'] = data_2['本地错误率']
data['错误占比'] = data_2['错误占比']
data['警告率'] = data_2['警告率']

order = ['MAJORID', '本地错误率', '错误占比', '警告率', '熵权法得分', '序关系法得分', '综合得分']
data = data[order]


data.to_excel('主客观得分.xlsx',index=False)
