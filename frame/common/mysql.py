#!/usr/bin/env python
# -*- encoding=utf8 -*-
import time
import pymysql
import threading
from frame.log.log import log


class Mysql(object):
    _mutex = threading.Lock()
    _host = ''
    _db = ''
    _port = 3306
    _user = ''
    _password = ''
    _connect = None

    def set_ip(self, host: str):
        self._host = host
        return self

    def set_port(self, port: int):
        self._port = port
        return self

    def set_database(self, db: str):
        self._db = db
        return self

    def set_usr(self, usr: str):
        self._user = usr
        return self

    def set_password(self, password: str):
        self._password = password
        return self

    def connect(self):
        self._connect = pymysql.Connect(
            host=self._host,
            port=self._port,
            user=self._user,
            db=self._db,
            passwd=self._password,
            charset='utf8'
        )
        return self

    def novel_info_is_locked_by_url(self, url: str) -> bool:
        flag = False
        msql = 'SELECT `nid`, `lock` FROM `novel_info` WHERE book_url = "{url}";'.format(self._connect.escape_string(url))
        cursor = self._connect.cursor()
        try:
            cursor.execute(msql)
            result = cursor.fetchone()
            if None is not result:
                if int(result[1]) == 1:
                    flag = True
        except Exception:
            log.error('SQL 执行错误')
        return flag

    def novel_info_exist(self, url: str) -> bool:
        flag = False
        msql = 'SELECT `nid` FROM `novel_info` WHERE book_url = "{url}";'.format(self._connect.escape_string(url))
        cursor = self._connect.cursor()
        try:
            cursor.execute(msql)
            result = cursor.fetchone()
            if None is not result:
                flag = True
        except Exception:
            flag = False
            log.error('SQL 执行错误')
        return flag

    def novel_chapter_exist(self, url: str) -> bool:
        flag = False
        msql = 'SELECT `nid` FROM `novel_chapter` WHERE chapter_url = "{url}";'.format(self._connect.escape_string(url))
        cursor = self._connect.cursor()
        try:
            cursor.execute(msql)
            result = cursor.fetchone()
            if None is not result:
                flag = True
        except Exception:
            flag = False
            log.error('SQL 执行错误')
        return flag

    def get_novel_info_by_url(self, url):
        flag = False
        nid, name, author, category, describe, complete, parser, book_url, img_url, img_content,\
        chapter_base_url, create_time, update_time, hot, cp, lock = \
            0, '', '', '', '', 0, '', '', '', '', '', 0, 0, 0, 0, 0
        msql = 'SELECT `nid`, `name`, `author`, `category`, `describe`, `complete`, `parser`, `book_url`,' \
               '`img_url`, `img_content`, `chapter_base_url`, `create_time`, `update_time`,' \
               '`hot`, `cp`, `lock` FROM `novel_info` WHERE book_url=' + self._connect.escape_string(url)
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            result = curosr.fetchone()
            self._mutex.release()
            if None is not result:
                flag = True
                nid, name, author, category, describe, complete, parser, book_url, img_url, img_content,\
                chapter_base_url, create_time, update_time, hot, cp, lock = \
                int(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]),\
                int(result[5]), str(result[6]), str(result[7]), str(result[8]), bytes(result[9]),\
                str(result[10]), int(result[11]), int(result[12]), int(result[13]), int(result[14]), int(result[15])
        except Exception:
            log.error('MySQL 执行错误!')
        return (flag, nid, name, author, category, describe, complete, parser, book_url, img_url, img_content,
                chapter_base_url, create_time, update_time, hot, cp, lock)

    def get_novel_info_by_nid(self, novel_id):
        flag = False
        nid, name, author, category, describe, complete, parser, book_url, img_url, img_content, chapter_base_url, \
        create_time, update_time, hot, cp, lock = \
            0, '', '', '', '', 0, '', '', '', '', '', 0, 0, 0, 0, 0
        msql = 'SELECT `nid`, `name`, `author`, `category`, `describe`, `complete`, `parser`, `book_url`,' \
               '`img_url`, `img_content`, `chapter_base_url`, `create_time`, `update_time`,' \
               '`hot`, `cp`, `lock` FROM `novel_info` WHERE nid=' + self._connect.escape_string(str(novel_id))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            result = curosr.fetchone()
            self._mutex.release()
            if None is not result:
                flag = True
                nid, name, author, category, describe, complete, parser, book_url, img_url, img_content,\
                chapter_base_url, create_time, update_time, hot, cp, lock = \
                    int(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), \
                    int(result[5]), str(result[6]), str(result[7]), str(result[8]), bytes(result[9]),\
                    str(result[10]), int(result[11]), int(result[12]), int(result[13]), int(result[14]), int(result[15])
        except Exception:
            log.error('MySQL 执行错误!')
        return (flag, nid, name, author, category, describe, complete, parser, book_url, img_url, img_content,
                chapter_base_url, create_time, update_time, hot, cp, lock)

    def get_novel_chapters_by_nid(self, novel_id):
        result_list = []
        msql = 'SELECT `cid`, `nid`, `index`, `chapter_url`, `name`, `content`, `update_time`,' \
               '`lock` FROM `novel_chapter` WHERE nid = ' + self._connect.escape_string(str(novel_id))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            results = curosr.fetchall()
            self._mutex.release()
            if None is not results:
                for result in results:
                    cid, nid, index, chapter_url, name, content, update_time, lock = \
                        int(result[0]), int(result[1]), int(result[2]), str(result[3]), str(result[4]), \
                        str(result[5]), int(result[6]), int(result[7])
                    result_list.append((cid, nid, index, chapter_url, name, content, update_time, lock))
        except Exception:
            log.error('MySQL 执行错误!')
        for i in result_list:
            yield i

    def insert_novel_info(self, name, author, category, describe, complete, parser,\
                          book_url, img_url, img_content, chapter_base_url):
        flag = False
        novel_id = 0
        msql = 'INSERT INTO `novel_info` (`name`, `author`, `category`, `describe`, `complete`, `parser`, `book_url`,' \
               ' `img_url`, `img_content`, `chapter_base_url`) VALUES ("{name}", "{author}", "{category}",' \
               ' "{describe}", "{complete}", "{parser}", "{book_url}", "{img_url}", "{chapter_base_url}");'.format(
            self._connect.escape_string(name), self._connect.escape_string(author), self._connect.escape_string(category),\
            self._connect.escape_string(describe), complete, self._connect.escape_string(parser),\
            self._connect.escape_string(book_url), self._connect.escape_string(img_url),\
            self._connect.escape_string(img_content), self._connect.escape_string(chapter_base_url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('MySQL存储小说信息成功!')
            else:
                log.error('MySQL存储小说信息失败')
        except Exception:
            log.error('MySQL 执行错误!')
        return flag, novel_id

    """ list(nid, index, chapter_url, name, content) """
    def insert_novel_chapter(self, novel_id, chapter_list):
        flag, nid, name, author, category, describe, complete, book_url, img_url, img_content,\
        chapter_base_url, create_time, update_time, hot, cp, lock = self.get_novel_info_by_nid(novel_id)
        if not flag or nid != novel_id:
            log.error('MySQL没有查找到指定书籍信息或书籍ID与给定的不符!章节保存失败!')
            return False
        curosr = self._connect.cursor()
        for nid, index, chapter_url, name, content in chapter_list:
            msql = 'INSERT INTO `novel_chapter` (`nid`, `index`, `chapter_url`, `name`, `content`, `update_time`)' \
                   ' VALUES ("{nid}", "{index}", "{chapter_url}", "{name}", "{content}", "{update_time}");'.format(\
                self._connect.escape_string(str(novel_id)), self._connect.escape_string(str(index)),
                self._connect.escape_string(chapter_url), self._connect.escape_string(name),
                self._connect.escape_string(str(content)), self._connect.escape_string(str(time.time())))
            try:
                curosr.execute(msql)
            except Exception:
                return False
        return True

    def update_novel_info_update_by_url(self, url: str, update: int):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET update_time = "{update_time}" WHERE book_url = "{book_url}";'.format(
            self._connect.escape_string(str(update)), self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception:
            flag = False
            log.error('SQL执行失败')
        return flag

    def update_novel_info_name_by_url(self, url: str, name: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET name = "{name}" WHERE book_url = "{book_url}";'.format(
            self._connect.escape_string(str(name)), self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception:
            flag = False
            log.error('SQL执行失败')
        return flag

    def update_novel_info_author_by_url(self, url: str, author: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET author = "{author}" WHERE book_url = "{book_url}";'.format(
            self._connect.escape_string(str(author)), self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception:
            flag = False
            log.error('SQL执行失败')
        return flag

    def update_novel_info_category_by_url(self, url: str, category: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET category = "{category}" WHERE book_url = "{book_url}";'.format(
            self._connect.escape_string(str(category)), self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception:
            flag = False
            log.error('SQL执行失败')
        return flag

    def update_novel_info_describe_by_url(self, url: str, describe: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET describe = "{describe}" WHERE book_url = "{book_url}";'.format(
            self._connect.escape_string(str(describe)), self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception:
            flag = False
            log.error('SQL执行失败')
        return flag

    def update_novel_info_complete_by_url(self, url: str, complete: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET complete = "{complete}" WHERE book_url = "{book_url}";'.format(
            self._connect.escape_string(str(complete)), self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception:
            flag = False
            log.error('SQL执行失败')
        return flag

    def update_novel_info_img_url_by_url(self, url: str, img_url: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET img_url = "{img_url}" WHERE book_url = "{book_url}";'.format(
            self._connect.escape_string(str(img_url)), self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception:
            flag = False
            log.error('SQL执行失败')
        return flag

    def update_novel_info_img_content_by_url(self, url: str, img_content: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET img_content = "{img_content}" WHERE book_url = "{book_url}";'.format(
            self._connect.escape_string(str(img_content)), self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception:
            flag = False
            log.error('SQL执行失败')
        return flag

    def update_novel_info_chapter_base_url_by_url(self, url: str, chapter_base_url: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET chapter_base_url = "{chapter_base_url}" WHERE book_url = "{book_url}";'.format(
            self._connect.escape_string(str(chapter_base_url)), self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception:
            flag = False
            log.error('SQL执行失败')
        return flag






