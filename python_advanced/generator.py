import time

with open ('./python_advanced/what_you_show.txt' , 'r',encoding='utf-8' ) as f :
    literal=f.read()


def gen (*arg):
    yield from arg

iter1=gen(*literal)

for item in iter1:
    print(item,end=" ",flush=True) 
    time.sleep(0.5)

    