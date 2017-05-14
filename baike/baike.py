#!/bin/bash
# -*-coding=utf-8-*-
'''
    根据关键词爬取百度百科
    http://baike.baidu.com/search/word?word=  # 得到url的方法
'''
import urllib
import urllib2
from bs4 import BeautifulSoup
import jieba.analyse
import re
import MySQLdb
import sys
from ml.util.schemas import *
from ml.util.encrypt import *
import traceback
from sys import argv

reload(sys)
sys.setdefaultencoding('utf-8')


class Baike(object):
    def __init__(self):
        self._url = 'http://baike.baidu.com/search/word?word='  # 爬取链接
        self._name = 'div'  # 抓取页面的html标签
        self._attr = {'class': 'para'}  # 抓取页面的html标签属性
        self._encoding = 'utf-8'
        self._pattern = re.compile("\w|[/.,/#@$%^&]")  # 页面过滤内容
        self._topK = 30  # 关键词个数
        self._stopwords = '{0}/stopwords.txt'.format(sys.path[0])  # 停用词位置
        self._basePath = '{0}/ml/model/'.format(sys.path[7])  # 模型文件存放位置
        self._keyword = {}

    def craw(self, keyword):
        url = self.get_url(keyword)
        return self.passer(url, self.download(url))

    def get_url(self, keyword):
        return self._url + keyword

    def download(self, url):
        return urllib2.urlopen(url).read()

    def passer(self, url, html_count):
        soup = BeautifulSoup(html_count, 'html.parser', from_encoding=self._encoding)
        return self.get_content(soup)

    def get_content(self, soup):
        content = []
        summarys = soup.find_all(name=self._name, attrs=self._attr)
        for summary in summarys:
            content.append(summary.getText())
        result = re.sub(self._pattern, '', ''.join(content))
        return self.get_keyword(result)

    def get_keyword(self, content):
        keys = jieba.analyse.extract_tags(content, topK=self._topK)
        stopwords = self.load_stop_words()
        keywords = ','.join(set(keys) - set(stopwords))
        return keywords

    def load_stop_words(self):
        stop_words = [line.strip().decode(self._encoding) for line in open(self._stopwords).readlines()]
        return stop_words

    def create_file(self, mid, clzss):
        result = open('{0}.txt'.format(self._basePath + mid), 'a')
        for label, keyword in self._keyword.items():
            for word in keyword:
                result.write('{0} {1}\n'.format(label, word))
        result.close()

    def save(self, clzss, labels, mid):
        try:
            _clzss = Encrypt.args_decode(clzss)
            _label = Encrypt.args_decode(labels)
            _labels = _label.split(',')
            conn = MySQLdb.connect(host=demo_web['host'], port=demo_web['port'], user=demo_web['user'], passwd=demo_web['passwd'], db=demo_web['db'],
                                   charset='utf8')
            cur = conn.cursor()
            insert = "INSERT INTO model (label,keyword,clzss,mid) VALUES "
            for keyword, label in zip(map(lambda x: self.craw(x), _labels), _labels):
                self._keyword[label] = keyword.split(',')
                insert += "('{0}','{1}','{2}','{3}'),".format(label, keyword, _clzss, mid)
            cur.execute(insert[:-1])
            cur.close()
            conn.commit()
            conn.close()
            self.create_file(mid, clzss)
        except:
            print str(traceback.format_exc())
            exit(0)


if __name__ == '__main__':
    baike = Baike()
    baike.save(clzss=argv[1], labels=argv[2], mid=argv[3])
