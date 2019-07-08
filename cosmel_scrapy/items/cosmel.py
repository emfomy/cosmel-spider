#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy
from .items import CosmelItem

class BrandMetaItem(CosmelItem):
    id = scrapy.Field()
    orig_name = scrapy.Field()

    def submit(self, db):
        try:
            db.execute(
                'INSERT IGNORE INTO cosmel.brand (id, orig_name) VALUES (%s, %s)',
                (self['id'], self['orig_name'],)
            )
        except Warning as w:
            if w.args[0] == 1062: # Duplicate entry
                db.execute(
                    '''
                        UPDATE cosmel.brand
                        SET orig_name = %s
                        WHERE id = %s
                    ''',
                    (self['orig_name'], self['id'],)
                )
            else:
                raise w

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

class BrandMetaStylemeOldItem(CosmelItem):
    id = scrapy.Field()
    name = scrapy.Field()

    def submit(self, db):
        db.execute(
            '''
                UPDATE cosmel_styleme_old.product
                SET brand_id = %s
                WHERE brand_name = %s
            ''',
            (self['id'], self['name'],)
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
    brand_id = scrapy.Field()
    orig_name = scrapy.Field()
    orig_descr = scrapy.Field()

    def submit(self, db):
        try:
            db.execute(
                'INSERT IGNORE INTO cosmel.product (id, brand_id, orig_name, orig_descr) VALUES (%s, %s, %s, %s)',
                (self['id'], self['brand_id'], self['orig_name'], self['orig_descr'],)
            )
        except Warning as w:
            if w.args[0] == 1062: # Duplicate entry
                db.execute(
                    '''
                        UPDATE cosmel.product
                        SET orig_name = %s, orig_descr = %s
                        WHERE id = %s AND brand_id = %s
                    ''',
                    (self['orig_name'], self['orig_descr'], self['id'], self['brand_id'],)
                )
            else:
                raise w

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

class ProductStylemeOldItem(CosmelItem):
    styleme_id = scrapy.Field()
    cosmel_id= scrapy.Field()

    def submit(self, db):
        db.execute(
            '''
                UPDATE cosmel_styleme_old.product
                SET cosmel_id = %s
                WHERE id = %s
            ''',
            (self['cosmel_id'], self['styleme_id'],)
        )

class ProductPurgeItem(CosmelItem):
    id = scrapy.Field()
    name = scrapy.Field()

    def submit(self, db):
        db.execute(
            '''
                UPDATE cosmel.product
                SET name = %s
                WHERE id = %s
            ''',
            (self['name'], self['id'],)
        )

class ProductArticleItem(CosmelItem):
    id = scrapy.Field()
    article_id = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel_styleme.product_article (id, article_id) VALUES (%s, %s, %s)',
            (self['id'], self['article_id'],)
        )
