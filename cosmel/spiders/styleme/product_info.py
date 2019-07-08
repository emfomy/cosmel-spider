# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import *

from ..base import CosmelSpider
from cosmel.db import Db
from cosmel.items.styleme import *

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])
    allowed_domains = ['styleme.pixnet.net']

    def start_requests(self):
        db = Db(self)
        db.execute('''
            SELECT id, name FROM cosmel_styleme.product
            WHERE description IS NULL
               OR id NOT IN (SELECT id FROM cosmel_styleme.product_spec)
               OR id NOT IN (SELECT id FROM cosmel_styleme.product_quality)
            ORDER BY id
        ''')
        res = db.fetchall()
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
            yield from self.retry(res)
            return

        p = data['product']
        yield ProductInfoItem(
            id          = p['id'],
            description = p['desc'],
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
                id    = p['id'],
                type  = spec['spec_name'],
                spec  = spec['spec'],
                price = price,
            )
