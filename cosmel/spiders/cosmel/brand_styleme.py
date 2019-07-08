# -*- coding: utf-8 -*-
import json
from functools import partial

import scrapy

from utils.logging import *

from ..base import CosmelSpider
from cosmel.db import Db
from cosmel.items.cosmel import *

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])

    def start_requests(self):
        db = Db(self)

        db.execute('SELECT id, name FROM cosmel.brand ORDER BY id')
        self.skip_set_brand_meta = {bid: name for (bid, name,) in db.fetchall()}

        db.execute('SELECT id, cosmel_id FROM cosmel_styleme.brand ORDER BY id')
        self.skip_set_brand_styleme = {styleme_id: cosmel_id for (styleme_id, cosmel_id,) in db.fetchall()}

        db.execute('SELECT id, name FROM cosmel_styleme.brand ORDER BY id')
        res = db.fetchall()

        del db

        cosmel_dict = {}
        styleme_dict = {}
        for (bid, bname,) in res:
            # logger().spam((bid, bname,))
            assert bid not in cosmel_dict
            assert bid not in styleme_dict
            cosmel_dict[bid] = bname
            styleme_dict[bid] = bid

        # Rename
        for (bid, bname_old, bname_new,) in self.rename_list:
            logger().info(f'{bid} {bname_old} -> {bname_new}')
            assert cosmel_dict[bid] == bname_old
            cosmel_dict[bid] = bname_new

        # Merge
        for merge_tuple in self.merge_list:
            cosmel_bid, cosmel_bname = merge_tuple[0]
            assert cosmel_dict[cosmel_bid] == cosmel_bname
            for styleme_bid, styleme_bname in merge_tuple[1:]:
                logger().verbose(f'{cosmel_bid} {cosmel_bname} <- {styleme_bid} {styleme_bname}')
                assert cosmel_dict[styleme_bid] == styleme_bname
                del cosmel_dict[styleme_bid]
                styleme_dict[styleme_bid] = cosmel_bid

        # Items
        items = []
        for (bid, bname,) in cosmel_dict.items():
            if bname != self.skip_set_brand_meta.get(bid):
                items.append(
                    BrandMetaItem(
                        id   = bid,
                        name = bname,
                    )
                )

        for (styleme_id, cosmel_id,) in styleme_dict.items():
            if cosmel_id != self.skip_set_brand_styleme.get(styleme_id):
                items.append(
                    BrandStylemeItem(
                        styleme_id = styleme_id,
                        cosmel_id  = cosmel_id,
                    )
                )

        yield from self.do_items(*items)

    merge_list = [
        [(11, 'SHISEIDO 資生堂',), (29, 'SHISEIDO 資生堂（國際櫃）',),],
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

    rename_list = [
        (11, 'SHISEIDO 資生堂（東京櫃）', 'SHISEIDO 資生堂',)
    ]
