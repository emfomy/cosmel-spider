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
        del db

        total = len(res)
        for i, (pid, pname,) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((pid, pname,))
            yield from self.do_product_article(pid=pid, type='impression')
            yield from self.do_product_article(pid=pid, type='teaching')

    def do_product_article(self, *, pid, type, page=1):
        url = f'https://styleme.pixnet.net/api/products/{pid}/articles?type={type}/'
        yield scrapy.Request(
            url,
            callback=partial(self.parse_product_article, pid=pid, type=type, page=page),
            meta={ 'dont_redirect': True },
        )

    def parse_product_article(self, res, *, pid, type, page):
        data = json.loads(res.body)
        assert not data['error']
        for a in data['articles']:
            aid = a['id']
            yield ArticleMetaItem(
                id         = aid,
                author     = a['user']['user_name'],
                is_styleme = bool(a['is_styleme']),
                link       = a['link'],
            )
            yield ProductArticleItem(
                id         = pid,
                article_id = a['id'],
                type       = type,
            )
        if page < data['total_page']:
            yield from self.do_product_article(pid=pid, type=type, page=page+1)
