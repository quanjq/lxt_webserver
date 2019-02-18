# -*- coding:utf-8 -*-
import sys
import os
dir_sign=os.path.split(os.path.realpath(__file__))[0] #将当前的目录sign加入sys的path路径，方便 python执行时能够找到自定义的库
sys.path.append(dir_sign)
from wsgiref.simple_server import make_server #由于该server只能支持单线程，因此一般只作测试之用
from urlconf import  urlConf
import urllib



# 不同的网址有不同的结果，但是所有的处理逻辑写到一起，很混乱
def application(environ, start_response):
    url = environ['PATH_INFO']
    if url=="/update-action/":
        request_body_size = int(environ.get('CONTENT_LENGTH', '0'))
        request_body = environ['wsgi.input'].read(request_body_size) #提取post请求的body数据
        request_bod=request_body.replace('&','=')
        data_list = request_bod.split('=',5)
        msg_recevieUrl=urllib.unquote(data_list[1]) #python2 直接用 urllib，python3需要用urllib.parse.unquote（）
        msg_from_pjs=urllib.unquote(data_list[3]).replace('+'," ")
        msg_from_lxt=urllib.unquote(data_list[5]).replace('+',' ')
        response_fun=urlConf[0][1]
        response_body=response_fun(msg_recevieUrl,msg_from_pjs,msg_from_lxt)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return response_body
    else:
        response_fun = None
        for item in urlConf:
            if url == item[0]:
                response_fun = item[1]
                break
        if response_fun:
            request_body_size = int(environ.get('CONTENT_LENGTH', '0'))
            request_body = environ['wsgi.input'].read(request_body_size) #提取post请求的body数据
            data_list = request_body.split('=',1)
            encryptMsg = data_list[1].replace('%3D','=')
            start_response('200 OK', [('Content-Type', 'text/html')])
            response_body = response_fun(encryptMsg)
        else:
            start_response('404 Not Found', [('Content-Type', 'text/html')])
            response_body = [bytes('<h1>404 !</h1>'.encode("utf-8"))]
        return response_body


def run_server(host,port):
    server = make_server(host, port, application)
    server.serve_forever()

if __name__ == '__main__':
    host="10.1.20.85"
    port=8002
    run_server(host,port)