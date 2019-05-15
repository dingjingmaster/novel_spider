#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
import threading
from frame.log.log import log
from frame.base.spider import Spider


class ThreadPool:
    _stop = False
    _thread = []
    _spider = []
    _thread_count = 10
    _mutex = threading.Lock()

    def set_pool_num(self, num: int):
        if num > self._thread_count:
            self._thread_count = num
        if self._thread_count > 100:
            self._thread_count = 100
        return self

    def set_spider(self, sp: Spider):
        self._mutex.acquire()
        self._spider.append(sp)
        self._mutex.release()

    def working(self, thread_id: int):
        log.info('spider id: ' + str(thread_id) + ' 启动成功!')
        while True:
            if self._mutex.acquire():
                spider: Spider = None
                if len(self._spider) > 0:
                    spider = self._spider.pop()
                    log.info('成功获取spider: ' + spider.get_name())
                self._mutex.release()
                if spider is None:
                    log.info('任务执行完毕! spider id: ' + str(thread_id) + ' 开始退出...')
                    break
                else:
                    log.info('spider: ' + spider.get_name() + '开始检查！')
                    spider.check()
                    log.info('spider: ' + spider.get_name() + '开始执行！')
                    spider.run()
                    log.info('spider: ' + spider.get_name() + '执行完成!')

    def run(self):
        """ 先添加，也可不添加 """
        for i in range(0, self._thread_count):
            t = ThreadPool.Thread(self.working, i + 1)
            self._thread.append(t)
        for i in self._thread:
            i.start()
        for i in self._thread:
            i.join()

    class Thread(threading.Thread):
        def __init__(self, route, tid: int):
            threading.Thread.__init__(self)
            self._tid = tid
            self._route = route

        def run(self):
            self._route(self._tid)

