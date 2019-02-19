# -*- coding:utf-8 -*-

import socket

host='127.0.0.1'
port=10037
bufsiz=1024
addr=(host,port)
send_data='ceshiceshi'

tcpsk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建服务器的套接字
tcpsk.bind(addr)#将套接字与地址绑定
tcpsk.listen(5)#监听连接，传入连接请求的最大数为5
while True:#服务器无限循环等待c端的连接
    tcpsk_client,addr_client=tcpsk.accept()#接收c端的连接，并创建一个与这个c端的临时的套接字
    print '.....connected from:',addr_client
    while True:#在无限循环等待c端发送消息，如果发送为空
        recive_data=tcpsk_client.recv(bufsiz)#接收c端的信息，参数是一次只能接收最大的字节，剩下的可以第二次读取
        if not recive_data:
            break
        tcpsk_client.send(send_data)#向c端发送信息
    tcpsk_client.close()#关闭与c端的连接
tcpsk.close()#可选，现实中，服务器一般不会关闭的，而是一直不停的监听




