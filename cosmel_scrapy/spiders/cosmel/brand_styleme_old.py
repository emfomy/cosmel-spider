# -*- coding: utf-8 -*-
import json
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
        cosmel_dict_inv = {bname.lower(): bid for (bid, bname,) in db.fetchall()}

        db.execute('SELECT cosmel_id, name FROM cosmel_styleme.brand ORDER BY id')
        cosmel_dict_inv.update({bname.lower(): bid for (bid, bname,) in db.fetchall()})

        db.execute('SELECT DISTINCT brand_name FROM cosmel_styleme_old.product WHERE brand_name IS NOT NULL')
        res = db.fetchall()

        del db

        # Merge
        for merge_tuple in self.merge_list:
            cosmel_bid, cosmel_bname = merge_tuple[0]
            assert cosmel_dict_inv[cosmel_bname.lower()] == cosmel_bid
            for (styleme_bname,) in merge_tuple[1:]:
                logger().verbose(f'{cosmel_bid} {cosmel_bname} <- {styleme_bname}')
                cosmel_dict_inv[styleme_bname.lower()] = cosmel_bid

        # Check
        for (bname,) in res:
            if bname.lower() not in cosmel_dict_inv:
                logger().warning(bname)

        # Items
        items = []
        for (bname, bid,) in cosmel_dict_inv.items():
            items.append(
                BrandMetaStylemeOldItem(
                    id = bid,
                    name = bname,
                )
            )

        yield from self.do_items(*items)

    merge_list = [
        [(11, 'SHISEIDO 資生堂',), ('SHISEIDO 資生堂（開架式）',),],
        [(20, 'KOSE 高絲',), ('CLEAR TURN',),],
        [(406, 'Dr.Morita 森田藥粧'), ('Dr.Morita',),],
        [(838, 'CHRONO AFFECTION 時間寵愛',), ('時間寵愛',),],
    ]

    new_list = [
        (9000, 'Bio oil 百洛',),
        (9001, 'CORSICA 科皙佳',),
        (9002, 'Covermark',),
        (9003, 'HACCI',),
        (9004, 'LUDEYA 露蒂雅',),
        (9005, 'Mdmmd. 明洞國際',),
        (9006, 'motives 莫蒂膚',),
        (9007, 'MUJI 無印良品',),
        (9008, 'Panatec 沛莉緹',),
        (9009, 'PURE',),
        (9010, 'TSZJITSUEI 瓷肌萃',),
        (9011, 'White',),
        (9012, '御泥坊',),
    ]
