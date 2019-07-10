# -*- coding: utf-8 -*-
from functools import partial

import scrapy

from utils.logging import *

from ..base import CosmelSpider
from cosmel_scrapy.db import Db
from cosmel_scrapy.items.cosmel import *

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])

    def start_requests(self):
        db = Db(self)

        db.execute('SELECT id, orig_name FROM cosmel.brand ORDER BY id')
        self.skip_set_brand_meta = {bid: bname for (bid, bname,) in db.fetchall()}

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
                        id        = bid,
                        orig_name = bname,
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
        [(11, 'SHISEIDO 資生堂',), (29, 'SHISEIDO 資生堂（國際櫃）',), (9013, 'SHISEIDO 資生堂（開架式）',),],
        [(20, 'KOSE 高絲',), (9001, 'CLEAR TURN',),],
        [(43, 'CLARINS 克蘭詩',), (9003, 'Clarins 克蘭詩',),],
        [(340, 'noreva 法國歐德瑪',), (907, '法國歐德瑪',),],
        [(370, 'Hada-Labo 肌研',), (841, 'HADALABO',),],
        [(406, 'Dr.Morita 森田藥粧'), (9005, 'Dr.Morita',),],
        [(457, 'Pure Beauty',), (1189, 'PUREBEAUTY',),],
        [(463, 'Za',), (9016, 'ZA',),],
        [(487, 'neuve 惹我',), (916, 'FITIT&WHITIA',),],
        [(511, 'Anime Cosme',), (1000, 'ANIMECOSME',),],
        [(838, 'CHRONO AFFECTION 時間寵愛',), (9019, '時間寵愛',),],
        [(868, 'EQUILIBRA 義貝拉',), (940, 'PERLABELLA 義貝拉',), (943, 'SYRIO',),],
        [(970, 'MEMEBOX',), (1402, 'PONY EFFECT',), (1606, 'PONY女王',), (9008, 'MEMEBOX',),],
        [(976, '西班牙Babaria',), (1030, 'babaria 西班牙babaria',),],
        [(925, 'A’PIEU',), (1009, 'A\'PIEU',),],
        [(1525, 'Natura Bissé',), (1597, 'Natura Bissé',),],
    ]

    rename_list = [
        (11, 'SHISEIDO 資生堂（東京櫃）', 'SHISEIDO 資生堂',),
        (970, 'I’M MEME', 'MEMEBOX',),
    ]
