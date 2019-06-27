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
        db.execute('SELECT id, author FROM article.meta WHERE is_styleme=True')
        res = db.fetchall()

        skip_sets = []

        db.execute('SELECT id FROM article.info')
        skip_sets.append(set(v[0] for v in db.fetchall()))

        db.execute('SELECT id FROM article.body')
        skip_sets.append(set(v[0] for v in db.fetchall()))

        res = [line for line in res if line[0] not in set.intersection(*skip_sets)]
        del db

        total = len(res)
        logger().notice(f'Total {total} articles')

        for i, (aid, author,) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((aid, author,))
            yield from self.do_article_body_styleme(aid=aid, author=author)

    def do_article_body_styleme(self, *, aid, author):
        url = f'https://styleme.pixnet.net/api/articles/{aid}'
        yield scrapy.Request(
            url,
            callback=self.parse_product_body_styleme,
            meta={ 'dont_redirect': True },
        )

    def parse_product_body_styleme(self, res):
        data = json.loads(res.body)
        assert not data['error']
        a = data['article']
        yield ArticleBodyItem(
            id             = a['id'],
            title          = a['title'],
            category_id    = a['category_id'],
            subcategory_id = a['subcategory_id'],
            body           = a['body'],
        )
