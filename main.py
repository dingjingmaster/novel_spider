#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.log.log import log
from frame.thread import ThreadPool
from frame.spider_factory import SpiderFactory

MAX_THREADS = 10


def create_new_thread():
    pass


def drop_thread():
    pass


if __name__ == '__main__':
    log.info('抓取任务开始执行...')
    spider = SpiderFactory()
    tpool = ThreadPool()
    tpool.set_spider(spider.get_spider('34fd_com'))
    tpool.run()
    log.info('抓取任务完成!')


    exit(0)
