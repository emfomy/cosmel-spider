# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import logger

from ..db import Db
from ..items import *

class Spider(scrapy.Spider):
    name = __name__.split('.')[-1]
    allowed_domains = ['pixnet.net']
    handle_httpstatus_list = [406]

    def start_requests(self):
        self.count_406 = 0

        db = Db(self)
        db.execute('SELECT id, author, link FROM article.meta WHERE is_styleme=False')
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

        for i, (aid, author, link,) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((aid, author,))
            assert self.count_406 < 100
            yield from self.do_article_body_pixnet(aid=aid, link=link)

    def do_article_body_pixnet(self, *, aid, link):
        # url = f'http://{author}.pixnet.net/blog/post/{aid}'
        url = link
        yield scrapy.Request(
            url,
            callback=partial(self.parse_product_body_pixnet, aid=aid),
            # meta={ 'dont_redirect': True },
        )

    def parse_product_body_pixnet(self, res, *, aid):
        if res.status == 406:
            self.count_406 += 1
            logger().error(f'406 count {self.count_406}')
            return

        title = res.xpath(f'//li[@id="article-{aid}"]/h2/a/node()').getall()
        title = ''.join(title).strip()

        body = res.xpath('//div[@id="article-content-inner"]/node()').getall()
        body = ''.join(body).strip()

        yield ArticleBodyItem(
            id             = aid,
            title          = title,
            category_id    = None,
            subcategory_id = None,
            body           = body,
        )
