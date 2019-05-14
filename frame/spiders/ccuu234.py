#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
import pyquery
from frame.log.log import log
from frame.base.spider import Spider
from frame.web.ccuu234 import *
from frame.parser_factory import get_parser
from frame.common.novel import Novel


class CCuu234Spider(Spider):
    def __init__(self):
        self._name = CC_UU234_NAME
        self._webURL = CC_UU234_WEB_URL
        log.info('name:' + self._name + ' url:' + self._webURL + ' spider安装成功!')

    def run(self):
        parser = get_parser().get_parser(CC_UU234_NAME)
        for url in self.get_book_list():
            text = Spider.http_get(url)
            if '' == text:
                continue
            doc = parser.parse(text, rule='body>div>.listconl>.clearfix')
            for ct in doc.children().items():
                novel = Novel(CC_UU234_NAME)
                flag, name = parser.parse(ct.html(), parse_type=parser.PARSER_BOOK_NAME)
                novel.set_name(name)
                flag, author = parser.parse(ct.html(), parse_type=parser.PARSER_BOOK_AUTHOR)
                novel.set_author(author)
                flag, url = parser.parse(ct.html(), parse_type=parser.PARSER_BOOK_URL)
                novel.set_book_url(url)
                flag, category = parser.parse(ct.html(), parse_type=parser.PARSER_BOOK_CATEGORY)
                novel.set_category(category)
                flag, status = parser.parse(ct.html(), parse_type=parser.PARSER_BOOK_STATUS)
                novel.set_complete(status)
                text = Spider.http_get(novel.get_book_url())
                if '' == text:
                    continue
                flag, img_url = parser.parse(text, parse_type=parser.PARSER_BOOK_IMG_URL)
                novel.set_img_url(img_url)
                flag, desc = parser.parse(text, parse_type=parser.PARSER_BOOK_DESC)
                novel.set_describe(desc)
                flag, chapter_url = parser.parse(text, parse_type=parser.PARSER_BOOK_CHAPTER_BASE_URL)
                novel.set_chapter_base_url(chapter_url)
                img_content = Spider.http_get(novel.get_img_url(), resource_method=2)
                novel.set_img_content(img_content)
                text = Spider.http_get(novel.get_chapter_base_url())
                if '' == text:
                    continue
                for index, name, chapter_url in parser.parse(text, parse_type=parser.PARSER_BOOK_CHAPTER_URL):
                    novel.add_chapter(index, name, chapter_url, '')
                    log.info('正在获取 ' + novel.get_name() + '|' + novel.get_author() + '|' + name + '|' + chapter_url)
                    c = Spider.http_get(chapter_url)
                    if '' == text:
                        log.error(novel.get_name() + '|' + novel.get_author() + '|' + name + '下载失败!')
                        continue
                    flag, content = parser.parse(c, parse_type=parser.PARSER_BOOK_CHAPTER_CONTENT)
                    if flag:
                        novel.set_chapter_content_by_index(index, content)
                    break
                novel.save_novel_info()
            exit(1)
            print(url)

