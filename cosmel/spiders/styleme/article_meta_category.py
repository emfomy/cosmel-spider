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

    item_db_name = 'cosmel_styleme'

    def start_requests(self):
        db = Db(self, self.item_db_name)

        db.execute('SELECT id FROM article ORDER BY id')
        self.skip_set = {aid for (aid,) in db.fetchall()}

        db.execute('SELECT category_id, id, name FROM article_category_sub ORDER BY category_id, id')
        res = db.fetchall()

        res = [line for line in res if (line[0] in [4, 7, 10, 19])]
        del db

        total = len(res)
        for i, (cid, csid, csname) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((cid, csid, csname,))
            yield from self.do_article_meta_category(cid=cid, csid=csid)

    def do_article_meta_category(self, *, cid, csid, page=1):
        url = f'https://styleme.pixnet.net/api/articles/categorylist/{cid}?subcategory_id={csid}&page={page}'
        yield scrapy.Request(
            url,
            callback=partial(self.parse_article_meta_category, cid=cid, csid=csid, page=page),
            meta={ 'dont_redirect': True },
        )

    def parse_article_meta_category(self, res, *, cid, csid, page):
        data = json.loads(res.body)
        assert not data['error']
        for a in data['articles']:
            if a['user'] is None: continue
            aid = int(a['id'])
            if aid not in self.skip_set:
                yield ArticleMetaItem(
                    id         = aid,
                    author     = a['user']['user_name'],
                    is_styleme = bool(a['is_styleme']),
                    link       = a['link'],
                )

        if page < data['total_page']:
            yield from self.do_article_meta_category(cid=cid, csid=csid, page=page+1)
