#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
import pyquery
"""
    解析基类
        参数：
            1. 网站根 URL
            2. 解析器名字
            3. 解析类型：
                PARSER_BOOK_URL
                PARSER_BOOK_IMG_URL
                PARSER_BOOK_CHAPTER_BASE_URL
                PARSER_BOOK_CHAPTER_URL
                PARSER_BOOK_NAME
                PARSER_BOOK_AUTHOR
                PARSER_BOOK_CATEGORY
                PARSER_BOOK_DESC
                PARSER_BOOK_STATUS
                PARSER_BOOK_IMG_CONTENT
"""


class Parser(object):
    def __init__(self):
        self._webURL = ''
        self._parserName = 'base_parser'

    def _parser_book_url(self, doc: str) -> (bool, str):
        return

    def _parser_book_img_url(self, doc: str) -> (bool, str):
        return

    def _parser_book_chapter_base_url(self, doc: str) -> (bool, str):
        return

    def _parser_book_chapter_url(self, doc: str) -> (bool, dict, dict, dict):
        return

    def _parser_book_chapter_content(self, doc: str) -> (bool, str):
        return

    def _parser_book_name(self, doc: str) -> (bool, str):
        return

    def _parser_book_author(self, doc: str) -> (bool, str):
        return

    def _parser_book_category(self, doc: str) -> (bool, str):
        return

    def _parser_book_desc(self, doc: str) -> (bool, str):
        return

    def _parser_book_status(self, doc: str) -> (bool, str):
        return

    def get_parser_name(self):
        return self._parserName

    @staticmethod
    def _parser(doc: str, rule: str):
        return pyquery.PyQuery(doc).find(rule)

    def parse(self, doc: str, rule='', parse_type=-1):
        if self.PARSER_BOOK_URL == parse_type:
            return self._parser_book_url(doc)
        elif self.PARSER_BOOK_IMG_URL == parse_type:
            return self._parser_book_img_url(doc)
        elif self.PARSER_BOOK_CHAPTER_BASE_URL == parse_type:
            return self._parser_book_chapter_base_url(doc)
        elif self.PARSER_BOOK_CHAPTER_URL == parse_type:
            return self._parser_book_chapter_url(doc)
        elif self.PARSER_BOOK_NAME == parse_type:
            return self._parser_book_name(doc)
        elif self.PARSER_BOOK_AUTHOR == parse_type:
            return self._parser_book_author(doc)
        elif self.PARSER_BOOK_CATEGORY == parse_type:
            return self._parser_book_category(doc)
        elif self.PARSER_BOOK_DESC == parse_type:
            return self._parser_book_desc(doc)
        elif self.PARSER_BOOK_STATUS == parse_type:
            return self._parser_book_status(doc)
        elif self.PARSER_BOOK_CHAPTER_CONTENT == parse_type:
            return self._parser_book_chapter_content(doc)
        else:
            return Parser._parser(doc, rule)

    PARSER_BOOK_URL = 1
    PARSER_BOOK_IMG_URL = 2
    PARSER_BOOK_CHAPTER_BASE_URL = 3
    PARSER_BOOK_CHAPTER_URL = 4
    PARSER_BOOK_NAME = 5
    PARSER_BOOK_AUTHOR = 6
    PARSER_BOOK_CATEGORY = 7
    PARSER_BOOK_DESC = 8
    PARSER_BOOK_STATUS = 9
    PARSER_BOOK_CHAPTER_CONTENT = 10
