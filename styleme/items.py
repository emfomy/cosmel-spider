# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class StylemeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BrandMetaItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()

class ProductMetaItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()

class ProductArticleItem(scrapy.Item):
    id = scrapy.Field()
    article = scrapy.Field()
    type = scrapy.Field()

class ArticleMetaItem(scrapy.Item):
    id = scrapy.Field()
    author = scrapy.Field()
    is_styleme = scrapy.Field()

class ArticleBodyItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    category_id = scrapy.Field()
    subcategory_id = scrapy.Field()
    body = scrapy.Field()

    def __repr__(self):
        return repr({ k: v for k, v in self.items() if k != 'body' })
