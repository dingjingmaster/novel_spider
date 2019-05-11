#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.spiders.ccuu234 import CCuu234Spider
from frame.spiders.feidu_34fd import FeiduSpider


class SpiderFactory:
    def get_spider(self, spider_name: str):
        if spider_name in self._spiderDict:
            return self._spiderDict[spider_name]
    _spiderDict = {
        'cc_uu234': CCuu234Spider(),
        'com_34fd': FeiduSpider(),
    }
