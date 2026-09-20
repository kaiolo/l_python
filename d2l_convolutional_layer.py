import torch 
from torch import nn
def corr2d(X,Kernel):
    h,w = Kernel.shape
    Y=torch.zeros([X.shape[0]-h+1,X.shape[1]-w+1])
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i,j] = (X[i:i+h,j:j+w]*Kernel).sum()
    return Y

x=torch.tensor([[1,3,5],[2,4,6]])


class Conv_Layer (nn.Module):
    def __init__(self , kenel_size):
        super().__init__()
        self.weight=nn.Parameter(torch.rand(kenel_size))
        self.bias  =nn.Parameter(torch.zeros(1))
    def forward (self,x) :
        return corr2d(x,self.weight)+self.bias
if __name__ == "__main__" :
    net=Conv_Layer([1,2])
    print(net.weight,'\n',net(x))

    Y=torch.tensor([[ 0.,  1.,  0.,  0.,  0., -1.,  0.],
            [ 0.,  1.,  0.,  0.,  0., -1.,  0.],
            [ 0.,  1.,  0.,  0.,  0., -1.,  0.],
            [ 0.,  1.,  0.,  0.,  0., -1.,  0.],
            [ 0.,  1.,  0.,  0.,  0., -1.,  0.],
            [ 0.,  1.,  0.,  0.,  0., -1.,  0.]])
    X=torch.tensor([[1., 1., 0., 0., 0., 0., 1., 1.],
            [1., 1., 0., 0., 0., 0., 1., 1.],
            [1., 1., 0., 0., 0., 0., 1., 1.],
            [1., 1., 0., 0., 0., 0., 1., 1.],
            [1., 1., 0., 0., 0., 0., 1., 1.],
            [1., 1., 0., 0., 0., 0., 1., 1.]])        

    Y=Y.reshape([1,1,6,7]).cuda(0)
    X=X.reshape([1,1,6,8]).cuda(0)
    net=nn.Conv2d(1,1,kernel_size=(1,2),bias=False)
    net.to(device="cuda")
    lr=3e-2
    for i in range (10):
        Y_hat=net(X)
        net.zero_grad()
        loss=nn.MSELoss()
        l=loss(Y_hat , Y)
        l.sum().backward()
        net.weight.data -= net.weight.grad *lr
        if (i+1)%2 == 0 :
            print(f"batch:{i+1} : loss:{l.sum():.3f}")
    print(net.weight.data)
    
