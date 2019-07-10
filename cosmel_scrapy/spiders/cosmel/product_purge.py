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
            SELECT id, orig_name
            FROM cosmel.product
            WHERE name IS NULL
            ORDER BY id
        ''')
        res = db.fetchall()
        del db

        # Items
        items = []
        for (pid, pname,) in res:
            items.append(
                ProductPurgeItem(
                    id   = pid,
                    name = purge_string(pname, is_sentence=False),
                )
            )

        yield from self.do_items(*items)
