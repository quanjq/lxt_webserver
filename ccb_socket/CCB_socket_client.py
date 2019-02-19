# -*- coding:utf-8 -*-

import  socket

host='127.0.0.1'
port=10037
bufsiz=1024
addr=(host,port)
send_data='fffff'

tcpcl=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpcl.connect(addr)
buffer=[]
while True:
    tcpcl.send(send_data)
    recive_data=tcpcl.recv(bufsiz)
    if not recive_data:
        break
    print(recive_data)
    buffer.append(recive_data)
tcpcl.close()
data=b''.join(buffer)
print data