# -*- coding: utf-8 -*-
from functools import partial

import scrapy

from utils.logging import *

from ..base import CosmelSpider
from cosmel_scrapy.db import Db
from cosmel_scrapy.items.styleme import *

class Spider(scrapy.Spider, CosmelSpider):
    name = '_'.join(__name__.split('.')[-2:])
    allowed_domains = ['styleme.pixnet.net']

    def start_requests(self):

        db = Db(self)

        db.execute('SELECT id, name FROM cosmel_styleme.brand ORDER BY id')
        bname2bid = {bname: bid for (bid, bname,) in db.fetchall()}

        del db

        # Items
        items = []
        for (bid, bname,) in self.old_brand_list:
            if bname in bname2bid:
                assert bid == bname2bid[bname]
            else:
                logger().verbose(f'New Brand {bid} {bname}')

                items.append(
                    BrandMetaItem(
                        id   = bid,
                        name = bname,
                    )
                )

        yield from self.do_items(*items)

    old_brand_list = [
        (9000, 'Bio oil 百洛',),
        (9001, 'CLEAR TURN',),
        (9002, 'CORSICA 科皙佳',),
        (9003, 'Clarins 克蘭詩',),
        (9004, 'Covermark',),
        (9005, 'Dr.Morita',),
        (9006, 'HACCI',),
        (9007, 'LUDEYA 露蒂雅',),
        (9008, 'MEMEBOX',),
        (9009, 'MUJI 無印良品',),
        (9010, 'Mdmmd. 明洞國際',),
        (9011, 'PURE',),
        (9012, 'Panatec 沛莉緹',),
        (9013, 'SHISEIDO 資生堂（開架式）',),
        (9014, 'TSZJITSUEI 瓷肌萃',),
        (9015, 'White',),
        (9016, 'ZA',),
        (9017, 'motives 莫蒂膚',),
        (9018, '御泥坊',),
        (9019, '時間寵愛',),
    ]
