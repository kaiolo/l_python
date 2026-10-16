import time
class Iterable :
    def __init__(self,*arg):
        self.arg=arg
        self.__idx=0
    def __iter__(self):
        self.__idx=0
        return self
    def __next__(self):
        if self.__idx>=len(self.arg):
            raise StopIteration
        scope=list(self.arg)
        value =scope[self.__idx]
        self.__idx+=1
        return value
    def __len__(self):
        return len(self.arg)

with open ('./python_advanced/what_you_show.txt' , 'r',encoding='utf-8' ) as f :
    literal=f.read()

iter1 = Iterable(*literal)

for item in iter1:
    print(item,end=" ",flush=True) 
    time.sleep(0.5)