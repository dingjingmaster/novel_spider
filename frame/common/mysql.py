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

    def get_novel_info_by_nid(self, novel_id):
        flag = False
        nid, name, author, category, describe, complete, parser, book_url, img_url, img_content, chapter_base_url, \
        create_time, update_time, hot, cp, lock = \
            0, '', '', '', '', 0, '', '', '', '', '', 0, 0, 0, 0, 0
        msql = 'SELECT `nid`, `name`, `author`, `category`, `describe`, `complete`, `parser`, `book_url`,' \
               '`img_url`, `img_content`, `chapter_base_url`, `create_time`, `update_time`,' \
               '`hot`, `cp`, `lock` FROM `novel_info` WHERE nid="{nid}";'\
               .format(nid=self._connect.escape_string(str(novel_id)))
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
        except Exception as e:
            log.error('MySQL 执行错误: ' + str(e))
        return (flag, nid, name, author, category, describe, complete, parser, book_url, img_url, img_content,
                chapter_base_url, create_time, update_time, hot, cp, lock)

    def get_novel_chapters_by_nid(self, novel_id):
        result_list = []
        msql = 'SELECT `cid`, `nid`, `index`, `chapter_url`, `name`, `content`, `update_time`,' \
               '`lock` FROM `novel_chapter` WHERE nid="{nid}"'\
               .format(nid=self._connect.escape_string(str(novel_id)))
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
        except Exception as e:
            log.error('MySQL 执行错误: ' + str(e))
        for i in result_list:
            yield i

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

    """ ok """
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

    """  """
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

    def update_novel_info_update_by_url(self, url: str, update: int):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET update_time = "{update_time}" WHERE book_url = "{book_url}";'\
            .format(update_time=self._connect.escape_string(str(update)), book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception as e:
            flag = False
            log.error('SQL执行失败: ' + str(e))
        return flag

    def update_novel_info_name_by_url(self, url: str, name: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET name = "{name}" WHERE book_url = "{book_url}";'\
            .format(name=self._connect.escape_string(str(name)), book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception as e:
            flag = False
            log.error('SQL执行失败: ' + str(e))
        return flag

    def update_novel_info_author_by_url(self, url: str, author: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET author = "{author}" WHERE book_url = "{book_url}";'\
            .format(author=self._connect.escape_string(str(author)), book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception as e:
            flag = False
            log.error('SQL执行失败: ' + str(e))
        return flag

    def update_novel_info_category_by_url(self, url: str, category: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET category = "{category}" WHERE book_url = "{book_url}";'\
            .format(category=self._connect.escape_string(str(category)), book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception as e:
            flag = False
            log.error('SQL执行失败: ' + str(e))
        return flag

    def update_novel_info_describe_by_url(self, url: str, describe: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET describe = "{describe}" WHERE book_url = "{book_url}";'\
            .format(describe=self._connect.escape_string(str(describe)), book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception as e:
            flag = False
            log.error('SQL执行失败: ' + str(e))
        return flag

    def update_novel_info_complete_by_url(self, url: str, complete: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET complete = "{complete}" WHERE book_url = "{book_url}";'\
            .format(complete=self._connect.escape_string(str(complete)), book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception as e:
            flag = False
            log.error('SQL执行失败: ' + str(e))
        return flag

    def update_novel_info_img_url_by_url(self, url: str, img_url: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET img_url = "{img_url}" WHERE book_url = "{book_url}";'\
            .format(img_url=self._connect.escape_string(str(img_url)), book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception as e:
            flag = False
            log.error('SQL执行失败: ' + str(e))
        return flag

    def update_novel_info_img_content_by_url(self, url: str, img_content: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET img_content = "{img_content}" WHERE book_url = "{book_url}";'\
            .format(img_content=self._connect.escape_string(str(img_content)),
                    book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception as e:
            flag = False
            log.error('SQL执行失败: ' + str(e))
        return flag

    def update_novel_info_chapter_base_url_by_url(self, url: str, chapter_base_url: str):
        flag = False
        can = self.novel_info_is_locked_by_url(url)
        if can:
            log.info('书籍信息被锁!不可修改!')
            return True
        msql = 'UPDATE `novel_info` SET chapter_base_url = "{chapter_base_url}" WHERE book_url = "{book_url}";'\
            .format(chapter_base_url=self._connect.escape_string(str(chapter_base_url)),
                    book_url=self._connect.escape_string(url))
        try:
            self._mutex.acquire()
            curosr = self._connect.cursor()
            curosr.execute(msql)
            novel_id = int(curosr.lastrowid)
            self._mutex.release()
            if novel_id > 0:
                flag = True
                log.info('更新小说信息 -- 最后更新时间!')
        except Exception as e:
            flag = False
            log.error('SQL执行失败: ' + str(e))
        return flag






