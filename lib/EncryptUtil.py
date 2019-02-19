#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: alvis
@file: EncryptUtil.py
@time: 2018/4/18 14:05
"""

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES3

import base64
import json
import sys
import os
dir_sign=os.path.split(os.path.realpath(__file__))[0]
sys.path.append(dir_sign)


class EncryptUtil(object):
    """docstring for EncryptUtil"""
    def __init__(self,pub_key_file,pri_key_file):
        super(EncryptUtil, self).__init__()    #super
        self.padmode = 2   # 1: PAD_NORMAL    2: PAD_PKCS5   #
        self._pub_key=open(pub_key_file).read()
        self._pri_key=open(pri_key_file).read()

    def _encrypt_key(self,key): #非对称加密key ，使用RSA
        #print (type(self._pub_key))
        rsakey=RSA.importKey(self._pub_key)
        cipher=Cipher_pkcs1_v1_5.new(rsakey)
        return base64.b64encode(cipher.encrypt(key))

    def _decrypt_key(self,enc_key):
        rsakey=RSA.importKey(self._pri_key)
        cipher=Cipher_pkcs1_v1_5.new(rsakey)
        random_generator = Random.new().read
        return cipher.decrypt(base64.b64decode(enc_key), random_generator)

    def _encrypt_text(self,text,key):
        #=key对称加密报文,使用DES3，密钥key为3*8=24字节。
        # DES使用的密钥key为8字节，初始向量IV也是8字节。
        # 以8字节为一个块进行加密，一个数据块一个数据块的加密，一个8字节的明文加密后的密文也是8字节。
        # 如果明文长度不为8字节的整数倍，添加值为0的字节凑满8字节整数倍。所以加密后的密文长度一定为8字节的整数倍。

        text=self._pad(text)  #使明文长度为8字节的整数倍
        iv = ''.join([chr(val) for val in [0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF]])  #chr(val)将十进制数转化为基础字符
        # print (iv)
        des = DES3.new(key, DES3.MODE_ECB, iv)
        enc_text=base64.b64encode(des.encrypt(text))
        return enc_text

    def _decrypt_text(self,enc_text,key):
        iv = ''.join([chr(val) for val in [0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF]])
        des = DES3.new(key, DES3.MODE_ECB, iv)
        dec_text=des.decrypt(base64.b64decode(enc_text))
        return self._unpad(dec_text)

    def _pad(self, x):
        x=x.decode('utf-8')
        len_x = len(x)
        filling = 8 - len_x % 8
        if self.padmode == 2:
            fill_char = chr(filling)
        else:
            fill_char = "\0"
        return ( x + fill_char * filling )

    def _unpad(self, x):
        x=x.decode('utf-8')
        if self.padmode == 2:
            return x[0:-ord(x[-1])]
        return x.rstrip("\0")#删除 string 字符串末尾的指定字符（默认为空格）

    def encrypt(self,msg):
        key=Random.new().read(24)#使用DES3，密钥key为3*8=24字节,16字节也可以
        # print (len(key))
        # print (key)
        enc_key=self._encrypt_key(key).decode('utf-8')
        enc_text=self._encrypt_text(msg,key).decode('utf-8')
        obj={
            'encryptedText':enc_text,
            'keyInfo':{
                'encryptedKey':enc_key,
                'receiverX509CertSN':'123123',
            }
        }
        l=json.dumps(obj).encode('utf-8')
        return base64.b64encode(l)




    def decrypt(self,msg):
        obj=json.loads(base64.b64decode(msg))
        enc_key=obj['keyInfo']['encryptedKey']
        enc_text=obj['encryptedText']
        dec_key=self._decrypt_key(enc_key)
        dec_text=self._decrypt_text(enc_text,dec_key)
        return dec_text

if __name__ == '__main__':


    enc=EncryptUtil('pub.key','pri.key')
    # msg=b'eyJlbmNyeXB0ZWRUZXh0Ijoic2RoclNVRk5nMHpkR0R4bC8zN3QvZVM5MWNjUCtURkFHaVVTQTFFUzhkODZWNTJ1SGR3a3dDZWxKSmdEMGdJUjNobnpMQWUxNUZ5MHd0azFWbkRld1RmQlhBY1pXbEl5UWptMkFxdE9WRmdXaUhzN1lEVHdDNEpLL2tvS1ZSWi9hQXpyR00vV2thc2l4T3Z4ZDFlWGJUNzM2TG42WEsxZFZySTdEZUtITngvNjViNGZjaDBTWlpvdDA4ZDZXZFUrM1pUNStLN0VlOUpSK3kraVlOaXEzWm5CeG9OYzFDak5NeDU1VGhmMGc0cHNSaHRQUXFFcTRlOWI1bGFyL1JGTW5rR3IrOGNncjZjc1BMQmErTG1ycFoxR0ovM0lhemp0eDF3d1ZibUlLenJUTWJ4bTNWZU9LY0dMOW9uMk8xZVdGMGZYazd0UmdZU3ZxR09lY1RYN0F2ZmVVQnBXSVd5Y3d0Z0d5N2J6WG52c2Q3UDN2bzlyTlZQdnQvdkhvSHVBTEdsZkQydkVqN2trSzdpODZFSUpiNVFPVlBsaVZKSTB2T2xsc0N2Z3VLMHFKL0ZnS0pYQVBFdjRDam9lbkx6a3VtbFBaSmJaZlZtbURQdERPdEYvTkVUd01yS1EyRFN1RE9hU1QwTE9jUVdYT0FxY1BxaTBKdXhLdG1IcWJibkZyYVFPaDA0aVNvQVVManZpckZLYkRsNUZRSmtsZDZZOFFVUi9mMUNsc0pOWURYSFJZSVgyLzN5Nm8rMEMxaGtWbFdFeGx0TFFha29PTEdnK1QzWitsSm9HaVNCVE00Wjc5bkR1Yk9Cam1DNEpDd0JyWWd0SFVPem1xaTNvNmt2ckF6d1dETzlNeXRER2Y3ZkZtTFlTYjhuSzBuR29QZWdOREo5QXRZUjlwQzI4SDNObGg4YnlpL2tPb2hGY2pPVS9EOHVYNlVkOU9qcG4vSndVa3dtRXhMc25HZlk0c1hFY2RXMEkyU2ZEUU5SMXZleW8wSVFkdithMkx2bHQ4YUtlTmtXSW8zeEdsT3JjM2ZrUDJ5WXRHQkl1aTgvb1Eza0JOdXpubWk0VXBsYW9MYmU4TEJPWXRoaEY0cWJreVZmWklQSXk2V0ExbWRwVmYxa3kwek5XcytZSTBRd1g2azlyQzhBdDZiRTF0c1lHNlM4N3hxV0tNZlZvL2ZGWmo1WXFGTDlDNVlyanhkNm9QOHpINUlqeG5iWm9oWHJvZi9kRUVkTk5rQ1lQZlVEWStaUkMvWTZrOUE3Q1hsSWQzb0NtUzI4N0plY2RsV29XelZjcFUvM20zRUJFY3BtU001Z0RLcCtuTjMzZnJuL2NOdWJiOGJkc0xFWkFrTENlb3NVaW4rSmFCejdrd3poeUlrTzdtQXRWaE5heXQ1SEFTc0FlZFlrVmUwMnZZKzd0WWJ5TEhGeE5mOGo1eWhQQnViM1dOZk85OGtzZHVoTWRjWlZ4Y2IwSEdnUmtGTGtBWGdKSUhwaWVhVWEwOUpqems2dEhFS0lUT0V5SjVCZ04rZ0NjRmloSnFYYXNPSFVSMDAyUUpnOTlRTDByUjc2U3N6WCtISURkMWpISVdSZk1RSDNaaG5iSE5TM21rZkJocWJoQ25XcVV6eGdZc25zPSIsImtleUluZm8iOnsiZW5jcnlwdGVkS2V5IjoiUXMxWWpnRFpKMHNmc0FMeE5EUkhhZnlXNDFxWVpnbGU4cHlJVlRaZWREOS9XR0xLWlZZVXNRVVJHRmlGeVVlL205aXF0QURFQ1ZIUVlNcTNrRFJFQktTQVhzNFd5NlJFN0wrU2lvc3k3VFEwY3llZXgyUVhPTjJFcUl2STZoV1R2ZlF0Z1hTWGw2K0NKVUo3bG9WSGhGWi9hbDJhajBaanVrTndQYXM2Z2lWWFk2MDZwOFlhcjBXWXN2SE00VS9NWlJyQVUvOU92RkJNcy91Z3JBKy9Gd0dIMWVCdVN2Y1Nsck9LNjJlTmI0K1N0a002T2ZTeGNmb1kwVGZmamNHa25JL1RURndxYTZ4TnJWUWJyTE1sckhMbmMxcGYvMWN6bk5ucFlFNGVnZVNVaEpaZkF0R2xIQzNkTzhiRlJqSE1lU0JVUDI4MUxiU01VMmlUY3ZWN2tBPT0iLCJyZWNlaXZlclg1MDlDZXJ0U04iOiIxMDc3NjQxODgifX0='
    # dec_text= enc.decrypt(msg)
    # print (dec_text)

    dec2_text='{"acctNo":"9999987803163084","bankCod":"308","bankNm":"招商银行","custId":"1000000015","custNm":"黄秀美","custType":"1","idNo":"350321199002242628","idType":"A","orgCode":"105584099990002","recevieUrl":"http://127.0.0.1:8000/testa","sessionContext":{"accessSource":"WINDOWS-PC","accessSourceType":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36","authorizationReason":"","channel":"WEB","customerId":"1000000015","customerLimit":"0101101111000000","customerType":"1","customerValidationStatus":"1110001111100000","entityCode":6070,"externalReferenceNo":"201812201419238883","originalReferenceNo":"201812201419426277","postingDateText":"2018-12-20 14:19:42 581","remoteIp":"10.1.20.85, 10.1.1.67","serviceCode":"p2p1v3_159","transactionBranch":"1001","userReferenceNumber":"201812201419426785"},"telNo":"13715248761"}'
    enc_text=enc.encrypt(dec2_text.encode('utf-8'))
    print (enc_text)
