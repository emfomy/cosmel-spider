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
    handle_httpstatus_list = [403, 404]

    item_db_name = 'cosmel_styleme'

    def start_requests(self):
        self.count_error = 0

        db = Db(self, self.item_db_name)
        db.execute('''
            SELECT id, author FROM article
            WHERE is_styleme=False
              AND (title IS NULL OR body IS NULL)
        ''')
        res = db.fetchall()
        del db

        total = len(res)
        logger().notice(f'Total {total} articles')

        for i, (aid, author,) in enumerate(res):
            logger().notice('-'*(i*71//total+1))
            logger().info((aid, author,))
            assert self.count_error < 100
            yield from self.do_article_body_pixnet(aid=aid, author=author)

    def do_article_body_pixnet(self, *, aid, author):
        url = f'https://emma.pixnet.cc/blog/articles/{aid}.json?user={author}&trim_user=1'
        yield scrapy.Request(
            url,
            callback=partial(self.parse_article_body_pixnet, aid=aid),
            meta={ 'dont_redirect': True },
        )

    def parse_article_body_pixnet(self, res, *, aid):
        try:
            data = json.loads(res.body.decode())
            if data['error']:
                ecode = int(data['code'])
                emsg = data['message']
                if ecode in [2101, 3900]:
                    logger().warning(f'aid#{aid} | [{ecode}] {emsg}')
                    a = {
                        'title': None,
                        'body': None,
                    }
                elif ecode == 1302:
                    raise UserWarning(f'aid#{aid} | [{ecode}] {emsg}')
                else:
                    logger().warning(f'aid#{aid} | [{ecode}] {emsg}')
                    raise UserWarning(f'aid#{aid} | [{ecode}] {emsg}')
            else:
                a = data['article']
        except Exception as e:
            logger().error(exceptstr(e))
            self.count_error += 1
            logger().error(f'Error count {self.count_error}')
            return

        yield ArticleBodyItem(
            id             = aid,
            title          = a['title'],
            category_id    = None,
            subcategory_id = None,
            body           = a['body'],
        )
