import torch 
from   torch import nn
from .d2l_self_animator    import Animator
from .d2l_self_Accumulator import Accumulator
from .d2l_self_Timer       import Timer 
from .d2l_self_evaluate_accuracy import accuracy ,evalulate_accuracy
def train_on_gpu (net , train_iter , test_iter , num_epochs , lr ,device):

    def init_weight(m):
        if type(m)==nn.Linear or type(m)==nn.Conv2d :
            nn.init.xavier_uniform_(m.weight)
    net.apply(init_weight)
    print("train on",device)
    net.to(device)
    optimizer=torch.optim.SGD(net.parameters(),lr)
    loss =nn.CrossEntropyLoss()
    
    animator = Animator(x_label=['epoch'] ,x_lim=[[1,num_epochs]],
                        legend=[['train loss', 'train acc', 'test acc']]) 
    timer = Timer()
    num_batches = len(train_iter)

    for epoch in range(num_epochs) :
        metric = Accumulator(3)
        net.train()
        for i,(x,y) in enumerate(train_iter) :
            timer.start()
            x , y = x.to(device) , y.to(device)
            optimizer.zero_grad()
            y_hat=net(x)
            l=loss(y_hat , y)
            l.backward()
            optimizer.step()
            with torch.no_grad():
                metric.add(l*x.shape[0] , accuracy(y_hat , y) , x.shape[0])
            timer.stop()
            train_l = metric[0]/metric[2]
            train_acc = metric[1]/metric[2]
            if (i+1)%(num_batches//5)==0 or i==num_batches-1 :
                animator.add(epoch+1 , [train_l , train_acc ,None])
        test_acc = evalulate_accuracy(net ,test_iter)
        animator.add(epoch+1 , [None ,None , test_acc])
    print(f'loss {train_l:.3f}, train acc {train_acc:.3f}, '
          f'test acc {test_acc:.3f}')
    print(f'{metric[2] * num_epochs / timer.sum():.1f} examples/sec '
          f'on {str(device)}')    
    return animator




