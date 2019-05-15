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
        msql = 'SELECT `nid`, `lock` FROM `novel_info` WHERE book_url = "{book_url}";'\
            .format(book_url=self._connect.escape_string(url))
        cursor = self._connect.cursor()
        try:
            cursor.execute(msql)
            result = cursor.fetchone()
            if None is not result:
                if int(result[1]) == 1:
                    flag = True
        except Exception as e:
            log.error('SQL 执行错误: ' + str(e))
        return flag

    def novel_info_unlock_book_url_by_parser(self, parser_name: str) -> (str, str, str):
        mlist = []
        msql = 'SELECT `book_url`, img_url, chapter_base_url FROM `novel_info` WHERE `parser`="{parser_name}" \
               AND `lock`=0'.format(parser_name=self._connect.escape_string(parser_name))
        cursor = self._connect.cursor()
        try:
            cursor.execute(msql)
            result = cursor.fetchall()
            if None is not result:
                for res in result:
                    book_url = res[0]
                    img_url = res[1]
                    chapter_base_url = res[2]
                    mlist.append((book_url, img_url, chapter_base_url))
        except Exception as e:
            log.error('获取所有书籍信息失败：' + str(e))
        for infos in mlist:
            yield infos

    def novel_chapter_is_locked_by_url(self, url: str) -> bool:
        flag = False
        msql = 'SELECT `cid`, `lock` FROM `novel_chapter` WHERE chapter_url = "{chapter_url}";'\
            .format(chapter_url=self._connect.escape_string(url))
        cursor = self._connect.cursor()
        try:
            cursor.execute(msql)
            result = cursor.fetchone()
            if None is not result:
                if int(result[1]) == 1:
                    flag = True
        except Exception as e:
            log.error('SQL 执行错误: ' + str(e))
        return flag

    def novel_info_exist(self, url: str) -> bool:
        flag = False
        msql = 'SELECT `nid` FROM `novel_info` WHERE book_url = "{book_url}";'\
            .format(book_url=self._connect.escape_string(url))
        cursor = self._connect.cursor()
        try:
            cursor.execute(msql)
            result = cursor.fetchone()
            if None is not result:
                flag = True
        except Exception as e:
            flag = False
            log.error('SQL 执行错误: ' + str(e))
        return flag

    def novel_chapter_exist(self, url: str) -> bool:
        flag = False
        msql = 'SELECT `cid` FROM `novel_chapter` WHERE chapter_url = "{chapter_url}";'\
            .format(chapter_url=self._connect.escape_string(url))
        cursor = self._connect.cursor()
        try:
            cursor.execute(msql)
            result = cursor.fetchone()
            if None is not result:
                flag = True
        except Exception as e:
            flag = False
            log.error('SQL 执行错误: ' + str(e))
        return flag

    def get_novel_id_by_url(self, url):
        flag = False
        nid = 0
        msql = 'SELECT `nid` FROM `novel_info` WHERE book_url="{book_url}";'\
                .format(book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            result = curosr.fetchone()
            self._mutex.release()
            if None is not result:
                flag = True
                nid = int(result[0])
        except Exception as e:
            log.error('MySQL 执行错误: ' + str(e))
        return flag, nid

    def get_novel_info_by_url(self, url):
        flag = False
        nid, name, author, category, describe, complete, parser, book_url, img_url, img_content,\
        chapter_base_url, create_time, update_time, hot, cp, lock = \
            0, '', '', '', '', 0, '', '', '', '', '', 0, 0, 0, 0, 0
        msql = 'SELECT `nid`, `name`, `author`, `category`, `describe`, `complete`, `parser`, `book_url`,'\
               '`img_url`, `img_content`, `chapter_base_url`, `create_time`, `update_time`,'\
               '`hot`, `cp`, `lock` FROM `novel_info` WHERE book_url="{book_url}";'\
                .format(book_url=self._connect.escape_string(url))
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
        except Exception as e:
            log.error('MySQL 执行错误: ' + str(e))
        return (flag, nid, name, author, category, describe, complete, parser, book_url, img_url, img_content,
                chapter_base_url, create_time, update_time, hot, cp, lock)

    """ ok """
    def insert_novel_info(self, name: str, author: str, category: str, describe: str, complete: int, parser: str,
                          book_url: str, img_url: str, img_content: str, chapter_base_url: str,
                          create_time: int, update_time: int) -> (bool, int):
        flag = False
        novel_id = -1
        msql = 'INSERT INTO `novel_info` (`name`, `author`, `category`, `describe`, `complete`, `parser`, `book_url`,'\
               ' `img_url`, `img_content`, `chapter_base_url`, `create_time`, `update_time`)' \
               ' VALUES ("{name}", "{author}", "{category}", "{describe}", "{complete}", "{parser}", "{book_url}",' \
               ' "{img_url}", "{img_content}", "{chapter_base_url}", "{create_time}", "{update_time}");'\
            .format(name=self._connect.escape_string(name), author=self._connect.escape_string(author),
                    category=self._connect.escape_string(category), describe=self._connect.escape_string(describe),
                    complete=complete, parser=self._connect.escape_string(parser),
                    book_url=self._connect.escape_string(book_url), img_url=self._connect.escape_string(img_url),
                    img_content=self._connect.escape_string(str(img_content)),
                    chapter_base_url=self._connect.escape_string(chapter_base_url),
                    create_time=create_time, update_time=update_time)
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            self._connect.commit()
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id >= 0:
                flag = True
                log.info(name + '|' + author + '信息保存成功!')
            else:
                log.error(name + '|' + author + '信息保存失败!')
        except Exception as e:
            log.error('MySQL 执行错误: ' + str(e))
        return flag, novel_id

    """ 根据URL更新书籍信息 """
    def update_novel_info_by_url(self, book_url: str, name: str, author: str, category: str, describe: str,
                                 complete: int, img_url: str, img_content: str, chapter_base_url: str, update_time: int):
        msql = 'UPDATE `novel_info` SET `name`="{name}", `author`="{author}", `category`="{category}", \
                `describe`="{describe}", `complete`="{complete}", `img_url`="{img_url}", `img_content`="{img_content}",\
                `chapter_base_url`="{chapter_base_url}", `update_time`="{update_time}" WHERE `book_url`="{book_url}";'\
                .format(name=self._connect.escape_string(name), author=self._connect.escape_string(author),
                        category=self._connect.escape_string(category), describe=self._connect.escape_string(describe),
                        complete=complete, img_url=self._connect.escape_string(img_url),
                        img_content=self._connect.escape_string(str(img_content)),
                        chapter_base_url=self._connect.escape_string(chapter_base_url),
                        update_time=update_time, book_url=self._connect.escape_string(book_url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            self._connect.commit()
            self._mutex.release()
            log.info(name + '|' + author + '信息更新成功！')
        except Exception as e:
            log.error('MySQL 执行错误: ' + str(e))
        return None

    """ 根据URL插入书籍信息 """
    def insert_novel_chapter(self, novel_id: int, index: int, chapter_url: str, parser: str,
                             name: str, content: str, update_time: int):
        msql = 'INSERT INTO `novel_chapter` (`nid`, `index`, `chapter_url`,`parser`,\
            `name`, `content`, `update_time`) VALUES \
             ("{nid}", "{index}", "{chapter_url}", "{parser}", "{name}", "{content}", "{update_time}");' \
            .format(nid=novel_id, index=index, chapter_url=self._connect.escape_string(chapter_url),
                    parser=self._connect.escape_string(parser), name=self._connect.escape_string(name),
                    content=self._connect.escape_string(str(content)), update_time=update_time)
        try:
            self._mutex.acquire()
            cursor = self._connect.cursor()
            cursor.execute(msql)
            self._connect.commit()
            self._mutex.release()
            log.info(str(index) + '|' + name + '|' + chapter_url + ' 章节信息插入成功！')
        except Exception as e:
            log.error('插入章节' + name + '错误：' + str(e))
            return False
        return True

    """ 根据URL更新书籍章节 """
    def update_novel_chapter_by_url(self, novel_id: int, index: int, chapter_url: str, name: str,
                                    content: str, update_time: int) -> bool:
        msql = 'UPDATE `novel_chapter` SET `nid` = "{nid}", `index`="{index}", `name`="{name}",\
            `content`="{content}", `update_time`="{update_time}" WHERE `chapter_url`="{chapter_url}";'\
            .format(nid=novel_id, index=index, name=self._connect.escape_string(name),
                    content=self._connect.escape_string(content), update_time=update_time,
                    chapter_url=self._connect.escape_string(chapter_url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            self._connect.commit()
            self._mutex.release()
            log.info(str(index) + '|' + name + '|' + chapter_url + ' 章节信息更新成功！')
        except Exception as e:
            log.error('章节信息更新失败: ' + str(e))
            return False
        return True

    """ 根据URL更新小说封面图片URL """
    def update_novel_info_img_url_by_url(self, book_url: str, img_url: str):
        if self.novel_info_is_locked_by_url(book_url):
            log.info('书籍信息被锁!不可修改!')
            return True
        if self.novel_info_exist(book_url):  # 小说信息存在，更新
            msql = 'UPDATE `novel_info` SET img_url = "{img_url}", `update_time`="{update}"\
                    WHERE book_url = "{book_url}";'\
                    .format(img_url=self._connect.escape_string(str(img_url)),
                            book_url=self._connect.escape_string(book_url),
                            update=int(time.time()))
            try:
                self._mutex.acquire()
                curosr = self._connect.cursor()
                curosr.execute(msql)
                self._mutex.release()
            except Exception as e:
                log.error('书籍封面页URL更新失败：: ' + str(e))
                return False
            else:
                log.error('要更新的小说信息不存在！')
                return False
        return True

    """ 根据URL更新小说封面图片 """
    def update_novel_info_img_content_by_url(self, book_url: str, img_content: str):
        if self.novel_info_is_locked_by_url(book_url):
            log.info('书籍信息被锁!不可修改!')
            return True
        if self.novel_info_exist(book_url):  # 小说信息存在，更新
            msql = 'UPDATE `novel_info` SET img_content = "{img_content}", `update_time`="{update}"\
                        WHERE book_url = "{book_url}";' \
                .format(img_content=self._connect.escape_string(str(img_content)),
                        book_url=self._connect.escape_string(book_url),
                        update=int(time.time()))
            try:
                self._mutex.acquire()
                curosr = self._connect.cursor()
                curosr.execute(msql)
                self._mutex.release()
            except Exception as e:
                log.error('书籍封面页更新失败：: ' + str(e))
                return False
            else:
                log.error('要更新的小说信息不存在！')
                return False
        return True

    """ 根据URL更新小说章节页URL """
    def update_novel_info_chapter_by_url(self, book_url: str, chapter_base_url: str):
        if self.novel_info_is_locked_by_url(book_url):
            log.info('书籍信息被锁!不可修改!')
            return True
        if self.novel_info_exist(book_url):  # 小说信息存在，更新
            msql = 'UPDATE `novel_info` SET chapter_base_url = "{chapter_base_url}", `update_time`="{update}"\
                            WHERE book_url = "{book_url}";' \
                .format(chapter_base_url=self._connect.escape_string(str(chapter_base_url)),
                        book_url=self._connect.escape_string(book_url),
                        update=int(time.time()))
            try:
                self._mutex.acquire()
                curosr = self._connect.cursor()
                curosr.execute(msql)
                self._mutex.release()
            except Exception as e:
                log.error('书籍章节页更新失败：: ' + str(e))
                return False
            else:
                log.error('要更新的小说信息不存在！')
                return False
        return True

    """ 根据URL更新小说章节页URL """
    def update_novel_info_chapter_by_url(self, book_url: str, chapter_base_url: str):
        if self.novel_info_is_locked_by_url(book_url):
            log.info('书籍信息被锁!不可修改!')
            return True
        if self.novel_info_exist(book_url):  # 小说信息存在，更新
            msql = 'UPDATE `novel_info` SET chapter_base_url = "{chapter_base_url}", `update_time`="{update}"\
                            WHERE book_url = "{book_url}";' \
                .format(chapter_base_url=self._connect.escape_string(str(chapter_base_url)),
                        book_url=self._connect.escape_string(book_url),
                        update=int(time.time()))
            try:
                self._mutex.acquire()
                curosr = self._connect.cursor()
                curosr.execute(msql)
                self._mutex.release()
            except Exception as e:
                log.error('书籍章节页更新失败：: ' + str(e))
                return False
            else:
                log.error('要更新的小说信息不存在！')
                return False
        return True



