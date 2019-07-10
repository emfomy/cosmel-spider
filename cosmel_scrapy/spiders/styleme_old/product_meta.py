# -*- coding: utf-8 -*-
import csv
from functools import partial

import scrapy

from utils.logging import *

from ..base import CosmelSpider
from cosmel_scrapy.db import Db
from cosmel_scrapy.items.styleme import *

from cosmel.util.text import check_contain_chinese

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])
    allowed_domains = ['styleme.pixnet.net']

    def start_requests(self):

        db = Db(self)

        db.execute('SELECT id, name FROM cosmel_styleme.brand ORDER BY id')
        bname2bid = {bname: bid for (bid, bname,) in db.fetchall()}

        db.execute('SELECT id, name FROM cosmel_styleme.product ORDER BY id')
        pid2pname = {pid: pname for (pid, pname,) in db.fetchall()}

        del db

        unknown_brand_dict = set()

        # Items
        items = []
        with open('./data/styleme.csv') as fin:
            for row in csv.DictReader(fin):
                if not row['編號'] or not row['中文品名'] or \
                        '測試' in row['品牌'] or '測試' in row['中文品名'] or \
                        'test' in row['品牌'].lower() or 'test' in row['中文品名'].lower() or \
                        not check_contain_chinese(row['中文品名']):
                    # logger().spam(f'Skip product {row["編號"]}')
                    continue

                # Extract
                pid   = int(row['編號'])
                bid   = None
                bname = row['品牌']
                pname = row['中文品名']
                descr = row['中文簡介']

                # Fix typo
                if bname == '80': bname = '080'
                if not bname: bname = None
                if not descr: descr = ''
                if pid in self.pname2bname:
                    assert pname == self.pname2bname[pid][0], (pid, pname, self.pname2bname[pid],)
                    bname = self.pname2bname[pid][1]
                    logger().verbose(f'{pid} {pname} <- {bname}')

                # Skip product
                if pid in self.skip_list:
                    assert pname == self.skip_list[pid], (pid, pname, self.skip_list[pid],)
                    continue
                if pid in pid2pname:
                    continue

                # Unknown brand
                if bname not in bname2bid:
                    if bname: unknown_brand_dict.add(bname)
                    logger().warning(f'Unknown Brand: {bname} {pid} {pname}')
                    continue
                else:
                    bid = bname2bid[bname]

                logger().info((pid, pname,))
                items.append(
                    ProductMetaItem(
                        id       = pid,
                        brand_id = bid,
                        name     = pname,
                    )
                )
                items.append(
                    ProductInfoItem(
                        id       = pid,
                        descr    = descr,
                    )
                )

        for bname in sorted(unknown_brand_dict):
            logger().warning(f'Unknown Brand: {bname}')

        yield from self.do_items(*items)

    skip_list = {
    }

    pname2bname = {
        670:  ('絕對完美極緻再生眼霜', 'LANCÔME 蘭蔻',),
        3517: ('水感奇蹟四色蜜粉餅', 'LANCÔME 蘭蔻',),
        3766: ('絕對完美玫瑰乳霜面膜', 'LANCÔME 蘭蔻',),
        3769: ('絕對完美玫瑰修護唇霜', 'LANCÔME 蘭蔻',),
        3781: ('絕對完美黑鑽精華油', 'LANCÔME 蘭蔻',),
        4153: ('粉持久超級防水眼線筆', 'ESTÉE LAUDER 雅詩蘭黛',),
        4243: ('極淨光透白修護面膜', 'ESTÉE LAUDER 雅詩蘭黛',),
        5680: ('超未來不老女神微笑唇萃', 'ESTÉE LAUDER 雅詩蘭黛',),
        5683: ('超未來立體緊緻美頸胸霜', 'ESTÉE LAUDER 雅詩蘭黛',),
        6382: ('超水妍舒緩保濕凝露', 'LANCÔME 蘭蔻',),
        6415: ('鑽石立體超緊緻眼霜', 'ESTÉE LAUDER 雅詩蘭黛',),
        7333: ('蓬鬆波浪造型凍', 'MA CHÉRIE 瑪宣妮',),
        7651: ('黑天鵝超精準眼線液', 'LANCÔME 蘭蔻',),
        7948: ('超緊顏5D太空抗皺晚霜', 'LANCÔME 蘭蔻',),
        7951: ('超緊顏5D太空抗皺眼霜', 'LANCÔME 蘭蔻',),
        7954: ('超緊顏5D拉提滾輪', 'LANCÔME 蘭蔻',),
        7957: ('超緊顏5D太空按摩霜', 'LANCÔME 蘭蔻',),
        7960: ('超緊顏5D太空抗皺精露', 'LANCÔME 蘭蔻',),
        7963: ('超緊顏5D太空抗皺日霜(太空霜)-經典型', 'LANCÔME 蘭蔻',),
        7966: ('超緊顏5D太空抗皺日霜(太空霜)-水潤型', 'LANCÔME 蘭蔻',),
        7969: ('玫瑰之心淡香精', 'Chloé',),
        8122: ('9色限量眼彩盤', 'LANCÔME 蘭蔻',),
        8125: ('花瓣漸層唇蠟筆', 'LANCÔME 蘭蔻',),
        8131: ('愛戀亮色指甲油', 'LANCÔME 蘭蔻',),
        8299: ('年輕肌密煥膚凝乳', 'ESTÉE LAUDER 雅詩蘭黛',),
        8392: ('捲髮髮妝水(珍珠蜂蜜精華)', 'MA CHÉRIE 瑪宣妮',),
        8395: ('清爽髮妝水(珍珠蜂蜜精華)', 'MA CHÉRIE 瑪宣妮',),
        8398: ('保濕髮妝水(珍珠蜂蜜精華)', 'MA CHÉRIE 瑪宣妮',),
    }
