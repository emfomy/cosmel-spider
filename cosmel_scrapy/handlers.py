#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy

class DummyHandler:

    def __init__(self, settings):
        pass

    def download_request(self, request, spider):
        return scrapy.http.Response(request.url)
