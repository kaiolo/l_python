class degree :
    def __init__(self , level ,name):
        self.level=level
        self.name=name
    def __lt__ (self , other):
        return self.level<other.level
    def call(self):
        print(self.level)

    def __repr__(self):
        return self.name
      
kai=degree(4,'kai')
xu=degree(2,'xu')
xin=degree(3,'xin')
name=sorted([kai,xu,xin])
print(name)
