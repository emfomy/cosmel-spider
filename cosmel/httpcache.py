#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from scrapy.utils.request import request_fingerprint
from scrapy.extensions.httpcache import DummyPolicy, FilesystemCacheStorage

class CosmelPolicy(DummyPolicy):

    allow_http_codes = [200]

    def __init__(self, settings):
        super().__init__(settings)

    def should_cache_response(self, response, request):
        return response.status in self.allow_http_codes

class CosmelFilesystemCacheStorage(FilesystemCacheStorage):

    def _get_request_path(self, spider, request):
        key = request_fingerprint(request)
        return os.path.join(self.cachedir, key[0:2], key)
