#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
import time
from frame.log.log import log
from frame.common.param import *
from frame.common.novel import Novel
from frame.base.spider import Spider
from frame.parser_factory import get_parser


class CCuu234Spider(Spider):
    def __init__(self):
        self._name = CC_UU234_NAME
        self._webURL = CC_UU234_WEB_URL
        log.info('name:' + self._name + ' url:' + self._webURL + ' spider安装成功!')

    def check(self):
        check_index = 0
        check_all = 0
        check_error = 0
        check_update = 0
        check_update_chapter = 0
        check_update_exit_chapter = 0
        parser = get_parser().get_parser(CC_UU234_NAME)
        novel = Novel(CC_UU234_NAME)
        for book_url, img_url, chapter_base_url in novel.get_unlock_book_by_parser(CC_UU234_NAME):
            check_index += 1
            log.info('开始检查' + str(check_index) + '：' + book_url)
            check_all += 1
            text = Spider.http_get(book_url)
            if '' == text or None is text:
                check_error += 1
                log.error('获取书籍信息出错：' + book_url)
                continue
            flag, img_url_new = parser.parse(text, parse_type=parser.PARSER_BOOK_IMG_URL)
            if (img_url != img_url_new) and flag:
                check_update += 1
                novel.update_novel_info_img_url(book_url, img_url)
                img_content = Spider.http_get(img_url_new)
                if '' != img_content and None is not img_content:
                    check_update += 1
                    novel.update_novel_info_img_content(book_url, img_content)
            flag, chapter_url_new = parser.parse(text, parse_type=parser.PARSER_BOOK_CHAPTER_BASE_URL)
            if (chapter_base_url != chapter_url_new) and flag:
                check_update += 1
                novel.update_novel_info_chapter_base(book_url, chapter_url_new)
            text = Spider.http_get(chapter_url_new)
            if '' == text or None is text:
                check_error += 1
                log.error('获取书籍章节信息出错：' + chapter_url_new)
            for index, name, chapter_url in parser.parse(text, parse_type=parser.PARSER_BOOK_CHAPTER_URL):
                check_update_chapter += 1
                if novel.has_chapter(chapter_url):
                    check_update_exit_chapter += 1
                    log.info(name + '|' + chapter_url + '|' + name + '已经存在!')
                    continue
                c = Spider.http_get(chapter_url)
                if '' == text:
                    check_error += 1
                    log.error(name + '|' + chapter_url + '|' + name + '下载失败!')
                    continue
                flag, content = parser.parse(c, parse_type=parser.PARSER_BOOK_CHAPTER_CONTENT)
                if flag:
                    novel.save_check_novel_one_chapter(index, name, content, chapter_url, book_url)
            log.info('检查结束' + str(check_index) + '：' + book_url)
        log.info('检查结果：\
                \n\t\t总共：' + str(check_all) +\
                 '\n\t\t失败：' + str(check_error) +\
                 '\n\t\t成功更新：' + str(check_update) +\
                 '\n\t\t已有章节：' + str(check_update_exit_chapter) +\
                 '\n\t\t成功更新章节：' + str(check_update_chapter))
        time.sleep(3)
        return True

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
                if novel.has_book(url):
                    log.info(name + '|' + author + '已存在!')
                    continue
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
                if not novel.save_novel_info():
                    continue                                                    # 保存小说信息，上锁或出错则跳过
                for index, name, chapter_url in parser.parse(text, parse_type=parser.PARSER_BOOK_CHAPTER_URL):
                    # 测试是否已经包含章节信息
                    if novel.has_chapter(chapter_url):
                        log.info(novel.get_name() + '|' + novel.get_author() + '|' + name + '已经存在!')
                        continue
                    content = ''
                    novel.save_novel_one_chapter(index, name, content, chapter_url)
                    log.info('正在获取 ' + novel.get_name() + '|' + novel.get_author() + '|' + name + '|' + chapter_url)
                    c = Spider.http_get(chapter_url)
                    if '' == text:
                        log.error(novel.get_name() + '|' + novel.get_author() + '|' + name + '下载失败!')
                        continue
                    flag, content = parser.parse(c, parse_type=parser.PARSER_BOOK_CHAPTER_CONTENT)
                    if flag:
                        novel.save_novel_one_chapter(index, name, content, chapter_url)
        log.info(self._name + '执行完成!')


if __name__ == '__main__':
    cc = CCuu234Spider()
    cc.check()
    pass