import torch 
from torch import nn
from d2l import torch as d2l

def pool2d(X , pool_size , mode ="max") :
    p_h ,p_w = pool_size 
    Y=torch.zeros(X.shape[0]-p_h+1 , X.shape[1]-p_w+1)
    for i in range(Y.shape[0]) :
        for j in range (Y.shape[1]) :
            if mode == "max"  :
                Y[i , j] = torch.max(X[i:i+p_h , j : j+p_w])
            elif mode == "avg" :
                Y[i ,j] = torch.mean(X[i : i+p_h , j : j+p_w])
    return Y



if __name__ == "__main__":
    # X = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    # print(pool2d(X , (2 , 2) , "max"))
    # print(pool2d(X , (2 , 2) , "avg"))

    maxpool2d = nn.MaxPool2d(3 , padding = 1 , stride =2 )
    avgpool2d = nn.AvgPool2d(3 , padding = 1 , stride = 2)

    X = torch.arange(16 , dtype = torch.float32).reshape(1, 1,4,4)
    print(X , "\nMax Pooling:\n", maxpool2d(X))
    print("\nAverage Pooling:\n", avgpool2d(X))
