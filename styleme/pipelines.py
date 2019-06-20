# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import getpass
import json
import os

import psycopg2
import scrapy
import sshtunnel

from utils.logging import *

from .db import Db
from .items import *

class StylemePipeline:

    count = 0

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        pipeline = cls(*args, **kwargs)
        # crawler.signals.connect(pipeline.open_spider, signal=scrapy.signals.spider_opened)
        crawler.signals.connect(pipeline.close_spider, signal=scrapy.signals.spider_closed)
        return pipeline

    def open_spider(self, spider):
        logger().success('Starting Pipeline ...')
        self.db = Db(spider)

    def close_spider(self, spider):
        logger().success('Closing Pipeline ...')
        if self.db is not None:
            try:
                self.db.commit()
            except Exception as e:
                logger().error(exceptstr(e))
            finally:
                del self.db
                self.db = None

    def process_item(self, item, spider):
        # logger().verbose(item)

        if isinstance(item, BrandMetaItem):
            self.db.execute(
                'INSERT INTO brand.meta (id, name) VALUES (%s, %s) ' \
                'ON CONFLICT(id) DO NOTHING',
                # 'ON CONFLICT(id) DO UPDATE SET name=EXCLUDED.name',
                (item['id'], item['name'])
            )
        elif isinstance(item, ProductMetaItem):
            self.db.execute(
                'INSERT INTO product.meta (id, name, brand_id) VALUES (%s, %s, %s) ' \
                'ON CONFLICT(id) DO NOTHING',
                # 'ON CONFLICT(id) DO UPDATE SET name=EXCLUDED.name, brand_id=EXCLUDED.brand_id',
                (item['id'], item['name'], item['brand_id'])
            )
        elif isinstance(item, ProductArticleItem):
            self.db.execute(
                'INSERT INTO product.article (id, article_id, type) VALUES (%s, %s, %s) ' \
                'ON CONFLICT(id, article_id) DO NOTHING',
                (item['id'], item['article_id'], item['type'])
            )
        elif isinstance(item, ArticleMetaItem):
            self.db.execute(
                'INSERT INTO article.meta (id, author, is_styleme) VALUES (%s, %s, %s) ' \
                'ON CONFLICT(id) DO NOTHING',
                # 'ON CONFLICT(id) DO UPDATE SET author=EXCLUDED.author, is_styleme=EXCLUDED.is_styleme',
                (item['id'], item['author'], item['is_styleme'])
            )
        elif isinstance(item, ArticleBodyItem):
            self.db.execute(
                'INSERT INTO article.info (id, title, category_id, subcategory_id) VALUES (%s, %s, %s, %s) ' \
                'ON CONFLICT(id) DO NOTHING',
                (item['id'], item['title'], item['category_id'], item['subcategory_id'])
            )
            self.db.execute(
                'INSERT INTO article.body (id, body) VALUES (%s, %s) ' \
                'ON CONFLICT(id) DO NOTHING',
                (item['id'], item['body'])
            )
        else:
            logger().warning(f'Unknown item {item.__class__}')

        self.count += 1
        if self.count >= 1000:
            self.count = 0
            self.db.commit()

        return item
