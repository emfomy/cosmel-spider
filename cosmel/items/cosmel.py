#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy
from .items import CosmelItem

class BrandMetaItem(CosmelItem):
    id = scrapy.Field()
    name = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO brand (id, name) VALUES (%s, %s)',
            (self['id'], self['name'],)
        )
