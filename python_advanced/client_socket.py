import socket

#创建socket对象
client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

#连接服务器IP ，端口
client_socket.connect(("127.0.0.1",8000))

#发送数据
client_socket.send(" i'am client".encode())

#接收服务器数据
resp=client_socket.recv(1924).decode()
print(resp)

