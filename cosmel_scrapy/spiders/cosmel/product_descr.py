# -*- coding: utf-8 -*-
from functools import partial

import scrapy

from utils.logging import *

from ..base import CosmelSpider
from cosmel_scrapy.db import Db
from cosmel_scrapy.items.cosmel import *

from cosmel.util.text import purge_string

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])

    def start_requests(self):
        db = Db(self)
        db.execute('''
            SELECT id, orig_descr
            FROM cosmel.product
            WHERE id NOT IN (SELECT product_id FROM cosmel.product_descr)
        ''')
        res = db.fetchall()
        del db

        # Items
        items = []
        for (pid, pdescr,) in res:
            items.append(
                ProductSentenceItem(
                    id    = pid,
                    lines = purge_string(pdescr, is_sentence=True).split('\n'),
                )
            )

        yield from self.do_items(*items)
