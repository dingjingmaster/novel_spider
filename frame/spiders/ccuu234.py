#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.log.log import log
from frame.base.spider import Spider


class CCuu234Spider(Spider):
    def __init__(self):
        self.name = 'cc_uu234'
        self.webURL = 'http://www.uu234.cc/'
        log.info('name:' + self.name + ' url:' + self.webURL + ' spider安装成功!')

    def run(self):
        for url, info in self.bookList.items():
            arr = info.split()

            pass

        pass

