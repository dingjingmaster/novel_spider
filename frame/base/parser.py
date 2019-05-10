#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-

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
        self.webURL = ''
        self.parserName = 'base_parser'

    def parser_book_url(self, url: str, doc: str) -> (bool, str):
        return

    def parser_book_img_url(self, url: str, doc: str) -> (bool, str):
        return

    def parser_book_chapter_base_url(self, url: str, doc: str) -> (bool, str):
        return

    def parser_book_chapter_url(self, url: str, doc: str) -> (bool, dict, dict, dict):
        return

    def parser_book_name(self, url: str, doc: str) -> (bool, str):
        return

    def parser_book_author(self, url: str, doc: str) -> (bool, str):
        return

    def parser_book_category(self, url: str, doc: str) -> (bool, str):
        return

    def parser_book_desc(self, url: str, doc: str) -> (bool, str):
        return

    def parser_book_status(self, url: str, doc: str) -> (bool, str):
        return

    def parser_book_img_content(self, url: str, doc: str) -> (bool, bytes):
        return

    PARSER_BOOK_URL = 1
    PARSER_BOOK_IMG_URL = 2
    PARSER_BOOK_CHAPTER_BASE_URL = 3
    PARSER_BOOK_CHAPTER_URL = 4
    PARSER_BOOK_NAME = 5
    PARSER_BOOK_AUTHOR = 6
    PARSER_BOOK_CATEGORY = 7
    PARSER_BOOK_DESC = 8
    PARSER_BOOK_STATUS = 9
    PARSER_BOOK_IMG_CONTENT = 10



