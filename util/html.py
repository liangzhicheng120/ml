#!/bin/bash
# -*-coding=utf-8-*-
'''
    html工具
'''
import re


class Html(object):
    @classmethod
    def delhtmltag(cls, html):
        '''
        去除html标签
        Parameters
        ----------
        html

        Returns
        -------

        '''
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html)
        return dd


if __name__ == '__main__':
    print Html.delhtmltag('<div>2.你输入的网址有误，请重新检查您输入的网址。</div>')
