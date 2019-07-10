# -*- coding: utf-8 -*-
import json
import re
from functools import partial

import scrapy
import bs4

from utils.logging import *

from ..base import CosmelSpider
from cosmel_scrapy.db import Db
from cosmel_scrapy.items.cosmel import *

from cosmel.util.text import purge_string

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])

    def start_requests(self):
        db = Db(self)

        total = db.execute('''
            SELECT id, orig_title, html_body
            FROM cosmel.article
            WHERE id NOT IN (SELECT article_id FROM cosmel.article_content)
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
                ArticleSentenceItem(
                    aid = aid,
                    callback = partial(self.format_body, aid=aid, title=title, body=body, msg='-'*(i*71//total+1)),
                )
            )

            # if i >= 0: break

        del db

        yield from self.do_items(*items)


    regexes0 = \
        [(re.compile('[^\S ]'), ' ',)] + \
        [(re.compile(rf'<{tag}>'), f'\n<{tag}>',)
            for tag in ['blockquote', 'center', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']] + \
        [(re.compile(rf'</{tag}>'), f'</{tag}>\n',)
            for tag in ['blockquote', 'center', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']] + \
        [(re.compile(rf'<{tag}/>'), f'<{tag}/>\n',)
            for tag in ['br', 'hr']]

    regexes1 = [ \
            (re.compile(r' +'), ' '), \
            (re.compile(r' ($|\n)'), '\n'), \
            (re.compile(r'(\A|\n) '), '\n'), \
            (re.compile(r'\n+'), '\n'), \
    ]

    def format_body(self, *, aid, title, body, msg):
        logger().notice(msg)
        logger().info((aid, title,))

        for regex in self.regexes0:
            body = regex[0].sub(regex[1], body)

        soup = bs4.BeautifulSoup(body, 'lxml')
        for s in soup(['script', 'style']): s.decompose()

        body_text = soup.text.strip()+'\n'
        for regex in self.regexes1:
            body_text = regex[0].sub(regex[1], body_text)

        title_lines = purge_string(title, is_sentence=True).split('\n')
        body_lines = purge_string(body_text, is_sentence=True).split('\n')

        return title_lines + body_lines, len(title_lines)
