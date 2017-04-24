#!/bin/bash
# -*-coding=utf-8-*-
import re
import sys
import os
import MySQLdb
from ml.util.schemas import *
from ml.util.encrypt import *
from sys import argv
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')


class Bayes(object):
    @classmethod
    def make_model(cls, clzss):
        _clzss = clzss.decode('gbk')
        try:
            modelfile = sys.path[0] + '/model/' + Encrypt.hmacmd5(_clzss.encode('utf-8')) + '.txt'  # 模型文件位置
            result = file(modelfile, 'w+')
            keyword_set = cls.get_keyword(_clzss)
            for label, keyword, newword in keyword_set:
                words = set(filter(lambda s: s and s.strip(), (str(keyword) + ',' + str(newword)).replace('None', '').split(',')))
                for word in words:
                    result.write(label + ' ' + word + '\n')
            result.close()
        except:
            result.close()
            os.remove(modelfile)
            print str(traceback.format_exc())
            exit(0)

    @staticmethod
    def get_keyword(clzss):
        try:
            conn = MySQLdb.connect(host=bayes['host'], port=bayes['port'], user=bayes['user'], passwd=bayes['passwd'], db=bayes['db'], charset='utf8')
            cur = conn.cursor()
            result_set = cur.fetchmany(cur.execute(
                'SELECT '
                'label,keyword,newword '
                'FROM '
                'model '
                'WHERE '
                'clzss = "{0}" '
                'AND '
                '('
                'keyword IS NOT NULL AND keyword != "" '
                'OR '
                'newword IS NOT NULL AND newword != ""'
                ')'.format(clzss)
            ))
            cur.close()
            conn.commit()
            conn.close()
            return result_set
        except:
            print str(traceback.format_exc())
            exit(0)


if __name__ == '__main__':
    Bayes.make_model(argv[1])
