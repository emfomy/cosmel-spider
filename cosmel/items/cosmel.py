#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy
from .items import CosmelItem

class BrandMetaItem(CosmelItem):
    id = scrapy.Field()
    name = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel.brand (id, name) VALUES (%s, %s)',
            (self['id'], self['name'],)
        )

class BrandStylemeItem(CosmelItem):
    styleme_id = scrapy.Field()
    cosmel_id= scrapy.Field()

    def submit(self, db):
        db.execute(
            '''
                UPDATE cosmel_styleme.brand
                SET cosmel_id = %s
                WHERE id = %s
            ''',
            (self['cosmel_id'], self['styleme_id'],)
        )

class BrandAliasItem(CosmelItem):
    id = scrapy.Field()
    alias = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel.brand_alias (id, alias) VALUES (%s, %s)',
            (self['id'], self['alias'],)
        )
