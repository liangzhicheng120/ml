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
    def __init__(self):
        self._basePath = '{0}/ml/model/'.format(sys.path[7])

    def make_model(self, mid):
        fileName = '{0}{1}.txt'.format(self._basePath, mid)
        result = open(fileName, 'w+')
        try:
            keyword_set = self.get_keyword(mid)
            for label, keyword in keyword_set:
                # words = set(filter(lambda s: s and s.strip(), (str(keyword) + ',' + str(newword)).replace('None', '').split(',')))
                words = set(filter(lambda s: s and s.strip(), str(keyword).replace('None', '').split(',')))
                for word in words:
                    result.write(label + ' ' + word + '\n')
            result.close()
        except:
            result.close()
            os.remove(fileName)
            print str(traceback.format_exc())
            exit(0)

    def get_keyword(self, mid):
        try:
            conn = MySQLdb.connect(host=demo_web['host'], port=demo_web['port'], user=demo_web['user'], passwd=demo_web['passwd'], db=demo_web['db'],
                                   charset='utf8')
            cur = conn.cursor()
            result_set = cur.fetchmany(
                cur.execute('SELECT label,keyword FROM model WHERE mid = "{0}" AND (keyword IS NOT NULL AND keyword != "")'.format(mid)))
            cur.close()
            conn.commit()
            conn.close()
            return result_set
        except:
            print str(traceback.format_exc())
            exit(0)


if __name__ == '__main__':
    bayes = Bayes()
    bayes.make_model(mid=argv[1])
