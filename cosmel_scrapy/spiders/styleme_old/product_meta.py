# -*- coding: utf-8 -*-
import csv
import json
from functools import partial

import scrapy

from utils.logging import *

from ..base import CosmelSpider
from cosmel_scrapy.db import Db
from cosmel_scrapy.items.styleme_old import *

from cosmel.util.text import check_contain_chinese
from cosmel.util.text import check_contain_chinese

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])
    allowed_domains = ['styleme.pixnet.net']

    def start_requests(self):
        items = []

        with open('./data/styleme.csv') as fin:
            for row in csv.DictReader(fin):
                if not row['編號'] or not row['中文品名'] or \
                        '測試' in row['品牌'] or '測試' in row['中文品名'] or \
                        'test' in row['品牌'].lower() or 'test' in row['中文品名'].lower() or \
                        not check_contain_chinese(row['中文品名']):
                    # logger().spam(f'Skip product {row["編號"]}')
                    continue
                row = RawData(row)
                # logger().info(row)

                items.append(
                    ProductMetaItem(
                        id         = row.pid,
                        brand_name = row.bname,
                        name       = row.pname,
                        descr      = row.descr,
                    )
                )

        yield from self.do_items(*items)

class RawData:

    def __init__(self, row):
        self.pid   = int(row['編號'])
        self.bname = row['品牌']
        self.pname = row['中文品名']
        self.descr = row['中文簡介']

        if not self.bname: self.bname = None
        if not self.descr: self.descr = None

        if self.bname == '80': self.bname = '080'

        self.raw = row

    def __str__(self):
        return f'{self.pid} {self.bname} {self.pname}'
