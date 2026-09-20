import torch
import torchvision
from torch.utils import data
from torchvision import transforms
from linreg import sgd as sgd
import matplotlib.pyplot as plt
"""初始数据"""
batch_size=256
num_input,num_output=784,10
W=torch.normal(0,0.01,[num_input,num_output],requires_grad=True)
b=torch.zeros(num_output,requires_grad=True)
lr=0.3
num_epochs = 10

"""数据导入"""
trans=transforms.ToTensor()
minist_train=torchvision.datasets.FashionMNIST(root="../data",train=True,transform=trans,download=True)
minist_test=torchvision.datasets.FashionMNIST(root="../data",train=False,transform=trans,download=True)

train_iter=data.DataLoader(minist_train,batch_size,shuffle=True)
test_iter=data.DataLoader(minist_test,batch_size,shuffle=False)

"""softmax实现"""
def softmax(x):
    x_exp=torch.exp(x)
    partition=x_exp.sum(dim=1,keepdim=True)
    return x_exp/partition
def net(x):
    y_hat=torch.matmul(x.reshape([-1,W.shape[0]]),W)+b
    return softmax(y_hat)
"""损失函数"""
def cross_entropy(y_hat,y):
    loss=-torch.log(y_hat[range(len(y)),y])
    return loss
"""精度"""
def accuracy(y_hat,y):
    if len(y_hat)>1 and y_hat.shape[1]>1:
        y_hat= y_hat.argmax(axis=1)
    cmp=y_hat.type(y.dtype)==y
    return float(sum(cmp.type(y.dtype)))
"""累加器"""
class Accumulator:
    def __init__(self,n):
        self.data=[0.0]*n
    def add(self,*arg):
        self.data= [a+float(b) for a,b in zip(self.data,arg)]
   
    def reload(self):
        self.data=[0.0]*len(self.data)
    def __getitem__(self, idx):
        return self.data[idx]
def evaluate_accuracy(net,data_iter):
    metric=Accumulator(2)
    with torch.no_grad ():
        for x,y in data_iter:
            y_hat=net(x)
            metric.add(accuracy(y_hat,y),len(y))
    return metric[0]/metric[1]
"""训练"""
def train_epoch(net,data_iter,loss,updater):
    if isinstance (net ,torch.nn.Module):
        net.eval()
    metric=Accumulator(3)
    for x,y in data_iter:
        y_hat=net(x)
        l=loss(y_hat,y)
        if isinstance(updater,torch.optim.Optimizer): 
            updater.zero_grad()
            l.mean().backward()
            updater.step()
        else :
            l.sum().backward()
            updater(x.shape[0])
        metric.add(float(l.sum()),accuracy(y_hat,y),len(y))
    return metric[0]/metric[2],metric[1]/metric[2]
train_losses, train_accs, test_accs = [], [], []
def train(num_epoach,net,train_iter,test_iter,loss,updater):
    
    for epoch in range(num_epoach):
        train_loss,train_acc=train_epoch(net,train_iter,loss,updater)
        test_acc=evaluate_accuracy(net,test_iter)
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        test_accs.append(test_acc)
        print(f"epoch{epoch+1},train_loss:{train_loss},test_acc:{train_acc}")

def updater (batch_size):
    return sgd([W,b],lr,batch_size)

        

train(num_epochs,net, train_iter, test_iter, cross_entropy, updater)
epochs = range(1, num_epochs + 1)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.plot(epochs, train_losses, 'b-o', markersize=3)
ax1.set(xlabel='epoch', ylabel='loss', title='train loss')
ax1.grid(True)

ax2.plot(epochs, train_accs, 'b-o', markersize=3, label='train acc')
ax2.plot(epochs, test_accs, 'r-o', markersize=3, label='test acc')
ax2.set(xlabel='epoch', ylabel='accuracy', title='accuracy')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig('train_curve.png', dpi=150)
plt.show()