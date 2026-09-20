import torch
import random
"y=Xw+b+xi"
def sythetenic_data(num_examples,w,b):
    X=torch.normal(0,0.1,(num_examples,len(w)))
    y=torch.matmul(X,w)+b
    y+=torch.normal(0,0.001,(y.shape))
    return X,y
def data_iter(batch_size,features,labels):
    num_examples=len(features)
    indices=list(range(num_examples))
    random.shuffle(indices)
    for i in range(0,num_examples,batch_size):
        batch_indices=torch.tensor(indices[i:min(i+batch_size,num_examples)])
        yield features[batch_indices],labels[batch_indices]
def linreg(X,w,b):
    y=torch.matmul(X,w)+b
    return y
def square_loss(y_hat,y):
    loss=(y-y_hat)**2/2
    return loss
def sgd (params,lr,batch_size):
    with torch.no_grad():
        for param in params:
            param-=lr*param.grad/batch_size
            param.grad.zero_()

true_w=torch.tensor([2,-3.4])
true_b=4.2
w=torch.normal(0,0.1,(2,1),requires_grad=True)
b=torch.zeros(1,requires_grad=True)
features,labels=sythetenic_data(1000,true_w,true_b)
num_epoches=3
net=linreg
loss=square_loss
lr=0.03
batch_size=10
for epoch in range(num_epoches):
    for X,y in data_iter(batch_size,features,labels):
        l=loss(net(X,w,b),y,)
        l.sum().backward()
        sgd([w,b],lr,batch_size)
    with torch.no_grad():
        train_l=loss(net(features,w,b),labels)
        print(f"hahaepoch{epoch+1},loss {float(train_l.mean()):f}")
