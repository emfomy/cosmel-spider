# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import *

class CosmelSpider:

    def retry(res):
        if not res.request.meta.get('dont_cache'):
            logger().warning(f'RETRY {res.request.url}!')
            meta = res.request.meta
            meta['dont_cache'] = True
            yield res.request.replace(meta=meta, dont_filter=True)

    def do_items(self, *items):
        yield scrapy.Request(
            'dummy:',
            callback=partial(self.parse_items, items=items),
            meta={
                'dont_filter': True,
                'dont_cache': True,
            },
        )

    def parse_items(self, _, *, items):
        return iter(items)
