"""weight decay"""
#%%
%matplotlib inline
import d2l
from d2l import torch as d2l
import torch
import linreg

num_input,n_train,n_test,batch_size=200,20,100,5
true_w,true_b=torch.ones([num_input,1])*0.01,0.05
def synthetic(w,b,num_examples):
    X=torch.normal(0,0.01,[num_examples,len(w)],dtype=torch.float32)
    Y=X@w+b
    Y+=torch.normal(0,0.01,Y.shape,dtype=torch.float32)
    return X,Y
def load_arry(data_array,batch_size,is_true=True):
    data=torch.utils.data.TensorDataset(*data_array)
    return torch.utils.data.DataLoader(data,batch_size,shuffle=is_true)
train_data=synthetic(true_w,true_b,n_train)
train_iter=load_arry(train_data,batch_size)
test_data=synthetic(true_w,true_b,n_test)
test_iter=load_arry(test_data,batch_size)
def l2_penalty(w):
    return torch.sum(w.pow(2))/2
def init_para():
    w=torch.normal(0,1,size=(num_input,1),requires_grad=True)
    b=torch.zeros(1,requires_grad=True)
    return [w,b]
def train (lamd):
    w,b=init_para()
    net,loss=lambda X:linreg.linreg(X,w,b),linreg.square_loss
    num_epoch=100
    animator = d2l.Animator(xlabel='epochs', ylabel='loss', yscale='log',
                            xlim=[5, num_epoch], legend=['train', 'test'])
    for epoch in range(num_epoch):
        for x,y in train_iter :
            l=loss(net(x),y)+lamd*l2_penalty(w)
            l.sum().backward()
            linreg.sgd([w,b],0.003,batch_size)
        if (epoch + 1) % 5 == 0:
            animator.add(epoch + 1, (d2l.evaluate_loss(net, train_iter, loss),
            d2l.evaluate_loss(net, test_iter, loss)))
train(3)

