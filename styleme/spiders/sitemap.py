# -*- coding: utf-8 -*-

import json
import urllib

import scrapy

from utils.logging import logger

from ..items import *

API_PREFIX = 'https://styleme.pixnet.net/api'

class Spider(scrapy.Spider):
    name = __name__.split('.')[-1]
    allowed_domains = ['styleme.pixnet.net']
    start_urls = ['https://styleme.pixnet.net/sitemap.xml']

    def parse(self, res):
        s = scrapy.utils.sitemap.Sitemap(res.body)
        for loc in s:
            o = urllib.parse.urlparse(loc['loc'])
            if o.path.startswith('/products/'):
                url = f'{API_PREFIX}{o.path}'
                yield scrapy.Request(
                    url,
                    callback=self.parse_product,
                    meta={ 'dont_redirect': True },
                )

    def parse_product(self, res):
        data = json.loads(res.body)
        assert not data['error']
        p = data['product']
        yield BrandItem(
            id=p['brand_id'],
            name=p['brand'],
        )
        yield ProductItem(
            id=p['id'],
            name=p['name'],
            brand=p['brand'],
        )
