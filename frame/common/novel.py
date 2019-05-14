#!/usr/bin/env python
# -*- encoding=utf8 -*-
import re
import time
import base64
import hashlib
from frame.log.log import log
from frame.common.param import *
from frame.common.mysql import Mysql


class Novel:
    def __init__(self, parser_name: str):
        self._parser_name = parser_name
        self._info = Novel.NovelInfo()
        self._mysql = Novel.NovelMysql()
        self._chapter = []

    def get_nid(self):
        return self._info.get_nid()

    def set_name(self, name):
        self._info.set_name(name)
        return self

    def get_name(self):
        return self._info.get_name()

    def set_author(self, author):
        self._info.set_author(author)
        return self

    def get_author(self):
        return self._info.get_author()

    def set_category(self, cate):
        self._info.set_category(cate)
        return self

    def get_category(self):
        return self._info.get_category()

    def set_describe(self, desc):
        self._info.set_describe(desc)
        return self

    def get_describe(self):
        return self._info.get_describe()

    def set_complete(self, status: str):
        self._info.set_complete(status)
        return self

    def get_complete(self):
        return self._info.get_complete()

    def get_complete_str(self):
        if self._info.get_complete() == 2:
            return '完结'
        elif self._info.get_complete() == 1:
            return '连载'
        else:
            return '状态不确定'

    def set_book_url(self, url):
        self._info.set_book_url(url)
        return self

    def get_book_url(self):
        return self._info.get_book_url()

    def set_chapter_base_url(self, url):
        self._info.set_chapter_base_url(url)
        return self

    def get_chapter_base_url(self):
        return self._info.get_chapter_base_url()

    def set_img_url(self, url: str):
        self._info.set_img_url(url)
        return self

    def get_img_url(self):
        return self._info.get_img_url()

    def get_img_content(self):
        return self._info.get_img_content()

    def set_img_content(self, content):
        self._info.set_img_content(content)
        return self

    def get_update_time(self):
        return self._info.get_update_time()

    def get_create_time(self):
        return self._info.get_create_time()

    def set_cp(self, cp: bool):
        self._info.set_cp(cp)
        return self

    def get_cp(self) -> bool:
        return self._info.get_cp()

    def get_lock(self) -> bool:
        return self._info.get_lock()

    def add_chapter(self, index: int, chapter_url: str, name: str, content: str):
        cp = Novel.NovelChapter()
        cp.set_nid(self.get_nid())\
            .set_index(index)\
            .set_chapter_url(chapter_url)\
            .set_chapter_name(name)\
            .set_chapter_content(content)
        self._chapter.append(cp)

    def set_chapter_content_by_index(self, index: int, content: str):
        for chapter in self._chapter:
            if index == chapter.get_index():
                ele = chapter
                self._chapter.remove(ele)
                ele.set_chapter_content(content)
                self._chapter.append(ele)

    """ ok """
    def save_novel_info(self):
        # 检测信息是否上锁
        if self._mysql.novel_info_is_locked_by_url(self.get_book_url()):
            log.info(self.get_name() + '|' + self.get_author() + '信息上锁!')
            return
        # 检测信息是否存在
        if self._mysql.novel_info_exist(self.get_book_url()):                       # 小说信息存在，更新
            log.info(self.get_name() + '|' + self.get_author() + '信息存在！开始更新...')
            self._mysql.update_novel_info_by_url(self.get_book_url(), self.get_name(), self.get_author(),
                        self.get_category(), self.get_describe(), self.get_complete(), self.get_img_url(),
                        self.get_img_content(), self.get_chapter_base_url(), self.get_update_time())
        else:                                                                       # 小说信息不存在，插入小说信息
            self._mysql.insert_novel_info(self.get_name(), self.get_author(), self.get_category(),
                        self.get_describe(), self.get_complete(), self._parser_name, self.get_book_url(),
                        self.get_img_url(), self.get_img_content(), self.get_chapter_base_url(),
                        self.get_create_time(), self.get_update_time())

    class NovelInfo:
        def __init__(self):
            self._nid = 0
            self._name = ''
            self._author = ''
            self._category = ''
            self._describe = ''
            self._img_content = ''
            self._img_url = ''
            self._book_url = ''
            self._chapter_base_url = ''
            self._cp = 0
            self._hot = 0
            self._lock = 0
            self._complete = 0
            self._create_time = int(time.time())
            self._update_time = int(time.time())

        def get_update_time(self):
            return self._update_time

        def get_create_time(self):
            return self._create_time

        def get_nid(self):
            return self._nid

        def set_nid(self, nid: int):
            if nid >= 0:
                self._nid = nid

        def set_name(self, name):
            if None is not name and '' != name:
                self._name = Novel.norm_name(name)
            return self

        def get_name(self):
            return self._name

        def set_author(self, author):
            if None is not author and '' != author:
                self._author = Novel.norm_author(author)
            return self

        def get_author(self):
            return self._author

        def set_category(self, cate):
            if None is not cate:
                self._category = Novel.norm_tag(cate)
            return self

        def get_category(self):
            return self._category

        def set_describe(self, desc):
            if desc is not None:
                self._describe = desc
            return self

        def get_describe(self):
            return self._describe

        def set_complete(self, status: str):
            if re.search(r'(完结|完成|结束|大结局|完本|完|结)', status):
                self._complete = 2
            elif re.search(r'(连载|未完成|断更|更新中|更)', status):
                self._complete = 1
            else:
                self._complete = 0
            return self

        def get_complete(self):
            return self._complete

        def set_book_url(self, url):
            if None is not url:
                self._book_url = url
            return self

        def get_book_url(self):
            return self._book_url

        def set_chapter_base_url(self, url):
            if None is not url and '' != url:
                self._chapter_base_url = url
            return self

        def get_chapter_base_url(self):
            return self._chapter_base_url

        def set_img_url(self, url: str):
            if None is not url and '' != url:
                self._img_url = url
            return self

        def get_img_url(self):
            return self._img_url

        def get_img_content(self):
            return self._img_content

        def set_img_content(self, content):
            if None is not content and '' != content:
                self._img_content = content
            return self

        def set_cp(self, cp: bool):
            if cp:
                self._cp = 0
            else:
                self._cp = 1
            return self

        def get_cp(self) -> bool:
            if self._cp == 0:
                return True
            return False

        def get_lock(self) -> bool:
            if 1 == self._lock:
                return True
            return False

    class NovelChapter:
        def __init__(self):
            self._cid = 0
            self._nid = 0
            self._index = 0
            self._chapter_url = ''
            self._name = ''
            self._content = ''
            self._lock = 0
            self._update_time = int(time.time())

        def set_cid(self, cid):
            if 0 == cid:
                self._cid = cid
            return self

        def get_cid(self):
            return self._cid

        def set_nid(self, nid):
            if 0 == nid:
                self._nid = nid
            return self

        def get_nid(self):
            return self._nid

        def set_index(self, index):
            if index >= 0:
                self._index = index
            return self

        def get_index(self):
            return self._index

        def set_chapter_url(self, url: str):
            if None is not url:
                self._chapter_url = url
            return self

        def get_chapter_url(self):
            return self._chapter_url

        def set_chapter_name(self, name: str):
            if None is not name:
                self._name = Novel.norm_name(name)
            return self

        def get_chapter_name(self):
            return self._name

        def set_chapter_content(self, content: str):
            if None is not content:
                self._content = content
            return self

        def get_chapter_content(self):
            return self._content

        def get_chapter_lock(self):
            return self._lock

    class NovelMysql(Mysql):
        def __init__(self):
            self.set_database(MYSQL_NOVEL_DB)\
                .set_ip(MYSQL_HOST)\
                .set_port(MYSQL_PORT)\
                .set_usr(MYSQL_USER)\
                .set_password(MYSQL_PASSWORD)\
                .connect()

    @staticmethod
    def norm_name(name: str) -> str:
        # 去掉所有非法字符
        name = re.sub(r'[\\/:*?"<>|.]', '', name)
        if None is name:
            name = ''
        return name

    @staticmethod
    def norm_author(author: str) -> str:
        author = re.sub(r'[\\/:*?"<>|.]', '', author)
        if author is None:
            author = ''
        return author

    @staticmethod
    def norm_tag(tag: str) -> str:
        tag = re.sub(r'[\\/:*?"<>|.\[\]]', '', tag)
        if tag is None:
            tag = ''
        return tag

    @staticmethod
    def encode(name: str) -> str:
        if None is name or '' == name:
            return ''
        m2 = hashlib.md5()
        m2.update(base64.b64encode(name.encode('utf8')))
        return m2.hexdigest()


