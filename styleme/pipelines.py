# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy

from utils.logging import *

from utils.db import Db
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

        try:
            item.submit(self.db)
        except Exception as e:
            logger().error(exceptstr(e))

        self.count += 1
        if self.count >= 1000:
            self.count = 0
            self.db.commit()

        return item
