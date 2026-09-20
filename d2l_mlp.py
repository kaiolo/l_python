import torch
from torch import nn
from d2l import torch as d2l
batch_size=256
train_iter,test_iter=d2l.load_data_fashion_mnist(batch_size)
num_in,num_out,num_h=784,10,256
num_epochs=10
lr=0.3
w1=nn.Parameter(torch.rand(num_in,num_h,requires_grad=True)*0.01)
b1=nn.Parameter(torch.zeros(num_h,requires_grad=True))
w2=nn.Parameter(torch.rand(num_h,num_out,requires_grad=True)*0.01)
b2=nn.Parameter(torch.zeros(num_out,requires_grad=True))
params=[w1,b1,w2,b2]
def relu(x):
    a=torch.zeros_like(x)
    return torch.max(a,x)
def net(x):
    h=relu(x.reshape(-1,num_in)@w1+b1)
    return (h@w2+b2)
loss=nn.CrossEntropyLoss(reduction="none")
updater = torch.optim.SGD(params, lr=lr)
d2l.train_ch3(net, train_iter, test_iter, loss, num_epochs, updater)
