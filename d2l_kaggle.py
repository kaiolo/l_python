#%%
%matplotlib inline
import os
import hashlib
import tarfile
import zipfile
import requests
DATA_HUB = dict()
DATA_URL = 'http://d2l-data.s3-accelerate.amazonaws.com/'
def download(name,cache_dir=os.path.join("..","data")):
    assert name in DATA_HUB ,f"{name} is not in {DATA_HUB}"
    url,sha1_hash=DATA_HUB[name]
    os.makedirs(cache_dir,exist_ok=True)
    fname=os.path.join(cache_dir,url.split("/")[-1])
    if os.path.exists(fname):
        sha1=hashlib.sha1()
        with open (fname,"rb") as f:
            while data:= f.read(1048576):
                sha1.update(data)
        if sha1.hexdigest()==sha1_hash:
            return fname
    print(f"正在从{url}下载{name}")
    r=requests.get(url,stream=True,verify=True)
    with open(fname,"wb") as f:
        f.write(r.content)
    return fname


def download_extact(name,folder=None):
    fname=download(name)
    dir_name=os.path.dirname(fname)
    data_dir,ext=os.path.splitext(fname)
    if ext==".zip":
        fp=zipfile.ZipFile(fname,"r")
    elif ext in (".tar",".gz"):
        fp=tarfile.open(fname,"r")
    else: assert  False,'格式不对'
    fp.extractall(dir_name)
    return os.path.join(dir_name,folder) if folder else data_dir


def download_all ():
    for name in DATA_HUB:
        download(name)

import numpy as np
import pandas as pd
import torch 
import d2l
from torch import nn
from d2l import torch as d2l

DATA_HUB['kaggle_house_train'] = (  #@save
    DATA_URL + 'kaggle_house_pred_train.csv',
    '585e9cc93e70b39160e7921475f9bcd7d31219ce')

DATA_HUB['kaggle_house_test'] = (  #@save
    DATA_URL + 'kaggle_house_pred_test.csv',
    'fa19780a7b011d9b009e8bff8e99922a8ee2eb90')

train_data=pd.read_csv(download('kaggle_house_train'))
test_data=pd.read_csv(download('kaggle_house_test'))


"""数据预处理"""
all_features=pd.concat((train_data.iloc[:,1:-1],test_data.iloc[:,1:]))
numeric=all_features.dtypes[all_features.dtypes != "object"].index
all_features[numeric]=all_features[numeric].apply(lambda x:(x-x.mean())/(x.std()))
all_features[numeric]=all_features[numeric].fillna(0)
all_features=pd.get_dummies(all_features,dummy_na=True)

n_train=train_data.shape[0]
all_features=all_features*1.0
train_features=torch.tensor(all_features[:n_train].values,dtype=torch.float32)
test_features=torch.tensor(all_features[n_train:].values,dtype=torch.float32)
train_labels=torch.tensor(train_data.SalePrice.values.reshape([-1,1]),dtype=torch.float32)

loss=nn.MSELoss()
num_features=train_features.shape[1]

def get_net():
    net=nn.Sequential(nn.Linear(num_features,256),nn.ReLU(),
                      nn.Linear(256,64),nn.ReLU(),
                      nn.Linear(64,1))
    return net

def rmse (net,features,labels):
    clipped_pred=torch.clamp(net(features),1,float('inf'))
    rmse=torch.sqrt(loss(torch.log(clipped_pred),torch.log(labels)))
    return rmse.item()

def train(net,train_features,train_labels,test_features,test_labels,batch_size,learning_rate,weight_decay,num_epochs):
    train_ls,test_ls=[],[]
    train_iter=d2l.load_array((train_features,train_labels),batch_size)
    optimizer=torch.optim.Adam(net.parameters(),lr=learning_rate,weight_decay=weight_decay)
    for epoch in range(num_epochs):
        for x,y in train_iter :
            optimizer.zero_grad()
            l=loss(net(x),y)
            l.backward()
            optimizer.step()
        train_ls.append(rmse(net,train_features,train_labels))
        if test_labels is not None:
            test_ls.append(rmse(net, test_features, test_labels))
    return train_ls , test_ls

def k_fold_data(k,i,x,y):
    assert k>1
    fold_size=x.shape[0]//k
    x_train,y_train=None,None
    for j in range(k):
        idx=slice(j*fold_size,(j+1)*fold_size)
        x_part=x[idx]
        y_part=y[idx]
        if i==j:
            x_val=x_part
            y_val=y_part
        elif x_train is None:
            x_train=x_part
            y_train=y_part
        else :
            x_train=torch.cat([x_train,x_part],dim=0)
            y_train=torch.cat([y_train,y_part],dim=0)
    return x_train ,y_train,x_val,y_val

def k_fold_train(k,batch_size,learning_rate,weight_decay,num_epochs,train_features,train_labels):
    net=get_net()
    train_ls_sum,test_ls_sum=0,0
    for i in range(k):
        data=k_fold_data(k,i,train_features,train_labels)
        train_ls,test_ls=train(net,*data,batch_size,learning_rate,weight_decay,num_epochs)
        train_ls_sum+=train_ls[-1]
        test_ls_sum+=test_ls[-1]
        if i == 0:
            d2l.plot(list(range(1, num_epochs + 1)), [train_ls,test_ls],
                     xlabel='epoch', ylabel='rmse', xlim=[1, num_epochs],
                     legend=['train', 'valid'], yscale='log')
        print(f'折{i + 1},训练log rmse{float(train_ls[-1]):f}, 'f'验证log rmse{float(test_ls[-1]):f}')
    return train_ls_sum / k, test_ls_sum / k
    

k, num_epochs, lr, weight_decay, batch_size = 20, 200, 0.1, 0, 128
train_l, valid_l = k_fold_train(k,  batch_size,lr,weight_decay,num_epochs, train_features,train_labels, 
                          )
print(f'{k}-折验证: 平均训练log rmse: {float(train_l):f}, '
      f'平均验证log rmse: {float(valid_l):f}')

def train_and_load (train_features, test_features, train_labels, test_data,
                   num_epochs, lr, weight_decay, batch_size):
    net=get_net()
    train_ls,_=train(net,train_features,train_labels,None,None,batch_size,
                     lr,weight_decay,num_epochs)
    d2l.plot(np.arange(1, num_epochs + 1), [train_ls], xlabel='epoch',
             ylabel='log rmse', xlim=[1, num_epochs], yscale='log')
    print(f'训练log rmse：{float(train_ls[-1]):f}')
    pred=net(test_features).detach().numpy()
    test_data["SalePrice"]=pd.Series(pred.reshape(1,-1)[0])
    sumbmission=pd.concat([test_data["Id"],test_data["SalePrice"]],axis=1)
    sumbmission.to_csv('submission.csv', index=False)
train_and_load(train_features, test_features, train_labels, test_data,
                   num_epochs, lr, weight_decay, batch_size)

# %%
