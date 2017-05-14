#!/bin/bash
# -*-coding=utf-8-*-
'''
    根据关键词爬取百度百科
    http://baike.baidu.com/search/word?word=  # 得到url的方法
'''
import re
import MySQLdb
import sys
from ml.util.schemas import *
from ml.util.encrypt import *
import traceback
import math
import os

reload(sys)
sys.setdefaultencoding('utf-8')


class Recommend(object):
    def __init__(self):
        self._fileName = '{0}/ml/cf/user.txt'.format(sys.path[7]);
        self._min = 0
        self._max = 255.25
        # self._max = 1010.49285462  one day

    def make_model(self):
        result_set = self.get_result_set()
        model = open(self._fileName, 'w')
        try:
            for aid, nid, views, cost in result_set:
                model.write('{0},{1},{2}\n'.format(aid, nid, self.rate(views, cost)))
                # model.write('{0},{1},{2}\n'.format(i, nid, self.rate(views, cost)))
            model.close()
        except:
            model.close()
            os.remove(self._fileName)
            print str(traceback.format_exc())
            exit(0)

    def rate(self, views, cost):
        return self.normalization(views + math.log(cost / 60 + 1, 2))
        # return round(views + math.log(cost / 60 + 1, 2), 0)

    def normalization(self, x):
        return (x - self._min) / (self._max - self._min)

    def get_result_set(self):
        conn = MySQLdb.connect(host=demo_web['host'], port=demo_web['port'], user=demo_web['user'], passwd=demo_web['passwd'], db=demo_web['db'],
                               charset='utf8')
        cur = conn.cursor()
        try:
            result_set = cur.fetchmany(cur.execute('SELECT aid,nid,views,cost FROM recommend'))
            cur.close()
            conn.commit()
            conn.close()
            return result_set
        except:
            print str(traceback.format_exc())
            exit(0)


if __name__ == '__main__':
    recommend = Recommend()
    recommend.make_model()
