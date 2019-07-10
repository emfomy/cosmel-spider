#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy
from .items import CosmelItem

class BrandMetaItem(CosmelItem):
    id = scrapy.Field()
    name = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel_styleme.brand (id, name) VALUES (%s, %s)',
            (self['id'], self['name'],)
        )

class ProductMetaItem(CosmelItem):
    id = scrapy.Field()
    brand_id = scrapy.Field()
    name = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel_styleme.product (id, brand_id, name) VALUES (%s, %s, %s)',
            (self['id'], self['brand_id'], self['name'],)
        )

class ProductInfoItem(CosmelItem):
    id = scrapy.Field()
    descr = scrapy.Field()

    def submit(self, db):
        db.execute(
            '''
                UPDATE cosmel_styleme.product
                SET descr = %s
                WHERE id = %s
            ''',
            (self['descr'], self['id'],)
        )

class ProductCategoryItem(CosmelItem):
    id = scrapy.Field()
    type = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel_styleme.product_category (id, type) VALUES (%s, %s)',
            (self['id'], self['type'],)
        )

class ProductSpecItem(CosmelItem):
    id = scrapy.Field()
    type = scrapy.Field()
    spec = scrapy.Field()
    price = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel_styleme.product_spec (id, type, spec, price) VALUES (%s, %s, %s, %s)',
            (self['id'], self['type'], self['spec'], self['price'],)
        )

class ProductArticleItem(CosmelItem):
    id = scrapy.Field()
    article_id = scrapy.Field()
    type = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel_styleme.product_article (id, article_id, type) VALUES (%s, %s, %s)',
            (self['id'], self['article_id'], self['type'],)
        )

class ArticleMetaItem(CosmelItem):
    id = scrapy.Field()
    author = scrapy.Field()
    is_styleme = scrapy.Field()
    link = scrapy.Field()

    def __repr__(self):
        return repr({ k: v for k, v in self.items() if k != 'link' })

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel_styleme.product_article (id, author, is_styleme, link) VALUES (%s, %s, %s, %s)',
            (self['id'], self['author'], self['is_styleme'], self['link'],)
        )

class ArticleBodyItem(CosmelItem):
    id = scrapy.Field()
    title = scrapy.Field()
    category_id = scrapy.Field()
    subcategory_id = scrapy.Field()
    body = scrapy.Field()

    def __repr__(self):
        return repr({ k: v for k, v in self.items() if k != 'body' })

    def submit(self, db):
        db.execute(
            '''
                UPDATE cosmel_styleme.article
                SET title = %s,
                    category_id = %s,
                    subcategory_id = %s,
                    body = %s
                WHERE id = %s
            ''',
            (self['title'], self['category_id'], self['subcategory_id'], self['body'], self['id'],)
        )
