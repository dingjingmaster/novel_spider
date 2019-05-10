#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.spiders.feidu_34fd import FeiduSpider


class SpiderFactory:
    def get_spider(self, spider_name: str):
        if spider_name in self._spiderDict:
            return self._spiderDict[spider_name]
    _spiderDict = {
        '34fd_com': FeiduSpider(),
    }