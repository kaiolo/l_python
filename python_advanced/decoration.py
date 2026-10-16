#region
def polite (msg):
    def inner (func):
            def wrapper (*arg,**kwarg):
                print(f"这是{msg}")
                return  func(*arg)
            return wrapper
    return inner

@polite('加法器')
def add(x,y):
    return x+y

# print(add(1,3))

@polite("乘法器")
def mult(a,b,*arg):
    result=a*b
    for mutiplier in arg :
        result*= mutiplier
    return result
#endregion
# print(mult(3,4,5))

class Polite :
    def __init__(self,msg):
        self.msg=msg
    def __call__(self,func):
        def polite (*arg):
            print(f"这是{self.msg}")
            return  func(*arg)
        return polite


@Polite("加法器")
def add(x,y):
    return x+y

print(add(1,3))
