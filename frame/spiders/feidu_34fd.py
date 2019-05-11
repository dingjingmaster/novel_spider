#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.log.log import log
from frame.base.spider import Spider
from frame.novel_parser.feidu_parser import FeiduParser


class FeiduSpider(Spider):
    def __init__(self):
        self.name = ''
        self.webURL = ''
        log.info('name:' + self.name + ' url:' + self.webURL + ' spider安装成功!')
