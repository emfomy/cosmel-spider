# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import logger

from ..db import Db
from ..items import *

class Spider(scrapy.Spider):
    name = __name__.split('.')[-1]
    allowed_domains = ['styleme.pixnet.net']

    def start_requests(self):
        db = Db(self)
        db.execute('SELECT id, name FROM product.meta ORDER BY id')
        res = db.fetchall()

        skip_sets = []

        db.execute('SELECT id FROM product.info')
        skip_sets.append(set(v[0] for v in db.fetchall()))

        db.execute('SELECT id FROM product.spec')
        skip_sets.append(set(v[0] for v in db.fetchall()))

        db.execute('SELECT id FROM product.quality')
        skip_sets.append(set(v[0] for v in db.fetchall()))

        res = [line for line in res if line[0] not in set.intersection(*skip_sets)]
        del db

        total = len(res)
        logger().notice(f'Total {total} products')

        total = len(res)
        for i, (pid, pname,) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((pid, pname,))
            yield from self.do_product_info(pid=pid)

    def do_product_info(self, *, pid, page=1):
        url = f'https://styleme.pixnet.net/api/products/{pid}'
        yield scrapy.Request(
            url,
            callback=partial(self.parse_product_info, pid=pid, page=page),
            meta={ 'dont_redirect': True },
        )

    def parse_product_info(self, res, *, pid, page):
        data = json.loads(res.body)
        if data['error']:
            logger().warning('ERROR!')
            return []

        p = data['product']
        yield ProductInfoItem(
            id   = p['id'],
            desc = p['desc'],
        )

        for quality in p['qualities']:
            yield ProductQualityItem(
                id   = p['id'],
                type = quality,
            )

        for spec in p['spec']:
            price = str(spec['price'])
            if not price.isnumeric() or price == '0': continue
            yield ProductSpecItem(
                id   = p['id'],
                type = spec['spec_name'],
                spec = spec['spec'],
                price = price,
            )
