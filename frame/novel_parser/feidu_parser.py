#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.log.log import log
from frame.base.parser import Parser


class FeiduParser(Parser):
    webURL = 'http://www.34fd.com'
    parserName = '345fd_com'

    def __init__(self):
        log.info('name:' + self.parserName + ' url:' + self.webURL + ' 解析器安装成功!')







