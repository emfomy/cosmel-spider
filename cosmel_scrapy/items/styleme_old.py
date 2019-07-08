#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy
from .items import CosmelItem

class ProductMetaItem(CosmelItem):
    id = scrapy.Field()
    brand_name = scrapy.Field()
    name = scrapy.Field()
    descr = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel_styleme_old.product (id, brand_name, name, descr) VALUES (%s, %s, %s, %s)',
            (self['id'], self['brand_name'], self['name'], self['descr'],)
        )
