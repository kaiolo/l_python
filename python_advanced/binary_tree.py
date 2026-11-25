class Node :
    def __init__(self , item):
        self.item = item
        self.lstree=None
        self.rstree=None
    def __repr__(self):
        return str(self.item)
class BinaryTree:
    def __init__ (self ,items=None ,*args):
        self.root=None
        if items!=None:
            if not hasattr(items,"__iter__"):
                self.add(items)
            else :
                for item in items :
                    self.add(item)
            for item in args:
                if not hasattr(item,"__iter__"):
                    self.add(item)
                else :
                    for i in item :
                        self.add(i)
    def is_empty(self):
        if self.root == None:
            return True
        return False
    def add (self , items ,*args):
        if self.is_empty() :
            if not hasattr(items,"__iter__"):
                self.root=Node(items)
            else :
                self.root=Node(items[0])
                for item in items[1:] :
                    self.__add_one(item)
        else:
            if not hasattr(items,"__iter__"):
                self.__add_one(items)
            else :
                for item in items :
                    self.__add_one(item)
        for item in args:
            if not hasattr(item,"__iter__"):
                self.__add_one(item)
            else :
                for i in item :
                    self.__add_one(i)      
    def __add_one(self , item):
        node=Node(item)
        queue=[]
        queue.append(self.root)
        while True:
            cur_root=queue.pop(0)
            if cur_root.lstree != None:
                queue.append(cur_root.lstree)
            else : 
                cur_root.lstree=node
                return 
            if cur_root.rstree != None:
                queue.append(cur_root.rstree)
            else: 
                cur_root.rstree=node
                return        
    def breadth_travel(self):
        if self.is_empty():
            print("这是一颗空树")
            return False
        queue=[]
        queue.append(self.root)
        while len(queue) != 0:
            cur_root=queue.pop(0)
            print(cur_root.item , end=' ')
            if cur_root.lstree != None:
                queue.append(cur_root.lstree)
            if cur_root.rstree != None:
                queue.append(cur_root.rstree)
    def deep_travel(self,root,mode='inner'):
        match mode :
            case "inner" :
                if root.lstree != None:
                    self.deep_travel(root.lstree ,mode="inner")
                print(root.item,end=' ')
                if root.rstree != None:
                    self.deep_travel(root.rstree ,mode="inner")

            case "prev":
                print(root.item,end=' ')
                if root.lstree != None:
                    self.deep_travel(root.lstree ,mode="prev")
                if root.rstree != None:
                    self.deep_travel(root.rstree ,mode="prev")

            case "post":
                if root.lstree != None:
                    self.deep_travel(root.lstree ,mode="post")
                if root.rstree != None:
                    self.deep_travel(root.rstree ,mode="post")
                print(root.item,end=' ')
    def __len__(self):
        if self.is_empty():
            return 0
        cur_node=self.root
        counter=1
        while True:
            cur_node=cur_node.lstree
            if cur_node != None:
                print(cur_node)
                counter+=1
            else:return counter
    def show_tree(self):
        def helper(node, prefix="", is_last=True):
            if node is not None:
                print(prefix + ("└── " if is_last else "┌── ") + str(node.item))
                new_prefix = prefix + ("    " if is_last else "│   ")
                # 先右，后左
                helper(node.rstree, new_prefix, False)
                helper(node.lstree, new_prefix, True)
        helper(self.root)  
if __name__ == '__main__':
    bt=BinaryTree([0,1,2],[3,4,5],6)
    bt.add(7,[8,9])
    # bt.breadth_travel()
    # node=bt.root
    # print('中序',end=' ')
    # bt.deep_travel(bt.root,mode="inner")
    # print(' ')
    # print('前序',end=' ')
    # bt.deep_travel(bt.root,mode="prev")
    # print(' ')
    # print('后序',end=' ')
    # bt.deep_travel(bt.root,mode="post")
    # print(' ')
    # print(len(bt))
    bt.show_tree()
    

    # for _ in range(4):
    #     node=node.lstree
    # print(node)
        