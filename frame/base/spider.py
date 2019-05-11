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
        self.name = 'base_spider'
        self.webURL = ''

    def set_book_url(self, book_url: dict):
        if len(book_url) > 0:
            self.bookList = book_url

    def set_seed_url(self, url: str):
        if '' != url and url is not None:
            self.startURL = url

    def run(self):
        pass

    name = ''
    webURL = ''
    bookList = {}
    startURL = ''




