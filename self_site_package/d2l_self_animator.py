import matplotlib.pyplot as plt
import numpy as np

def set_axes (axes:plt.Axes ,x_label , y_label ,x_lim , y_lim , x_scale , y_scale , legend):
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)
    axes.set_xscale(x_scale)
    axes.set_yscale(y_scale)
    axes.set_xlim  (x_lim)
    axes.set_ylim  (y_lim)
    if legend :
        axes.legend(legend)
    axes.grid()

class Animator () :
    def __init__(self, x_label=None, y_label=None, x_lim=None, y_lim=None,
                 x_scale=None,y_scale=None,legend=None,
                 fmts=('-', 'm--', 'g-.', 'r:'), nrows=1, ncols=1,figsize=(10.5, 8.5)):
        plt.ion()#进入交互模式 interactive on
        self.fig , self.axes = plt.subplots(nrows , ncols ,figsize=figsize)

        #判断是否是多个子图
        if isinstance (self.axes , np.ndarray):
            self.axes = self.axes.flatten()
        else:self.axes = [self.axes]

        self.n_subplots = nrows*ncols
        self.xlabels = x_label if x_label is not None else [None]*self.n_subplots
        self.ylabels = y_label if y_label is not None else [None]*self.n_subplots
        self.legends = legend  if legend  is not None else [[]]*self.n_subplots
        self.xlims   = x_lim   if x_lim   is not None else [None]*self.n_subplots
        self.ylims   = y_lim   if y_lim   is not None else [None]*self.n_subplots
        self.xscales = x_scale if x_scale is not None else ['linear']*self.n_subplots
        self.yscales = y_scale if y_scale is not None else ['linear']*self.n_subplots
        self.X =[[] for _ in range (self.n_subplots)] 
        self.Y =[[] for _ in range (self.n_subplots)] 
        self.fmts = fmts

    def add (self , x , y ,subplot_idx=0) :

        # 判断绘制几条曲线
        if not hasattr(y , '__len__') :
            y=[y]
        n=len(y)

        # 匹配x和y的长度
        if not hasattr(x , '__len__'):
            x=[x]*n

        if not self.X[subplot_idx] :
            self.X[subplot_idx] = [[] for _ in range(n)] 
        if not self.Y[subplot_idx] :
            self.Y[subplot_idx] = [[] for _ in range(n)]

        for i , (a,b) in enumerate(zip(x,y)):
            if a is not None and b is not None :
                self.X[subplot_idx][i].append(a)
                self.Y[subplot_idx][i].append(b)
        # 清除画布
        self.axes[subplot_idx].cla()

        for x_data , y_data , fmt in zip (self.X[subplot_idx] , self.Y[subplot_idx] , self.fmts):
            self.axes[subplot_idx].plot(x_data,y_data,fmt)

        set_axes(self.axes[subplot_idx],
                 self.xlabels[subplot_idx],
                 self.ylabels[subplot_idx],
                 self.xlims[subplot_idx],
                 self.ylims[subplot_idx],
                 self.xscales[subplot_idx],
                 self.yscales[subplot_idx],
                 self.legends[subplot_idx])
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)

    def show(self):
        plt.ioff()  # 关闭交互模式
        plt.show()  # 保持窗口，等待手动关闭，阻止程序跑完直接一闪消失
    
            










