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
from ml.util.html import *
import traceback
import math
import os
from sys import argv
import jieba.analyse
from random import sample

reload(sys)
sys.setdefaultencoding('utf-8')


class Recommend(object):
    def __init__(self):
        self._recommend = "SELECT aid,nid,views,cost FROM recommend WHERE aid = '{0}'"
        self._note = "SELECT keyword FROM note WHERE id = '{0}'"
        self._suggest = "SELECT id,title FROM note WHERE content LIKE '%{0}%'"
        self._stopwords = '{0}/stopwords.txt'.format(sys.path[0])  # 停用词位置
        self._topK = 2  # 关键词个数
        self._encoding = 'utf-8'

    def run(self, aid):
        result = []
        result_map = {}
        result_set = self.get_result_set(self._recommend.format(aid))
        for aid, nid, views, cost in result_set:
            result_map[nid] = self.rate(views, cost)
        result_map = sorted(result_map.items(), key=lambda d: d[1], reverse=True)
        for nid, rate in result_map[:3]:
            for keyword in self.get_result_set(self._note.format(nid)):
                for word in keyword:
                    result += self.get_suggest(word)
        print ','.join(result)

    def get_suggest(self, word):
        random = set()
        for w in word.split(','):
            for nid, title in self.get_result_set(self._suggest.format(w)):
                random.add(str(nid))
        if (len(random) > 2):
            return sample(list(random), 3)
        else:
            return sample(list(random), 1)

    def rate(self, views, cost):
        return round(views + math.log(cost / 60 + 1, 2), 1)

    def get_keyword(self, content):
        keys = jieba.analyse.extract_tags(content, topK=self._topK)
        stopwords = self.load_stop_words()
        keywords = ','.join(set(keys) - set(stopwords))
        return keywords

    def load_stop_words(self):
        stop_words = [line.strip().decode(self._encoding) for line in open(self._stopwords).readlines()]
        return stop_words

    def get_result_set(self, sql):
        conn = MySQLdb.connect(host=demo_web['host'], port=demo_web['port'], user=demo_web['user'], passwd=demo_web['passwd'], db=demo_web['db'],
                               charset='utf8')
        cur = conn.cursor()
        try:
            result_set = cur.fetchmany(cur.execute(sql))
            cur.close()
            conn.commit()
            conn.close()
            return result_set
        except:
            print str(traceback.format_exc())
            exit(0)


if __name__ == '__main__':
    recommend = Recommend()
    recommend.run(aid='1')
