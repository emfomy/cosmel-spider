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

        db.execute('SELECT id FROM product ORDER BY id')
        self.skip_set = {pid for (pid,) in db.fetchall()}

        db.execute('SELECT id, name FROM brand ORDER BY id')
        res = db.fetchall()
        del db

        total = len(res)
        for i, (bid, bname,) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((bid, bname,))
            yield from self.do_product_meta(bid=bid)

    def do_product_meta(self, *, bid):
        url = f'https://styleme.pixnet.net/api/searchbrands/{bid}/products/'
        yield scrapy.Request(
            url,
            callback=partial(self.parse_product_meta, bid=bid),
            meta={ 'dont_redirect': True },
        )

    def parse_product_meta(self, res, *, bid):
        data = json.loads(res.body)
        assert not data['error']
        for p in data['products']:
            if int(p['id']) not in self.skip_set:
                yield ProductMetaItem(
                    id       = p['id'],
                    name     = p['name'],
                    brand_id = bid,
                )
