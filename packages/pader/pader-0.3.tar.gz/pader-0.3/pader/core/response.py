# -*- coding: utf-8 -*-

from parsel import Selector
from requests import Response as _Response


class Response(_Response):
    def __init__(self, resp: _Response):
        super().__init__()
        self.__dict__.update(resp.__dict__)
        self.sel = Selector(text=resp.text)

    def __str__(self):
        return '<Response {}>'.format(self.status_code)

    def xpath(self, query: str):
        return self.sel.xpath(query)

    def css(self, query: str):
        return self.sel.css(query)
