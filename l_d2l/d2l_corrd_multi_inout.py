import torch
from d2l_convolutional_layer import corr2d




def corrd_multi_in (X , kernel_3d) :
    """
    X:代表多通道输入
    k:多维(4d)卷积核的后三维
    """
    y_single_channel=sum(corr2d(x,k) for x, k in zip(X , kernel_3d))
    return y_single_channel

def corr_multi_in_out (X , Kernel_4d) :
    Y_multi_out=torch.stack([corrd_multi_in(X , k) for k in Kernel_4d] , dim=0)
    return Y_multi_out


X = torch.tensor([[[0.0, 1.0, 2.0], [3.0, 4.0, 5.0], [6.0, 7.0, 8.0]],
               [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]])

# K = torch.tensor([[[0.0, 1.0], [2.0, 3.0]], [[1.0, 2.0], [3.0, 4.0]]])

# K = torch.stack ( (K , K+1 , K+2 ),dim=0)

# print(corr_multi_in_out(X , K))


def corr_multi_in_1x1 (X , K):
    C_i , n_h ,n_w= X.shape
    X= X.reshape(C_i , n_h*n_w)
    C_o = K.shape[0]
    K = K.reshape(C_o , C_i)
    Y = torch.matmul(K , X)
    return Y.reshape(C_o , n_h , n_w)

K = torch.arange(6).reshape(3 , 2 , 1 , 1).to(dtype=torch.float32)
print (corr_multi_in_out(X,K)==corr_multi_in_1x1(X,K))
