# -*- coding: utf-8 -*-

import time
from queue import PriorityQueue

from pader.core.request import Request


class RequestQueue:
    """请求队列"""

    def __init__(self, qsize):
        self.pqueue = PriorityQueue(maxsize=qsize)

    def add(self, req: Request, force=True):
        """一个请求加入队列"""
        req.priority = req.priority or time.time()
        item = req.priority, req
        if force:
            self.pqueue.queue.append(item)
        else:
            self.pqueue.put(item)

    def get(self) -> Request | None:
        """从队列取出一个请求"""
        try:
            priority, req = self.pqueue.get(timeout=1)
            return req
        except:
            return

    def is_empty(self):
        return self.pqueue.empty()

    def is_full(self):
        return self.pqueue.full()

    def qsize(self):
        return self.pqueue.qsize()

    def __str__(self):
        return "<qsize={}>".format(self.qsize())
