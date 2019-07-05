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

    def start_requests(self):
        db = Db(self)

        db.execute('SELECT id FROM cosmel_styleme.article ORDER BY id')
        self.skip_set_article_meta = {aid for (aid,) in db.fetchall()}

        db.execute('SELECT id, article_id FROM cosmel_styleme.product_article ORDER BY id')
        self.skip_set_product_article = {(pid, aid) for (pid, aid,) in db.fetchall()}

        db.execute('SELECT id, name FROM cosmel_styleme.product ORDER BY id')
        res = db.fetchall()

        del db

        total = len(res)
        for i, (pid, pname,) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((pid, pname,))
            yield from self.do_article_meta_category(pid=pid, type='impression')
            yield from self.do_article_meta_category(pid=pid, type='teaching')

    def do_article_meta_category(self, *, pid, type, page=1):
        url = f'https://styleme.pixnet.net/api/products/{pid}/articles?type={type}&page={page}'
        yield scrapy.Request(
            url,
            callback=partial(self.parse_article_meta_category, pid=pid, type=type, page=page),
            meta={ 'dont_redirect': True },
        )

    def parse_article_meta_category(self, res, *, pid, type, page):
        data = json.loads(res.body)
        assert not data['error']
        for a in data['articles']:
            if a['user'] is None: continue
            aid = int(a['id'])

            if aid not in self.skip_set_article_meta:
                yield ArticleMetaItem(
                    id         = aid,
                    author     = a['user']['user_name'],
                    is_styleme = bool(a['is_styleme']),
                    link       = a['link'],
                )

            if (pid, aid,) not in self.skip_set_product_article:
                yield ProductArticleItem(
                    id         = pid,
                    article_id = aid,
                    type       = type,
                )

        if page < data['total_page']:
            yield from self.do_article_meta_category(pid=pid, type=type, page=page+1)
