from abc import ABC , abstractmethod
import json
class Book :
    def __init__(self,book_id,title,author,total_num):
        self.book_id  =book_id
        self.title    =title
        self.author   =author
        self.total_num=total_num
        self.__ava_num=total_num
    def borrow_book (self):
        if self.__ava_num >0 :
            self.__ava_num-=1
            return True
        return False

    def return_book (self):
        self.__ava_num+=1
        return True
    
    def get_ava_num (self):
        return self.__ava_num 


class Member (ABC) :
    def __init__(self,id,name,password):
        self.id  = id
        self.name=name
        self.__password=password
        self.__borrowed_books=[]

    def borrow_book (self ,Book:Book) :
        if len(self.__borrowed_books) == self.get_max_num():
            print('达到最大借阅数量，借阅失败')
            return False
        if not Book.borrow_book() :
            print('借阅失败')
            return False
        else:
            self.__borrowed_books.append(Book)
            print('借阅成功')
            return True

    def return_book (self ,Book:Book):    
        if Book not in self.__borrowed_books :
            print("还没借呢！！")
            return False
        self.__borrowed_books.remove(Book)
        Book.return_book()
        return True
    
    def get_password(self):
        return self.__password

    def get_borrowed_book(self):
        return self.__borrowed_books

    @abstractmethod
    def get_max_num(self):
        pass


class NMember (Member):

    def get_max_num(self):
        return 3

class VMember (Member):
    def __init__(self, id, name, password ,vip_level):
        super().__init__(id, name, password)
        self.vip_level = vip_level
    
    def get_max_num (self):
        return 6+self.vip_level

class Library_System :
    def __init__(self):
        self.books = {} 
        self.members={}
        self.current_member=None
        self.load_book_data()
        self.load_member_data()
        self.run()
    
    def load_book_data(self):
        with open("crawl/books.json" , "r" , encoding="UTF-8") as f:
            books_data = json.load(f)
            for book in books_data :
                self.books[book["编号"]] = Book(book['编号'] , book["标题"] ,book["作者"] ,book["数量"])
        print("书籍信息加载成功")
    def load_member_data(self):
        with open("crawl/members.json" , "r" , encoding="UTF-8") as f:
            members_data = json.load(f)
            for member in members_data :
                if member['卡号'].startswith ('N'):
                    self.members[member["卡号"]] = NMember(member['卡号'] , member["姓名"] ,member["密码"])
                elif member['卡号'].startswith("V"):    
                    self.members[member["卡号"]] = VMember(member['卡号'] , member["姓名"] ,member["密码"] ,member["会员等级"])
        print("会员信息加载成功")
    
    def login(self) :
        print('欢迎使用图书管理系统')
        while True :
            member_id=input('请输入会员id')

            if member_id not in self.members :
                print('查无此人')
                continue


            while True :
                member_password = input('请输入会员密码')
                if member_password != self.members[member_id].get_password():
                    print('密码不对')
                    continue
                else : 
                    print(f'欢迎{self.members[member_id].name}')
                    self.current_member:Member=self.members[member_id]
                    return True

    def return_book(self) :
        book = input('要归还的书籍编号')
        if book not in self.books :
            print('没有这本书')
            return False
        self.current_member.return_book(self.books[book])
    
    def borrow_book(self):
        self.book_list()
        book = input('要借阅书籍的编号')
        if book not in self.books :
            print('没有这本书')
        else :
            self.current_member.borrow_book(self.books[book])

    def book_list(self):
        for idx in self.books:
            print(self.books[idx].book_id , self.books[idx].title ,self.books[idx].author ,self.books[idx].get_ava_num())

    def borrowed_book(self):
        for book in self.current_member.get_borrowed_book():
            print(book.book_id , book.title ,book.author)

    def run(self):
        if self.login():
            while True :
                print('1 借书')
                print('2 还书')
                print('3 已借')
                print('4 退出')
                choice = input('请选择操作\n')
                match choice :
                    case '1':
                        self.borrow_book()
                    case '2':
                        self.return_book()
                    case '3':
                        self.borrowed_book()
                    case '4':
                        print('bye~')
                        break


if __name__ == "__main__" :       
    ls = Library_System()






        