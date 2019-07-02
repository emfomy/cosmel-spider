# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import *

from ..db import Db
from ..items import *

class Spider(scrapy.Spider):
    name = __name__.split('.')[-1]
    allowed_domains = ['pixnet.net']
    handle_httpstatus_list = [406, 500]

    def start_requests(self):
        self.count_error = 0

        db = Db(self)
        db.execute('SELECT id, author, link FROM article WHERE is_styleme=False')
        res = db.fetchall()

        db.execute('SELECT id FROM article_info')
        info_id = set(v[0] for v in db.fetchall())

        db.execute('SELECT id FROM article_body')
        body_id = set(v[0] for v in db.fetchall())

        res = [line for line in res if (line[0] not in info_id or line[0] not in body_id)]
        del db

        total = len(res)
        logger().notice(f'Total {total} articles')

        for i, (aid, author, link,) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((aid, author,))
            assert self.count_error < 100
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
        if res.status in self.handle_httpstatus_list:
            self.count_error += 1
            logger().error(f'Error count {self.count_error}')
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
