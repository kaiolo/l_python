class Node:
    def __init__(self , item):
        self.item = item
        self.prev =None
        self.next =None
    def __repr__(self):
        return str(self.item)
#doubly circular linked list
class DCLL:
    def __init__(self,head:Node|None =None ,tail:Node|None =None ):
        self.head=None
        self.tail=None
    def is_empty(self):
        if self.head == None:
            return True
        return False
    def head_add(self ,node:Node):
        if self.is_empty():
            self.head=node
            self.tail=node
            node.next=node
            node.prev=node
        else:
            node.next=self.head
            node.prev=self.tail
            self.head.prev=node
            self.tail.next=node
            self.head=node
            
    def tail_add(self,node:Node):
        if self.is_empty():
            self.head=node
            self.tail=node
            node.next=node
            node.prev=node
        else:
            node.prev=self.tail
            node.next=self.head
            self.head.prev=node
            self.tail.next=node
            self.tail     =node

    def insert(self ,idx,node:Node):
        if idx>self.__len__() or idx<0:
            raise IndexError
        if idx==0:
            self.head_add(node)
            return True
        if idx==self.__len__():
            self.tail_add(node)
            return True
        cur = self.head    
        for _ in range(idx):
            cur=cur.next
        node.next=cur
        node.prev=cur.prev
        cur.prev.next=node
        cur.prev=node
        return True
    
    def __len__(self):
        cur = self.head
        counter=1
        while not self.is_empty():
            if id(self.head) == id(self.tail) :
                return 1
            elif not id(cur)==id(self.tail):
                cur=cur.next
                counter+= 1
                continue
            return counter
        return 0
    
    def get(self,idx):
        if idx>=self.__len__() or idx<0:
            raise IndexError
        cur=self.head
        for _ in range(idx):
            cur=cur.next
        return cur
    
    def __repr__(self ,reverse=None):
        if self.is_empty():
            return "[]"
        if not reverse :
            cur=self.head
            repr_str=cur.__repr__()
            for _ in range(self.__len__()-1):
                cur=cur.next
                repr_str =repr_str + " " + cur.__repr__()
            return '[' + repr_str+ "]"
        if reverse :
            cur=self.tail
            repr_str=cur.__repr__()
            for _ in range(self.__len__()-1):
                cur=cur.prev
                repr_str =repr_str + " " + cur.__repr__()
            return '[' + repr_str+ "]"
        
    def remove(self , val):
        if self.is_empty():
            return False
        cur=self.head
        len=self.__len__()
        while len:
            if cur.item==val:
                prev=cur.prev
                next=cur.next
                prev.next=next
                next.prev=prev
                if len==1:
                    self.tail=prev
                if id(cur)==id(self.head):
                    self.head=next
                if len==1 and id(cur)==id(self.head):
                    self.head=None
                    self.tail=None
                return True
            cur=cur.next
            len-=1
            continue
        return False

    def remove_at(self,idx):
        len=self.__len__()
        if idx>=len or idx<0:
            raise IndexError
        cur=self.head
        if idx==0:
            if len==1:
                self.head=None
                self.tail=None  
            else:
                prev=cur.prev
                next=cur.next
                prev.next=next
                next.prev=prev
                self.head=next
            return True
        for _ in range(idx):
            cur=cur.next
        prev=cur.prev
        next=cur.next
        prev.next=next
        next.prev=prev
        if idx == len-1:
            self.tail=prev
        return True
    
    def find(self , val):    
        if self.is_empty():
            return False
        cur=self.head
        if cur.item==val:
            return 0
        counter=0
        for _ in range(self.__len__()-1):
            cur=cur.next
            counter+=1
            if cur.item == val:
                return counter
            
    def traverse(self , reverse=None):
        if not reverse :
            print (self)
        else : print(self.__repr__(reverse=True))

    def clear(self):
        self.head=None
        self.tail=None
        
if __name__ == "__main__":
    d = DCLL()
    print("=== Test1 空链表 ===")
    print("empty:", d.is_empty())
    print("len:", len(d))
    d.traverse()
    print("find 5:", d.find(5))
    try:
        d.get(0)
    except IndexError:
        print("get(0) 正确抛IndexError")
    print("remove 10:", d.remove(10))
    print()

    print("=== Test2 单节点 ===")
    d.tail_add(Node(10))
    print("len:", len(d))
    d.traverse()
    d.traverse(reverse=True)
    print("find 10 -> idx:", d.find(10))
    print("remove 10:", d.remove(10))
    print("empty after remove:", d.is_empty())
    print()

    print("=== Test3 连续尾插 ===")
    for v in [1,2,3]:
        d.tail_add(Node(v))
    print("len", len(d))
    d.traverse()
    d.traverse(reverse=True)
    print("find 2:", d.find(2))
    print("get(2):", d.get(2))
    print()

    print("=== Test4 头插 ===")
    d.head_add(Node(0))
    d.head_add(Node(-1))
    d.traverse()
    print()

    print("=== Test5 insert 中间、头部、尾部 ===")
    d.insert(2, Node(99))
    print("insert idx2, val99:")
    d.traverse()
    d.insert(0, Node(-100))
    print("insert idx0 -100:")
    d.traverse()
    d.insert(len(d), Node(200))
    print("insert tail idx=%d, 200:" % len(d))
    d.traverse()
    print()

    print("=== Test6 remove_at 删除头、尾、中间 ===")
    d.remove_at(0)
    print("remove_at 0:")
    d.traverse()
    d.remove_at(len(d)-1)
    print("remove_at tail:")
    d.traverse()
    d.remove_at(2)
    print("remove_at idx2:")
    d.traverse()
    print()

    print("=== Test7 remove 按值删除 存在/不存在 ===")
    d.traverse()
    print("remove 99:", d.remove(99))
    d.traverse()
    print("remove 999(不存在):", d.remove(999))
    print()

    print("=== Test8 clear ===")
    d.clear()
    print("after clear empty:", d.is_empty(), "len:", len(d))
    d.traverse()

        
        
        
        

