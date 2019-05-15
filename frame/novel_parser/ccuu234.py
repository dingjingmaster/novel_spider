#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
import re
import pyquery
from frame.log.log import log
from frame.common.param import *
from frame.base.parser import Parser


class CCuu234Parser(Parser):
    __doc__ = """http://www.uu234.cc 解析器"""

    def __init__(self):
        super().__init__()
        _webURL = CC_UU234_WEB_URL
        _parserName = CC_UU234_NAME
        log.info('name:' + self._parserName + ' url:' + self._webURL + ' 解析器安装成功!')

    def _parser_book_name(self, doc: str) -> (bool, str):
        flag = False
        name = pyquery.PyQuery(doc).find('.green').text()
        if None is not name and '' != name:
            flag = True
        return flag, name

    def _parser_book_author(self, doc: str) -> (bool, str):
        flag = False
        author = pyquery.PyQuery(doc).find('.width111>a').text()
        if None is not author and '' != author:
            flag = True
        return flag, author

    def _parser_book_category(self, doc: str) -> (bool, str):
        flag = False
        text = pyquery.PyQuery(doc).find('.jhfd').text()
        if None is not text and '' != text:
            flag = True
            res = re.search('^\[\S+\]', text)
            if None is not res:
                text = res.group(0)
        return flag, text

    def _parser_book_url(self, doc: str) -> (bool, str):
        flag = False
        text = pyquery.PyQuery(doc).find('.green').attr('href')
        if None is not text and '' != text:
            flag = True
        return flag, text

    def _parser_book_status(self, doc: str) -> (bool, str):
        flag = False
        text = pyquery.PyQuery(doc).find('.width85').text()
        if None is not text and '' != text:
            flag = True
        return flag, text

    def _parser_book_img_url(self, doc: str) -> (bool, str):
        flag = False
        text = pyquery.PyQuery(doc).find('.con_limg>img').attr('src')
        if None is not text and '' != text:
            flag = True
        return flag, text

    def _parser_book_desc(self, doc: str) -> (bool, str):
        flag = False
        text = pyquery.PyQuery(doc).find('.r_cons').text()
        if None is not text and '' != text:
            flag = True
        return flag, text

    def _parser_book_chapter_base_url(self, doc: str) -> (bool, str):
        flag = False
        text = pyquery.PyQuery(doc).find('.r_tools>.diralinks').attr('href')
        if None is not text and '' != text:
            flag = True
        return flag, text

    def _parser_book_chapter_url(self, doc: str) -> (int, str, str):
        index = 0
        text = pyquery.PyQuery(doc).find('.dirwraps>div').eq(4).find('li>a')
        if None is not text and '' != text:
            for cp in text.items():
                index += 1
                name = cp.text()
                cp_url = cp.attr('href')
                yield index, name, cp_url

    def _parser_book_chapter_content(self, doc: str) -> (bool, dict, dict, dict):
        flag = False
        text = pyquery.PyQuery(doc).find('.readbg>.content').text()
        if None is not text and '' != text:
            flag = True
        return flag, text
