# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from copy import copy
from typing import Iterable

from loguru import logger

from pader.core.queue import RequestQueue
from pader.core.request import Request
from pader.core.response import Response
from pader.core.spiders.base_spider import BaseSpider


class PaderSpider(BaseSpider):
    """多线程爬虫"""

    def __init__(self, qsize=10, speed=2):
        self.__request_queue = RequestQueue(qsize=qsize)
        self.__speed = speed
        self.__consumer = ThreadPoolExecutor(max_workers=speed)
        self.__worker = ThreadPoolExecutor(max_workers=speed)
        self.__fs = []

    def ready(self):
        result = self.start_requests()
        self.deal_result(result)

    def crawl(self):
        # 爬虫开始
        self.when_spider_start()

        # 爬虫流程
        self.__consumer.submit(self.ready)
        for _ in range(self.__speed):
            self.__consumer.submit(self.start_tasks)
        self.__consumer.shutdown()

        # 爬虫结束
        self.when_spider_close()

    def get_result(self, request: Request):
        """请求 ==> 中间件 ==> 响应 ==>  校验 ==> 回调"""
        request.middleware(request)
        resp = request.send()

        # 进入errback
        if resp is None:
            if hasattr(request, 'errback'):
                request.errback(request)
            return

        # 校验响应
        response = Response(resp)
        try:
            validate_result = self.validate(request, response)
        except Exception as e:
            logger.error(e)
        else:
            if validate_result is False:
                return

                # 进入回调函数
        try:
            result = request.callback(request, response)
        except Exception as e:
            logger.error(e)
        else:
            return result

    def job(self, request: Request):
        """结果 ==> 队列"""
        result = self.get_result(request)
        self.deal_result(result)

    def job_is_done(self):
        for f in copy(self.__fs):
            if not f.done():
                return False
            try:
                self.__fs.remove(f)
            except Exception as e:
                logger.error(e)

        for i in range(3):
            time.sleep(1)
            if len(self.__fs) != 0:
                return False
        else:
            return True

    def start_tasks(self):
        while True:
            if self.__request_queue.is_empty() and self.job_is_done():
                break

            request = self.__get_task()
            if request:
                f = self.__worker.submit(self.job, request)
                self.__fs.append(f)

    def deal_result(self, result):
        if result is None:
            return
        if not isinstance(result, Iterable):
            return
        for the in result:
            if isinstance(the, Request):
                self.__add_task(the)

    def __add_task(self, req: Request):
        """添加任务"""
        self.ensure_request(req)
        self.__request_queue.add(req)

    def __get_task(self):
        """获取任务"""
        return self.__request_queue.get()
