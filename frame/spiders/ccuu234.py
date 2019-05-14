#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.log.log import log
from frame.base.spider import Spider
from frame.web.ccuu234 import *
from frame.common.novel import Novel


class CCuu234Spider(Spider):
    def __init__(self):
        self._name = CC_UU234_NAME
        self._webURL = CC_UU234_WEB_URL
        log.info('name:' + self._name + ' url:' + self._webURL + ' spider安装成功!')

    def run(self):
        for url in self.get_book_list():
            novel = Novel()
            text = Spider.http_get(url)
            if '' == text:
                continue

            print(text)
            exit(1)
            print(url)

