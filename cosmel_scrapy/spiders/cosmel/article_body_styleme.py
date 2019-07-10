# -*- coding: utf-8 -*-
from functools import partial

import scrapy
import bs4

from utils.logging import *

from ..base import CosmelSpider
from cosmel_scrapy.db import Db
from cosmel_scrapy.items.cosmel import *

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])

    def start_requests(self):
        db = Db(self)
        total = db.execute('''
            SELECT cosmel.id, cosmel.orig_title, styleme.body
            FROM cosmel.article AS cosmel
            INNER JOIN cosmel_styleme.article AS styleme ON cosmel.id = styleme.id
            WHERE cosmel.html_body IS NULL
        ''')

        logger().notice(f'Total {total} articles')

        # Items
        items = []
        i = -1
        while True:
            i += 1
            line = db.fetchone()
            if line is None: break

            (aid, title, body,) = line
            items.append(
                ArticleBodyItem(
                    id = aid,
                    callback = partial(self.format_body, aid=aid, title=title, body=body, msg='-'*(i*71//total+1)),
                )
            )

            # if i >= 0: break

        del db

        yield from self.do_items(*items)

    def format_body(self, *, aid, title, body, msg):
        logger().notice(msg)
        logger().info((aid, title,))

        soup = bs4.BeautifulSoup(body, 'lxml')

        try: soup.html.unwrap()
        except: pass

        try: soup.body.unwrap()
        except: pass

        comments = soup.find_all(string=lambda text: isinstance(text, bs4.Comment))
        for comment in comments: comment.extract()

        html_body = ''.join(map(str.strip, soup.prettify().split('\n')))

        return html_body
