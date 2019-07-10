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

class ProductNameItem(CosmelItem):
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

class ProductSentenceItem(CosmelItem):
    id = scrapy.Field()
    lines = scrapy.Field()

    def __repr__(self):
        return repr({ k: v for k, v in self.items() if k != 'lines' })

    def submit(self, db):

        pid = self['id']
        vals = [(pid, sid, line,) for (sid, line,) in enumerate(self['lines'])]
        db.executemany(
            'INSERT IGNORE INTO cosmel.product_descr (product_id, sentence_id, text) VALUES (%s, %s, %s)',
            vals
        )

class ArticleMetaItem(CosmelItem):
    id = scrapy.Field()
    link = scrapy.Field()
    orig_title = scrapy.Field()
    subcategory_id = scrapy.Field()

    def __repr__(self):
        return repr({ k: v for k, v in self.items() if k != 'link' })

    def submit(self, db):
        db.execute(
            'INSERT IGNORE INTO cosmel.article (id, link, orig_title, subcategory_id) VALUES (%s, %s, %s)',
            (self['id'], self['link'], self['orig_title'], self['subcategory_id'],)
        )

class ArticleBodyItem(CosmelItem):
    id = scrapy.Field()
    callback = scrapy.Field()

    def __repr__(self):
        return repr({ k: v for k, v in self.items() if k != 'callback' })

    def submit(self, db):

        html_body = self['callback']()

        db.execute(
            '''
                UPDATE cosmel.article
                SET html_body = %s
                WHERE id = %s
            ''',
            (html_body, self['id'],)
        )

class ArticleSentenceItem(CosmelItem):
    aid = scrapy.Field()
    callback = scrapy.Field()

    def __repr__(self):
        return repr({ k: v for k, v in self.items() if k != 'callback' })

    def submit(self, db):

        aid = self['aid']
        lines, num_title = self['callback']()

        vals = [(aid, sid, line, (sid < num_title),) for (sid, line,) in enumerate(lines)]
        db.executemany(
            'INSERT IGNORE INTO cosmel.article_content (article_id, sentence_id, text, is_title) VALUES (%s, %s, %s, %s)',
            vals
        )
