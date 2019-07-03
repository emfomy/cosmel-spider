# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import *

from ..db import Db
from ..items import *

class Spider(scrapy.Spider):
    name = __name__.split('.')[-1]
    allowed_domains = ['styleme.pixnet.net']

    def start_requests(self):
        db = Db(self)

        db.execute('SELECT id, name FROM brand WHERE id NOT IN (SELECT id from brand_merge) ORDER BY id')
        res = db.fetchall()

        db.execute('SELECT id, name FROM brand_merge ORDER BY id')
        res += db.fetchall()

        del db

        bid2bname = {}

        total = len(res)
        for i, (bid, bname,) in enumerate(res):
            # logger().info((bid, bname,))
            bid2bname[bid] = bname

        # Check typo
        for merge_tuple in self.merge_list:
            for brand in merge_tuple:
                assert bid2bname[brand[0]] == brand[1], brand

        # Merge
        items = []
        for merge_tuple in self.merge_list:
            for brand in merge_tuple[1:]:
                logger().info(f'{brand} -> {merge_tuple[0]}')
                items.append(
                    BrandMergeItem(
                        id    = brand[0],
                        name  = brand[1],
                        merge = merge_tuple[0][0],
                    )
                )

        yield from self.do_items(*items)

    def do_items(self, *items):
        yield scrapy.Request(
            'https://styleme.pixnet.net',
            callback=partial(self.parse_items, items=items),
        )

    def parse_items(self, _, *, items):
        return iter(items)

    merge_list = [
        [(10000, 'SHISEIDO 資生堂',), (11, 'SHISEIDO 資生堂（東京櫃）',), (29, 'SHISEIDO 資生堂（國際櫃）',),],
        [(340, 'noreva 法國歐德瑪',), (907, '法國歐德瑪',),],
        [(370, 'Hada-Labo 肌研',), (841, 'HADALABO',),],
        [(457, 'Pure Beauty',), (1189, 'PUREBEAUTY',),],
        [(487, 'neuve 惹我',), (916, 'FITIT&WHITIA',),],
        [(511, 'Anime Cosme',), (1000, 'ANIMECOSME',),],
        [(868, 'EQUILIBRA 義貝拉',), (940, 'PERLABELLA 義貝拉',), (943, 'SYRIO',),],
        [(976, '西班牙Babaria',), (1030, 'babaria 西班牙babaria',),],
        [(925, 'A’PIEU',), (1009, 'A\'PIEU',),],
        [(1525, 'Natura Bissé',), (1597, 'Natura Bissé',),],
    ]
