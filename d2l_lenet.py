import torch
from torch import nn
from d2l import torch as d2l
from self_site_package import train_on_gpu

net = nn.Sequential(
        nn.Conv2d(1, 6, kernel_size= 5, stride = 1 , padding = 2 ) , 
        nn.ReLU() ,
        nn.AvgPool2d (kernel_size = 2, stride = 2) , 
        nn.Conv2d(6, 16 , kernel_size = 5 , stride = 1 , padding = 0),
        nn.ReLU(),
        nn.AvgPool2d(kernel_size = 2 , stride = 2 ),
        nn.Flatten() ,
        nn.Linear(16*5*5 , 120) ,
        nn.ReLU(), 
        nn.Linear(120 , 84),
        nn.ReLU(),
        nn.Linear(84 , 10))


batch_size =256
train_iter , test_iter = d2l.load_data_fashion_mnist(batch_size=batch_size)


if __name__ == '__main__' :
    lr, num_epochs = 0.1, 10
    animator=train_on_gpu(net, train_iter, test_iter, num_epochs, lr, d2l.try_gpu())
    animator.show()
