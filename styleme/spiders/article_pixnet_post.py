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

    def start_requests(self):

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
            yield from self.do_article_body_pixnet(aid=aid, author=author)

    def do_article_body_pixnet(self, *, aid, author):
        url = f'http://{author}.pixnet.net/blog/post/{aid}'
        yield scrapy.Request(
            url,
            callback=partial(self.parse_product_body_pixnet, aid=aid),
            meta={ 'dont_redirect': True },
        )

    def parse_product_body_pixnet(self, res, *, aid):
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
