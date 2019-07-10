# -*- coding: utf-8 -*-
from functools import partial

import scrapy

from utils.logging import *

from ..base import CosmelSpider
from cosmel_scrapy.db import Db
from cosmel_scrapy.items.cosmel import *

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])

    def start_requests(self):
        db = Db(self)
        db.execute('''
            SELECT id, link, title, subcategory_id
            FROM cosmel_styleme.article
            WHERE id NOT IN (SELECT id FROM cosmel.article)
              AND title IS NOT NULL
        ''')
        res = db.fetchall()

        del db

        total = len(res)
        logger().notice(f'Total {total} articles')

        # Items
        items = []
        for i, (aid, link, title, csid,) in enumerate(res):
            if not title: continue
            # logger().notice('-'*(i*71//total+1))
            # logger().info((aid, title,))
            items.append(
                ArticleMetaItem(
                    id             = aid,
                    link           = link,
                    orig_title     = title,
                    subcategory_id = csid,
                )
            )

        yield from self.do_items(*items)
