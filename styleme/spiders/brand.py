# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import logger

from ..items import *

class Spider(scrapy.Spider):
    name = __name__.split('.')[-1]
    allowed_domains = ['styleme.pixnet.net']
    start_urls = ['https://styleme.pixnet.net/api/searchbrands']

    def parse(self, res):
        data = json.loads(res.body)
        assert not data['error']
        for b in data['brands']:
            bid = b['id']
            yield BrandMetaItem(
                id   = bid,
                name = b['name'],
            )
