# -*-encoding:utf-8-*-
# __auther__='xiaopt'

from Crypto.Cipher import DES3
import base64

basekey = "333705661205A5E3D950933325240713"
key01 = 'UB7F6jKC15GrRQnjdr98IQ=='
keylist = ['UB7F6jKC15GrRQnjdr98IQ==', '7jFJnIo5sgiFoMlNxygk1w==', '8PvLYIZalNNxQcpkNXBlCw==',
           '2qgfU6wVa5EbA3DfRP4QwQ==', 'Ez7Cqi11TLWuql6MSKiNSw==', 'oKkl/Lff9E4ZPFGDkyt6Zw==',
           'GNQYuFE4URHPZzR6lixRvA==', 'rKXvS/2xWBtjf3mt+mRNSg==', '9FcI66fQrL5BFEQ35ZkgTQ==',
           'UqYsnp+5T5t5MtZ3Gu53rA==']


class CCBEncryptUtil(object):
    def __init__(self):  # , pub_key_file, pri_key_file
        super(CCBEncryptUtil, self).__init__()
        self.padmode = 1

    def _encrypt_text(self, key, msg):
        text = self._pad(msg)
        iv = ''.join([chr(x) for x in [0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF]])
        cipher = DES3.new(key, DES3.MODE_ECB, iv)
        return base64.b64encode(cipher.encrypt(text))

    def _decrypt_text(self, key, msg):
        iv = ''.join([chr(x) for x in [0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF]])
        cipher = DES3.new(key, DES3.MODE_ECB, iv)
        return self._unpad(cipher.decrypt(base64.b64decode(msg)))

    def _pad(self, x):
        len_x = len(x)
        filling = 8 - len_x % 8
        if self.padmode == 2:
            fill_char = chr(filling)
        else:
            fill_char = "\0"
        return (x + fill_char * filling)

    def _unpad(self, x):
        if self.padmode == 2:
            return x[0:-ord(x[-1])]
        return x.rstrip("\0")

    def _base_key_generator(self, basekey):
        strlen = len(basekey)
        list = [int('0x' + basekey[i:i + 2], 16) for i in range(0, strlen, 2)]
        print 'list',list
        listj= [int( basekey[j:j + 2], 16) for j in range(0, strlen, 2)]
        print 'listj',listj
        return ''.join(chr(item) for item in list)

    def get_real_key(self, keymsg):  # 获取建行真实加密秘钥
        basekeystrtest = self._base_key_generator(basekey)
        realkeystr = self._decrypt_text(basekeystrtest, keymsg)
        return realkeystr

    def encrypt_response(self, responsestr, keysqe):  # 加密响应报文
        keystr = keylist[keysqe]
        encryptstr = self._encrypt_text(self.get_real_key(keystr), responsestr)
        return base64.b64decode(encryptstr)

    def decrypt_request(self, requeststr, keysqe):  # 加密请求报文
        keystr = keylist[keysqe]
        request_decrypt = self._decrypt_text(self.get_real_key(keystr), requeststr)
        return request_decrypt


if __name__ == "__main__":
    requststr = """HxklZVhUSgiSWpubbsOr/T2QZFPc6dWIFJj8EKFk3j8aZ
                    nmAXoNv9pVpe7aeFw6e3uvqBEMq2A9+M3o66TO+td8owNuRcJ/AT58
                    rxGU2VeQULP3xthnyBPeLUovTb4dsE07zJ8DAUbLOkIz82P0CeXB4j
                    DG56vUkIdyCyb/gmg09JYj7767abU0dc1kEejdF"""
    crypt = CCBEncryptUtil()
    realkeystr = crypt.get_real_key(key01)
    request_decrypt = crypt.decrypt_request(requststr, 9)
    # print request_decrypt
    # request_encrypt = crypt.encrypt_response(request_decrypt, 9)
    # print base64.b64encode(request_encrypt)
