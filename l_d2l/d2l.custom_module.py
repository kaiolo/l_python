import torch 
from torch import nn 
from torch.nn import functional as F

class MLP(nn.Module) :
    def __init__(self):
        super().__init__()
        self.hidden=nn.Linear(20,256)
        self.out=nn.Linear(256,10)
    def forward (self , X):
        return self.out(F.relu(self.hidden(X)))



class MySequential (nn.Module):
    def __init__(self, *args, ):
        super().__init__()
        for idx , module in enumerate(args):
            self._modules[str(idx)]=module
    def forward (self,x):
        for block in self._modules.values():
            x=block(x)
        return x
class Fixed_Hidden_Layer(nn.Module):
    def __init__(self):
        super().__init__()
        self.rand_weight=torch.tensor([[1,2],[2,1]],requires_grad=False)
        self.linear=nn.Linear(2,2)
    def forward (self ,x ):
        x=F.relu(torch.mm(x,self.rand_weight)+1)
        x=self.linear(x)
        while x.abs().sum()>1:
            x/=2
        return x.sum()
net=Fixed_Hidden_Layer()     
# print(list(net.named_parameters()))

# def init(m):
#     if type(m) ==nn.Linear:
#         nn.init.uniform_(m.weight , -10 , 10)
#         m.weight.data*=m.weight.data.abs() > 5
# net[0].apply(init)
# print(net[0].weight.data)
class custom_linear (nn.Module) :
    def __init__(self,in_unit,unit):
        super().__init__()
        self.weight=nn.Parameter(torch.rand(in_unit,unit))
        self.bias  =nn.Parameter(torch.randn([unit,]))
    def forward (self ,x):
        x=torch.matmul(x,self.weight.data)+self.bias.data
        return F.relu(x)


x=torch.tensor([[1,2]],dtype=torch.float32,device="cuda")
# print(x.device)
net=nn.Sequential(nn.Linear(2,1))
net=net.to(device='cuda')
print(net(x))
print(net[0].weight.data.grad)






        
   





