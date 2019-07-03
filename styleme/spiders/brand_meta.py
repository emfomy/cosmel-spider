# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import *

from ..db import Db
from ..items import *

class Spider(scrapy.Spider):
    name = __name__.split('.')[-1]
    allowed_domains = ['styleme.pixnet.net']

    def start_requests(self):
        db = Db(self)

        db.execute('SELECT id FROM brand ORDER BY id')
        self.skip_set = {bid for (bid,) in db.fetchall()}

        del db

        yield from self.do_brand_meta()
        yield from self.do_items(
            BrandMetaItem(
                id   = 10000,
                name = 'SHISEIDO 資生堂',
            ),
        )

    def do_brand_meta(self):
        url = 'https://styleme.pixnet.net/api/searchbrands'
        yield scrapy.Request(
            url,
            callback=self.parse_brand_meta,
            meta={ 'dont_redirect': True },
        )

    def parse_brand_meta(self, res):
        data = json.loads(res.body)
        assert not data['error']
        for b in data['brands']:
            bid = int(b['id'])
            assert bid < 10000
            if bid not in self.skip_set:
                yield BrandMetaItem(
                    id   = bid,
                    name = b['name'],
                )

    def do_items(self, *items):
        yield scrapy.Request(
            'https://styleme.pixnet.net',
            callback=partial(self.parse_items, items=items),
        )

    def parse_items(self, _, *, items):
        return iter(items)
