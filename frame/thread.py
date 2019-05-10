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
    _condition = threading.Condition(threading.Lock())

    def set_pool_num(self, num: int):
        if num > self._thread_count:
            self._thread_count = num
        if self._thread_count > 100:
            self._thread_count = 100
        return self

    def set_spider(self, sp: Spider):
        self._condition.acquire()
        if len(self._spider) > 10:
            self._condition.wait()
        else:
            self._mutex.acquire()
            self._spider.append(sp)
            self._mutex.release()
            self._condition.notify()

    def working(self, thread_id: int):
        log.info('spider id: ' + str(thread_id) + ' 启动成功!')
        while True:
            if self._condition.acquire():
                self._mutex.acquire()
                spider: Spider = None
                if len(self._spider) > 0:
                    spider = self._spider.pop()
                    log.info('成功获取spider: ' + spider.name)
                self._mutex.release()
                if spider is None:
                    self._condition.wait()
                else:
                    log.info('spider: ' + spider.name + '开始执行!')
                    spider.run()
                    log.info('spider: ' + spider.name + '执行完成!')
                    self._condition.notify()
                self._condition.release()

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

