import socket

#创建socket对象
sever_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

#绑定IP，端口
sever_socket.bind(("0.0.0.0",8000))

#最大监听数
sever_socket.listen(5)

#等待客户端连接
accept_socekt , client_info = sever_socket.accept()

#接受客户端数据
resp=accept_socekt.recv(1024).decode()
print(resp)

#给出回执
accept_socekt.send("hello".encode())