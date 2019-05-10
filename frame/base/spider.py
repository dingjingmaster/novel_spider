#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-

"""
    抓取基类
        参数：
            1.种子url
        执行流程：
            1.使用种子url 根据url type 调用解析，获取基本信息，获取
"""


class Spider(object):
    def __init__(self):
        self.name = 'base_parser'

    def run(self):
        print('ok')
    name = ''
    webURL = ''
    bookList = []
    startURL = ''




