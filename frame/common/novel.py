#!/usr/bin/env python
# -*- encoding=utf8 -*-
import re
import time
import base64
import hashlib
from frame.log.log import log


class Novel:
    def __init__(self, url: str):
        self._info = Novel.NovelInfo()
        self._chapter = []
        self._url = url

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

        def get_nid(self):
            return self._nid

        def set_name(self, name):
            if None is not name:
                self._name = Novel.norm_name(name)
            return self

        def get_name(self):
            return self._name

        def set_author(self, author):
            if None is not author:
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
            if None is not url:
                self._chapter_base_url = url
            return self

        def get_chapter_base_url(self):
            return self._chapter_base_url

        def set_img_url(self, url: str):
            if None is not url:
                self._img_url = url
            return self

        def get_img_url(self):
            return self._img_url

        def get_img_content(self):
            return self._img_content

        def set_img_content(self, content):
            if None is not content:
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


