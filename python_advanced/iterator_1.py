import time
class Iterable :
    def __init__(self,*arg):
        self.arg=arg
    def __iter__(self):
        return Iterator(self)
    def __len__(self):
        return len(self.arg)

class Iterator :
    def __init__(self , iterable):
        self.idx=0
        self.iter = iterable
    def __iter__(self):
        return self
    def __next__(self):
        if self.idx>= len(self.iter):
            raise StopIteration
        scope=list(self.iter.arg)
        value=scope[self.idx]
        self.idx+=1
        return value
with open ('./python_advanced/what_you_show.txt' , 'r',encoding='utf-8' ) as f :
    literal=f.read()

iter1 = Iterable(*literal)

for item in iter1:
    print(item,end=" ",flush=True) 
    time.sleep(0.5)
        