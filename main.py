#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from url.ccuu234 import cc_uu234
from frame.log.log import log
from frame.thread import ThreadPool
from frame.spider_factory import SpiderFactory


if __name__ == '__main__':
    log.info('抓取任务开始执行...')
    spiderFactory = SpiderFactory()
    tpool = ThreadPool()

    """ www.uu234.cc """
    ccuu234 = spiderFactory.get_spider('cc_uu234')
    ccuu234.set_seed_url('http://www.uu234.cc/quanben/list_', 1, 390, '.html')         # 全本书籍
    tpool.set_spider(ccuu234)

    """ 开始运行 """
    tpool.run()
    log.info('抓取任务完成!')

    exit(0)
