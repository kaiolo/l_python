import time
import numpy as np
class Timer :
    def __init__(self):
        self.time=[]
        self.start()

    def start(self):
        self.tik=time.time()

    def stop(self):
        self.time.append(time.time()-self.tik)
        return self.time[-1]
    
    def avg (self):
        return sum(self.time)/len(self.time)
    
    def sum (self):
        return sum(self.time)
    
    def cumsum (self):
        return np.array(self.time).cumsum().tolist()
if __name__ == "__main__":
    time1 = Timer()
    time.sleep(0.2)
    print("第1次耗时：", time1.stop())
    
    time1.start()
    time.sleep(0.1)
    print("第2次耗时：", time1.stop())

    print("平均耗时：", time1.avg())
    print("总耗时：", time1.sum())
    print("累计时间序列：", time1.cumsum())
