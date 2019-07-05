#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CosmelItem(scrapy.Item):

    def submit(self, db):
        raise NotImplementedError
