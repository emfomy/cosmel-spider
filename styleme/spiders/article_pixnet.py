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
    handle_httpstatus_list = [403]

    def start_requests(self):
        self.count_403 = 0

        db = Db(self)
        db.execute('SELECT id, author FROM article.meta WHERE is_styleme=False')
        res = db.fetchall()

        db.execute('SELECT id FROM article.info')
        info_id = set(v[0] for v in db.fetchall())

        db.execute('SELECT id FROM article.body')
        body_id = set(v[0] for v in db.fetchall())
        del db

        res = [line for line in res if line[0] not in info_id or line[0] not in body_id]
        total = len(res)
        logger().notice(f'Total {total} articles')

        for i, (aid, author,) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((aid, author,))
            assert self.count_403 < 100
            yield from self.do_article_body_pixnet(aid=aid, author=author)

    def do_article_body_pixnet(self, *, aid, author):
        url = f'https://emma.pixnet.cc/blog/articles/{aid}.json?user={author}&trim_user=1'
        yield scrapy.Request(
            url,
            callback=self.parse_product_body_pixnet,
            meta={ 'dont_redirect': True },
        )

    def parse_product_body_pixnet(self, res):
        if res.status == 403:
            self.count_403 += 1
            logger().error(f'403 count {self.count_403}')
            return

        data = json.loads(res.body.decode())
        assert not data['error']
        a = data['article']
        yield ArticleBodyItem(
            id             = a['id'],
            title          = a['title'],
            category_id    = None,
            subcategory_id = None,
            body           = a['body'],
        )
