# -*- coding: utf-8 -*-

import scrapy

from utils.logging import logger

def retry(res):
    if not res.request.meta.get('dont_cache'):
        logger().warning(f'RETRY {res.request.url}!')
        meta = res.request.meta
        meta['dont_cache'] = True
        yield res.request.replace(meta=meta, dont_filter=True)
