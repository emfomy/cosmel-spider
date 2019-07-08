#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy
from .items import CosmelItem

class BrandMetaItem(CosmelItem):
    id = scrapy.Field()
    name = scrapy.Field()

    def submit(self, db):
        try:
            db.execute(
                'INSERT IGNORE INTO cosmel.brand (id, name) VALUES (%s, %s)',
                (self['id'], self['name'],)
            )
        except Warning as w:
            if w.args[0] == 1062: # Duplicate entry
                db.execute(
                    '''
                        UPDATE cosmel.brand
                        SET name = %s
                        WHERE id = %s
                    ''',
                    (self['name'], self['id'],)
                )
            else:
                raise(w)

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

class ProductMetaItem(CosmelItem):
    id = scrapy.Field()
    name = scrapy.Field()
    brand_id = scrapy.Field()

    def submit(self, db):
        try:
            db.execute(
                'INSERT IGNORE INTO cosmel.product (id, name, brand_id) VALUES (%s, %s, %s)',
                (self['id'], self['name'], self['brand_id'],)
            )
        except Warning as w:
            if w.args[0] == 1062: # Duplicate entry
                db.execute(
                    '''
                        UPDATE cosmel.product
                        SET name = %s
                        WHERE id = %s
                    ''',
                    (self['name'], self['id'],)
                )
            else:
                raise(w)

class ProductStylemeItem(CosmelItem):
    styleme_id = scrapy.Field()
    cosmel_id= scrapy.Field()

    def submit(self, db):
        db.execute(
            '''
                UPDATE cosmel_styleme.product
                SET cosmel_id = %s
                WHERE id = %s
            ''',
            (self['cosmel_id'], self['styleme_id'],)
        )
