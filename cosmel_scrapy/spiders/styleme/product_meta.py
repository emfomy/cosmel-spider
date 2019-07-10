# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import *

from ..base import CosmelSpider
from cosmel_scrapy.db import Db
from cosmel_scrapy.items.styleme import *

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])
    allowed_domains = ['styleme.pixnet.net']

    def start_requests(self):
        db = Db(self)

        db.execute('SELECT id FROM cosmel_styleme.product ORDER BY id')
        self.skip_set = {pid for (pid,) in db.fetchall()}

        db.execute('SELECT id, name FROM cosmel_styleme.brand ORDER BY id')
        res = db.fetchall()

        del db

        total = len(res)
        for i, (bid, bname) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((bid, bname,))
            yield from self.do_product_meta(bid=bid,)

    def do_product_meta(self, *, bid):
        url = f'https://styleme.pixnet.net/api/searchbrands/{bid}/products/'
        yield scrapy.Request(
            url,
            callback=partial(self.parse_product_meta, bid=bid,),
            meta={ 'dont_redirect': True },
        )

    def parse_product_meta(self, res, *, bid):
        data = json.loads(res.body)
        if data['error']:
            logger().error(f'Unknown Brand #bid={bid}')
            return
        # assert not data['error']
        for p in data['products']:
            pid = int(p['id'])
            if pid not in self.skip_set:
                yield ProductMetaItem(
                    id       = pid,
                    brand_id = bid,
                    name     = p['name'],
                )
