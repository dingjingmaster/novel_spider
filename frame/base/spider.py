#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.log.log import log
from frame.common.get import Get
"""
    抓取基类
        参数：
            1.种子url
        执行流程：
            1.使用种子url 根据url type 调用解析，获取基本信息，获取
"""


class Spider(object):
    def __init__(self):
        self._name = 'base_spider'
        self._webURL = ''

    def get_name(self):
        return self._name

    def get_web_url(self):
        return self._webURL

    def set_book_url(self, book_url: str):
        if None is not book_url and '' != book_url:
            self._bookList.append(book_url)

    def set_seed_url(self, for_url: str, mid_start: int, mid_end: int, back_url: str):
        key = for_url + '|' + back_url
        val = str(mid_start) + '|' + str(mid_end)
        self._seedURL[key] = val

    def get_book_list(self):
        if len(self._seedURL) <= 0:
            log.error(self._name + '由于未定义seed url 导致获取book list 失败！')
            return None
        try:
            for ik, iv in self._seedURL.items():
                arr1 = ik.split('|')
                arr2 = iv.split('|')
                for x in range(int(arr2[0]), int(arr2[1])):
                    self._bookList.append(arr1[0] + str(x) + arr1[1])
            for i in self._bookList:
                yield i
        except Exception as e:
            log.error(self._name + '不符合的seed url 设置: ' + str(e))
            return None

    @staticmethod
    def http_get(url: str, resource_method=1):
        if resource_method == 1:
            return Get(url).html()
        else:
            return Get(url).binary()

    """ 抓取新的书籍信息并保存MySQL """
    def run(self):
        pass

    """ 针对已抓取书籍检查是否有更新并保存MySQL """
    def check(self):
        pass
    _name = ''
    _webURL = ''
    _bookList = []
    _seedURL = {}
