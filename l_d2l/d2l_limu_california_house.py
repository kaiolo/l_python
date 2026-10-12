#%%
%matplotlib inline

import os
import torch
from torch import nn 
import kagglehub
import pandas as pd
import numpy as np
import d2l
from d2l import torch as d2l
# path = kagglehub.competition_download('california-house-prices',output_dir=os.path.join(os.getcwd(),"california_data"))
path="D:\l-python\california_data"
print("Path to competition files:", path)
test_data=pd.read_csv(os.path.join(path,'test.csv'))
train_data=pd.read_csv(os.path.join(path,'train.csv'))
print(test_data.shape,train_data.shape)
"""数据处理"""
clip_train_data=train_data.iloc[:,1:-1]
clip_test_data=test_data.iloc[:,1:]
print(clip_test_data.shape,clip_train_data.shape)

all_features=pd.concat([clip_train_data,clip_test_data],axis=0).reset_index(drop=True)


print(all_features.shape)
listed_on , Last_Sold_On = all_features['Listed On'] ,all_features["Last Sold On"]
loss=nn.MSELoss()

def column_data_process (column_data):
    years,months,days=[],[],[]
    values=column_data.values
    for idx in range(len(values)):
        if pd.isna(values[idx]):
            values[idx]='0-0-0'

    values=list(map(lambda x:x.split("-") ,values))

    years =[x[0] for x in values]
    months=[x[1] for x in values]
    days  =[x[2] for x in values]
    return [years , months , days]


def data_standardlize(column_data):
    values=np.array( [ int(x)  for x in column_data.values if x !='0'])
    value_std_p=iter(list(map(lambda x : (x-values.mean())/values.std(),values)))
    value_std=[]
    for value in column_data.values:
        if value=='0':
            value_std.append(0)
        else : value_std.append(next(value_std_p))
    return value_std

def get_net ():
    net=nn.Sequential(nn.Linear(18869,512),nn.ReLU(),nn.Linear(512,64),nn.ReLU(),nn.Linear(64,1))
    return net

def rmse (net,features,labels):
    clipped_pred=torch.clamp(net(features),1,float('inf'))
    rmse=torch.sqrt(loss(torch.log(clipped_pred),torch.log(labels)))
    return rmse.item()

def train (net,train_features,train_labels,batch_size,lr,num_epochs):
    optimizer=torch.optim.Adam(net.parameters(),lr=lr)
    train_iter=d2l.load_array((train_features,train_labels),batch_size)
    train_ls=[]
    for epoch in range(num_epochs):
        for x, y in train_iter:
            optimizer.zero_grad()
            l = loss(net(x), y)
            l.backward()
            optimizer.step()
        current_rmse = rmse(net, train_features, train_labels)
        train_ls.append(current_rmse)
        if (epoch + 1) % 5 == 0:
            print(f'epoch:{epoch+1}, rmse: {current_rmse:.4f}')
    return train_ls

def train_and_load (train_features, test_features, train_labels, test_data,
                   num_epochs, lr , batch_size):
    net=get_net()
    train_ls=train(net,train_features,train_labels,batch_size,
                     lr,num_epochs)
    d2l.plot(np.arange(1, num_epochs + 1), train_ls, xlabel='epoch',
             ylabel='log rmse', xlim=[1, num_epochs], yscale='log')
    print(f'训练log rmse：{float(train_ls[-1]):f}')
    pred=net(test_features).detach().numpy()
    test_data["Sold Price"]=pd.Series(pred.reshape(1,-1)[0])
    sumbmission=pd.concat([test_data["Id"],test_data["Sold Price"]],axis=1)
    sumbmission.to_csv('submission.csv', index=False)






num_idx=all_features.dtypes[all_features.dtypes!="object"].index

all_features[num_idx]=all_features[num_idx].apply(lambda x : (x-x.mean())/(x.std()))

"""日期处理"""
for x , y in zip(['ls_on_y', 'ls_on_m' , 'ls_on_d'] ,column_data_process(listed_on)):
    all_features[x] = y
    all_features[x] = data_standardlize(all_features[x])
for x ,y in zip (['lt_on_y', 'lt_on_m' , 'lt_on_d'], column_data_process(Last_Sold_On)):
    all_features[x] = y
    all_features[x] = data_standardlize(all_features[x])

# print (all_features['lt_on_y'])
# print(len(all_features['lt_on_y']))
"""日期处理"""

all_features=all_features.fillna(0)

all_features=all_features.drop(columns=["Address","Summary","Listed On","Last Sold On","Parking features","Appliances included","Parking"])

all_features=pd.get_dummies(all_features,dummy_na=True)

all_features=all_features*1.0

print(all_features.shape)
train_features=torch.tensor(all_features[:train_data.shape[0]].values,dtype=torch.float32)
train_labels  =torch.tensor(train_data["Sold Price"].values.reshape(-1,1),dtype=torch.float32)
test_features =torch.tensor(all_features[train_data.shape[0]:].values,dtype=torch.float32)

batch_size , lr ,num_epochs = 256 , 0.3 , 200

train_and_load(train_features ,test_features , train_labels ,test_data, num_epochs, lr ,batch_size )








