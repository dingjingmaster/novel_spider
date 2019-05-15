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

    """ www.uu234.cc 开始 """
    ccuu234 = spiderFactory.get_spider('cc_uu234')
    ccuu234.set_seed_url('http://www.uu234.cc/xuanhuan/list_update_', 1, 75, '.html')           # 玄幻魔法
    ccuu234.set_seed_url('http://www.uu234.cc/wuxia/list_update_', 1, 38, '.html')              # 武侠修真
    ccuu234.set_seed_url('http://www.uu234.cc/dushi/list_update_', 1, 105, '.html')             # 现代都市
    ccuu234.set_seed_url('http://www.uu234.cc/yanqing/list_update_', 1, 82, '.html')            # 言情小说
    ccuu234.set_seed_url('http://www.uu234.cc/junshi/list_update_', 1, 11, '.html')             # 历史军事
    ccuu234.set_seed_url('http://www.uu234.cc/jingji/list_update_', 1, 18, '.html')             # 游戏竞技
    ccuu234.set_seed_url('http://www.uu234.cc/kehuan/list_update_', 1, 32, '.html')             # 科幻灵异
    ccuu234.set_seed_url('http://www.uu234.cc/shenmei/list_update_', 1, 8, '.html')             # 耽美小说
    ccuu234.set_seed_url('http://www.uu234.cc/tongren/list_update_', 1, 7, '.html')             # 同人小说
    ccuu234.set_seed_url('http://www.uu234.cc/qita/list_update_', 1, 65, '.html')               # 其它小说
    ccuu234.set_seed_url('http://www.uu234.cc/quanben/list_', 1, 390, '.html')                  # 全本书籍
    tpool.set_spider(ccuu234)
    """ www.uu234.cc 结束 """

    tpool.run()
    log.info('抓取任务完成!')
    exit(0)
