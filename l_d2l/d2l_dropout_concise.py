#%%
%matplotlib inline
import torch
from torch import nn
import d2l
from d2l import torch as d2l
net = nn.Sequential(nn.Flatten(),
                    nn.Linear(784,256),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(256,256),
                    nn.ReLU(),
                    nn.Dropout(0.5),
                    nn.Linear(256,10))
def init_weights(m):
    if type(m) == nn.Linear:
        nn.init.normal_(m.weight, std=0.01)

net.apply(init_weights);
num_epochs, lr, batch_size = 10, 0.5, 256
loss = nn.CrossEntropyLoss(reduction='none')


from torch.utils.data import DataLoader
import torchvision
from torchvision import transforms

transform = transforms.ToTensor()
train_data = torchvision.datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)
test_data = torchvision.datasets.FashionMNIST(root='./data', train=False, download=True, transform=transform)

train_iter = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=0)
test_iter = DataLoader(test_data, batch_size=batch_size, shuffle=False, num_workers=0)


trainer = torch.optim.SGD(net.parameters(), lr=lr)
d2l.train_ch3(net, train_iter, test_iter, loss, num_epochs, trainer)
