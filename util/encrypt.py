#!/bin/bash
# -*-coding=utf-8-*-
import hashlib
import types
import sys
import hmac

reload(sys)
sys.setdefaultencoding('utf-8')


class Encrypt(object):
    '''
    加密key
    '''
    _HMA_CMD5 = "qwertyuiopasdfghjklzxcvbnm"

    @classmethod
    def hmacmd5(cls, str):
        '''
        hmacmd5加密字符串
        :param str:
        :return:
        '''
        if type(str) is types.StringType:
            return hmac.new(cls._HMA_CMD5, str, hashlib.md5).hexdigest()
        else:
            return ''

    @classmethod
    def args_decode(self, str):
        return str.decode('gbk')


if __name__ == '__main__':
    print Encrypt.hmacmd5('学习')
