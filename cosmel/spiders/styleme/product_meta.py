# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import *

from cosmel.db import Db
from cosmel.items.styleme import *

class Spider(scrapy.Spider):
    name = '_'.join(__name__.split('.')[-2:])
    allowed_domains = ['styleme.pixnet.net']

    item_db_name = 'cosmel_styleme'

    def start_requests(self):
        db = Db(self, self.item_db_name)

        db.execute('SELECT id FROM product ORDER BY id')
        self.skip_set = {pid for (pid,) in db.fetchall()}

        db.execute('SELECT id, name, id FROM brand ORDER BY id')
        res = db.fetchall()

        del db

        total = len(res)
        for i, (bid, bname, bmerge) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((bid, bname,))
            yield from self.do_product_meta(bid=bid, bmerge=bmerge,)

    def do_product_meta(self, *, bid, bmerge):
        url = f'https://styleme.pixnet.net/api/searchbrands/{bid}/products/'
        yield scrapy.Request(
            url,
            callback=partial(self.parse_product_meta, bid=bid, bmerge=bmerge,),
            meta={ 'dont_redirect': True },
        )

    def parse_product_meta(self, res, *, bid, bmerge):
        data = json.loads(res.body)
        if data['error']:
            logger().error(f'#bid={bid} Error?')
            return
        # assert not data['error']
        for p in data['products']:
            pid = int(p['id'])
            if (bid != bmerge) or (pid not in self.skip_set):
                yield ProductMetaItem(
                    id       = pid,
                    name     = p['name'],
                    brand_id = bmerge,
                )
