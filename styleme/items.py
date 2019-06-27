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
            'INSERT INTO brand.meta (id, name) VALUES (%s, %s) ' \
            'ON CONFLICT(id) DO NOTHING',
            # 'ON CONFLICT(id) DO UPDATE SET name=EXCLUDED.name',
            (self['id'], self['name'],)
        )

class ProductMetaItem(StylemeItem):
    id = scrapy.Field()
    name = scrapy.Field()
    brand_id = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT INTO product.meta (id, name, brand_id) VALUES (%s, %s, %s) ' \
            'ON CONFLICT(id) DO NOTHING',
            # 'ON CONFLICT(id) DO UPDATE SET name=EXCLUDED.name, brand_id=EXCLUDED.brand_id',
            (self['id'], self['name'], self['brand_id'],)
        )

class ProductInfoItem(StylemeItem):
    id = scrapy.Field()
    desc = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT INTO product.info (id, "desc") VALUES (%s, %s) ' \
            'ON CONFLICT(id) DO NOTHING',
            # 'ON CONFLICT(id) DO UPDATE SET desc=EXCLUDED.desc',
            (self['id'], self['desc'],)
        )

class ProductQualityItem(StylemeItem):
    id = scrapy.Field()
    type = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT INTO product.quality (id, type) VALUES (%s, %s) ' \
            'ON CONFLICT(id, type) DO NOTHING',
            (self['id'], self['type'],)
        )

class ProductSpecItem(StylemeItem):
    id = scrapy.Field()
    type = scrapy.Field()
    spec = scrapy.Field()
    price = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT INTO product.spec (id, type, spec, price) VALUES (%s, %s, %s, %s) ' \
            'ON CONFLICT(id, type, spec) DO NOTHING',
            (self['id'], self['type'], self['spec'], self['price'],)
        )

class ProductArticleItem(StylemeItem):
    id = scrapy.Field()
    article_id = scrapy.Field()
    type = scrapy.Field()

    def submit(self, db):
        db.execute(
            'INSERT INTO product.article (id, article_id, type) VALUES (%s, %s, %s) ' \
            'ON CONFLICT(id, article_id) DO NOTHING',
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
            'INSERT INTO article.meta (id, author, is_styleme, link) VALUES (%s, %s, %s, %s) ' \
            # 'ON CONFLICT(id) DO NOTHING',
            'ON CONFLICT(id) DO UPDATE SET author=EXCLUDED.author, is_styleme=EXCLUDED.is_styleme, link=EXCLUDED.link',
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
            'INSERT INTO article.info (id, title, category_id, subcategory_id) VALUES (%s, %s, %s, %s) ' \
            'ON CONFLICT(id) DO NOTHING',
            (self['id'], self['title'], self['category_id'], self['subcategory_id'],)
        )
        db.execute(
            'INSERT INTO article.body (id, body) VALUES (%s, %s) ' \
            'ON CONFLICT(id) DO NOTHING',
            (self['id'], self['body'],)
        )
