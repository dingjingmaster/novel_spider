#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.log.log import log
from frame.base.parser import Parser
from frame.web.ccuu234 import *


class CCuu234Parser(Parser):
    _webURL = CC_UU234_WEB_URL
    _parserName = CC_UU234_NAME

    def __init__(self):
        log.info('name:' + self._parserName + ' url:' + self._webURL + ' 解析器安装成功!')