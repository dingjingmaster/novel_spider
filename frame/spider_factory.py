#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.web.ccuu234 import *
from frame.spiders.ccuu234 import CCuu234Spider


class SpiderFactory:
    def get_spider(self, spider_name: str):
        if spider_name in self._spiderDict:
            return self._spiderDict[spider_name]
    _spiderDict = {
        CC_UU234_NAME: CCuu234Spider(),
    }
