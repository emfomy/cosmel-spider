# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class StylemeItem(scrapy.Item):

    def submit(self, db):
        raise NotImplementedError

class BrandMetaItem(StylemeItem):
    id = scrapy.Field()
    name = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO brand (id, name) VALUES (%s, %s)',
            (self['id'], self['name'],)
        )

class ProductMetaItem(StylemeItem):
    id = scrapy.Field()
    name = scrapy.Field()
    brand_id = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO product (id, name, brand_id) VALUES (%s, %s, %s)',
            (self['id'], self['name'], self['brand_id'],)
        )

class ProductInfoItem(StylemeItem):
    id = scrapy.Field()
    description = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO product_info (id, description) VALUES (%s, %s)',
            (self['id'], self['description'],)
        )

class ProductQualityItem(StylemeItem):
    id = scrapy.Field()
    type = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO product_quality (id, type) VALUES (%s, %s)',
            (self['id'], self['type'],)
        )

class ProductSpecItem(StylemeItem):
    id = scrapy.Field()
    type = scrapy.Field()
    spec = scrapy.Field()
    price = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO product_spec (id, type, spec, price) VALUES (%s, %s, %s, %s)',
            (self['id'], self['type'], self['spec'], self['price'],)
        )

class ProductArticleItem(StylemeItem):
    id = scrapy.Field()
    article_id = scrapy.Field()
    type = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO product_article (id, article_id, type) VALUES (%s, %s, %s)',
            (self['id'], self['article_id'], self['type'],)
        )

class ArticleMetaItem(StylemeItem):
    id = scrapy.Field()
    author = scrapy.Field()
    is_styleme = scrapy.Field()
    link = scrapy.Field()

    def __repr__(self):
        return repr({ k: v for k, v in self.items() if k != 'link' })

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO article (id, author, is_styleme, link) VALUES (%s, %s, %s, %s)',
            (self['id'], self['author'], self['is_styleme'], self['link'],)
        )

class ArticleBodyItem(StylemeItem):
    id = scrapy.Field()
    title = scrapy.Field()
    category_id = scrapy.Field()
    subcategory_id = scrapy.Field()
    body = scrapy.Field()

    def __repr__(self):
        return repr({ k: v for k, v in self.items() if k != 'body' })

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO article_info (id, title, category_id, subcategory_id) VALUES (%s, %s, %s, %s)',
            (self['id'], self['title'], self['category_id'], self['subcategory_id'],)
        )
        db.execute(
            'INSERT IGNORE INTO article_body (id, body) VALUES (%s, %s)',
            (self['id'], self['body'],)
        )
