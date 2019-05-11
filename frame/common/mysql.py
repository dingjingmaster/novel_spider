#!/usr/bin/env python
# -*- encoding=utf8 -*-
import time
import pymysql
import threading
from frame.log.log import log
from frame.common.param import *


class Mysql(object):
    _mutex = threading.Lock()
    _host = ''
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

    def set_usr(self, usr: str):
        self._user = usr
        return self

    def set_password(self, password: str):
        self._password = password
        return self

    def connect(self):
        self._connect = pymysql.Connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            charset='utf8'
        )
        return self

    def get_novel_info_by_url(self, url):
        flag = False
        nid, name, author, category, describe, complete, book_url, img_url, img_content,\
        chapter_base_url, create_time, update_time, hot, cp, lock = \
            0, '', '', '', '', 0, '', '', '', '', 0, 0, 0, 0, 0
        msql = 'SELECT `nid`, `name`, `author`, `category`, `describe`, `complete`, `book_url`,' \
               '`img_url`, `img_content`, `chapter_base_url`, `create_time`, `update_time`,' \
               '`hot`, `cp`, `lock` WHERE book_url=' + self._connect.escape_string(url)
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            result = curosr.fetchone()
            self._mutex.release()
            if None is not result:
                flag = True
                nid, name, author, category, describe, complete, book_url, img_url, img_content,\
                chapter_base_url, create_time, update_time, hot, cp, lock = \
                int(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]),\
                int(result[5]), str(result[6]), str(result[7]), bytes(result[8]), str(result[9]), \
                int(result[10]), int(result[11]), int(result[12]), int(result[13]), int(result[14])
        except Exception:
            log.error('MySQL 执行错误!')
        return (flag, nid, name, author, category, describe, complete, book_url, img_url, img_content,
                chapter_base_url, create_time, update_time, hot, cp, lock)

    def get_novel_info_by_nid(self, novel_id):
        flag = False
        nid, name, author, category, describe, complete, book_url, img_url, img_content, chapter_base_url, \
        create_time, update_time, hot, cp, lock = \
            0, '', '', '', '', 0, '', '', '', '', 0, 0, 0, 0, 0
        msql = 'SELECT `nid`, `name`, `author`, `category`, `describe`, `complete`, `book_url`,' \
               '`img_url`, `img_content`, `chapter_base_url`, `create_time`, `update_time`,' \
               '`hot`, `cp`, `lock` WHERE nid=' + self._connect.escape_string(str(novel_id))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            result = curosr.fetchone()
            self._mutex.release()
            if None is not result:
                flag = True
                nid, name, author, category, describe, complete, book_url, img_url, img_content, chapter_base_url, \
                create_time, update_time, hot, cp, lock = \
                    int(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), \
                    int(result[5]), str(result[6]), str(result[7]), bytes(result[8]), str(result[9]), \
                    int(result[10]), int(result[11]), int(result[12]), int(result[13]), int(result[14])
        except Exception:
            log.error('MySQL 执行错误!')
        return (flag, nid, name, author, category, describe, complete, book_url, img_url, img_content,
                chapter_base_url, create_time, update_time, hot, cp, lock)

    def get_novel_chapters_by_nid(self, novel_id):
        result_list = []
        msql = 'SELECT `cid`, `nid`, `index`, `chapter_url`, `name`, `content`, `update_time`,' \
               '`lock` WHERE nid = ' + self._connect.escape_string(str(novel_id))
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

    def insert_novel_info(self, name, author, category, describe, complete,\
                          book_url, img_url, img_content, chapter_base_url):
        flag = False
        novel_id = 0
        msql = 'INSERT INTO novel_info(`name`, `author`, `category`, `describe`, `complete`, `book_url`, `img_url`,\
         `img_content`, `chapter_base_url`) VALUES ("{name}", "{author}", "{category}", "{describe}", "{complete}",\
         "{book_url}", "{img_url}", "{chapter_base_url}");'.format(
            self._connect.escape_string(name), self._connect.escape_string(author),\
            self._connect.escape_string(category), self._connect.escape_string(describe),\
            complete, self._connect.escape_string(book_url), self._connect.escape_string(img_url),\
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
            msql = 'INSERT INTO novel_chapter(`nid`, `index`, `chapter_url`, `name`, `content`, `update_time`)' \
                   ' VALUES ("{nid}", "{index}", "{chapter_url}", "{name}", "{content}", "{update_time}");'.format( \
                self._connect.escape_string(str(novel_id)), self._connect.escape_string(str(index)),
                self._connect.escape_string(chapter_url), self._connect.escape_string(name),
                self._connect.escape_string(str(content)), self._connect.escape_string(str(time.time())))
            try:
                curosr.execute(msql)
            except Exception:
                return False
        return True

    """ 更新书籍信息 """



