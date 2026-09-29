import torch
from torch import nn
from self_site_package import Accumulator


def argmax (x , axis):
    """
    返回张量指定维度的最大值对应的索引
    example : 
    第 1 行[0.1,0.7 ,0.2 ]最大值在索引 1
    第 2 行[0.9,0.05,0.05]最大值在索引 0
    返回 [1 ,0]
    """
    return x.argmax(dim=axis)

def accuracy(y_hat , y) :
    """
    返回预测值正确的个数
    """
    if len(y_hat.shape)>1 and y_hat.shape[1]>1 :#判断是否是多维输入
        y_hat = argmax(y_hat , axis=1)
    cmp = y_hat.to(y.dtype) == y
    return float(sum(cmp.to(y.dtype)))


def evalulate_accuracy(net , data_iter ,device=None):

    if isinstance (net , nn.Module) :
        net.eval()
        if not device :
            device = next(iter(net.parameters())).device
    meric=Accumulator(2)
    with torch.no_grad() :
        for X , y in data_iter:
            if isinstance(X , list):
                X = [x.to(device) for x in X]
            else : X = X.to(device)
            y=y.to(device)
            meric.add(accuracy(net(X),y) , y.numel())
    return meric[0]/meric[1]


