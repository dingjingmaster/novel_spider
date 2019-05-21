#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
from frame.log.log import log
from frame.thread import ThreadPool
from frame.spider_factory import SpiderFactory
from url.ccuu234 import cc_uu234 as uu234


if __name__ == '__main__':
    log.info('抓取任务开始执行...')
    spiderFactory = SpiderFactory()
    tpool = ThreadPool()

    """ www.uu234.cc 开始 """
    ccuu234 = spiderFactory.get_spider('cc_uu234')
    ccuu234.set_seed_urls(uu234)
    tpool.set_spider(ccuu234)
    """ www.uu234.cc 结束 """

    tpool.run()
    log.info('抓取任务完成!')
    exit(0)
