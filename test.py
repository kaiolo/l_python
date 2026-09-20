import os
import torch
from torch import nn 
import kagglehub
import pandas as pd
import numpy as np
import numpy as np
def data_standardlize(column_data):
    values=np.array( [ int(x)  for x in column_data.values if x !='0'])
    value_std_p=iter(list(map(lambda x : (x-values.mean())/values.std(),values)))
    value_std=[]
    for value in column_data.values:
        if value=='0':
            value_std.append(0)
        else : value_std.append(next(value_std_p))
    return value_std
# path = kagglehub.competition_download('california-house-prices',output_dir=os.path.join(os.getcwd(),"california_data"))
path="D:\l-python\california_data"
print("Path to competition files:", path)
test_data=pd.read_csv(os.path.join(path,'test.csv'))
train_data=pd.read_csv(os.path.join(path,'train.csv'))

part_data=pd.read_csv(os.path.join(path,'part_test.csv'))


"""数据处理"""
clip_train_data=train_data.iloc[:,1:-1]
clip_test_data=test_data.iloc[:,1:]

""""测试"""


part_data=part_data.drop(columns=["Address","Summary"])

listed_on , Last_Sold_On = part_data['Listed On'] ,part_data["Last Sold On"]

print(listed_on.values,Last_Sold_On.values)
def column_data_process (column_data):
    years,months,days=[],[],[]
    values=column_data.values
    for idx in range(len(values)):
        if pd.isna(values[idx]):
            values[idx]='0/0/0'

    values=list(map(lambda x:x.split("/") ,values))

    years =[x[0] for x in values]
    months=[x[1] for x in values]
    days  =[x[2] for x in values]
    return [years , months , days]

for x , y in zip(['ls_on_y', 'ls_on_m' , 'ls_on_d'] ,column_data_process(listed_on)):
    part_data[x] = y
for x ,y in zip (['lt_on_y', 'lt_on_m' , 'lt_on_d'], column_data_process(Last_Sold_On)):
    part_data[x] = y
print (part_data['lt_on_y'])   
data_standardlize(part_data['lt_on_y'])
print (data_standardlize(part_data['lt_on_y']))
num_idx=part_data.dtypes[part_data.dtypes!="object"].index

part_data[num_idx]=part_data[num_idx].apply(lambda x : (x-x.mean())/(x.std()))

part_data=part_data.fillna(0)



""""测试"""




# all_features=pd.concat([clip_train_data,clip_test_data],axis=0)
# all_features=all_features.drop(columns=["Address","Summary"])
# num_idx=all_features.dtypes[all_features.dtypes!="objects"].index

# all_features=all_features[num_idx].apply(lambda x : (x-x.mean())/(x.std()))

# all_features=all_features.fillna(0)

# listed_on , Last_Sold_On = all_features['Listed On'] , all_features["Last Sold On"]
# def column_data_process (column_data):
#     years,months,days=[],[],[]
#     values=column_data.values
#     for idx in range(len(values)):
#         if pd.isna(values[idx]):
#             values[idx]='--'

#     values=list(map(lambda x:x.split("-") ,values))

#     years =[x[0] for x in values]
#     months=[x[1] for x in values]
#     days  =[x[2] for x in values]
#     return [years , months , days]

# for x , y in zip(['ls_on_y', 'ls_on_m' , 'ls_on_d'] ,column_data_process(listed_on)):
#     all_features[x] = y
# for x ,y in zip (['lt_on_y', 'lt_on_m' , 'lt_on_d'], column_data_process(Last_Sold_On)):
#     all_features[x] = y

# print (all_features['lt_on_y'])
# all_features=all_features*1.0
# all_features=pd.get_dummies(all_features,dummy_na=True)




# def column_data_process (column_data):
#     years,months,days=[],[],[]
#     values=column_data
#     for idx in range(len(values)):
#         if pd.isna(values[idx]):
#             values[idx]='--'

#     values=list(map(lambda x:x.split("-") ,values))

#     years =[x[0] for x in values]
#     months=[x[1] for x in values]
#     days  =[x[2] for x in values]
#     return [years , months , days]

# for x , y in zip(['ls_on_y', 'ls_on_m' , 'ls_on_d'] ,column_data_process(a)):
#     d[x] = y
# for x ,y in zip (['lt_on_y', 'lt_on_m' , 'lt_on_d'], column_data_process(b)):
#     d[x] = y

# print (d['lt_on_y'],d['lt_on_m'],d['lt_on_d'])
