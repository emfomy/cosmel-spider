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

        db.execute('SELECT id, name FROM cosmel.product ORDER BY id')
        self.skip_set_product_meta = {pid: name for (pid, name,) in db.fetchall()}

        db.execute('SELECT id, cosmel_id FROM cosmel_styleme.product ORDER BY id')
        self.skip_set_product_styleme = {styleme_id: cosmel_id for (styleme_id, cosmel_id,) in db.fetchall()}

        db.execute('''
            SELECT product.id, product.name, brand.cosmel_id
            FROM cosmel_styleme.product AS product
            INNER JOIN cosmel_styleme.brand AS brand ON product.brand_id = brand.id
            ORDER BY id;
        ''')
        res = db.fetchall()

        del db

        cosmel_dict = {}
        styleme_dict = {}
        for (pid, pname, bid,) in res:
            # logger().spam((pid, pname,))
            assert pid not in cosmel_dict
            assert pid not in styleme_dict
            cosmel_dict[pid] = [pname, bid,]
            styleme_dict[pid] = pid

        # Rename
        for (pid, pname_old, pname_new,) in self.rename_list:
            logger().info(f'{pid} {pname_old} -> {pname_new}')
            assert cosmel_dict[pid][0] == pname_old
            cosmel_dict[pid][0] = pname_new

        # Merge
        for merge_tuple in self.merge_list:
            cosmel_pid, cosmel_pname = merge_tuple[0]
            assert cosmel_dict[cosmel_pid][0] == cosmel_pname
            for styleme_pid, styleme_pname in merge_tuple[1:]:
                logger().verbose(f'{cosmel_pid} {cosmel_pname} <- {styleme_pid} {styleme_pname}')
                assert cosmel_dict[styleme_pid][0] == styleme_pname
                del cosmel_dict[styleme_pid]
                styleme_dict[styleme_pid] = cosmel_pid

        # Items
        items = []
        for (pid, (pname, bid,),) in cosmel_dict.items():
            if pname != self.skip_set_product_meta.get(pid):
                items.append(
                    ProductMetaItem(
                        id       = pid,
                        name     = pname,
                        brand_id = bid,
                    )
                )

        for (styleme_id, cosmel_id,) in styleme_dict.items():
            if cosmel_id != self.skip_set_product_styleme.get(styleme_id):
                items.append(
                    ProductStylemeItem(
                        styleme_id = styleme_id,
                        cosmel_id  = cosmel_id,
                    )
                )

        yield from self.do_items(*items)

    merge_list = [
        [(409, '雪紡瞬白BB霜SPF50/PA+++'), (6499, '雪紡瞬白BB霜 SPF50 PA+++',),],
        [(463, 'BB輕粉霜SPF30/PA++'), (6484, 'BB輕粉霜 SPF30 PA++',),],
        [(520, '經典修容N'), (18865, '經典修容 Ｎ',),],
        [(1192, '魔法肌密防曬隔離乳霜SPF50/PA+++'), (7183, '魔法肌密防曬隔離乳霜SPF 50 PA+++',),],
        [(1225, '極效賦活全能防禦乳SPF50/PA++++'), (7186, '極效賦活全能防禦乳SPF50 PA++++',),],
        [(5749, '極透氣清爽運動防曬乳SPF50+/PA++++'), (18562, '極透氣清爽運動防曬乳SPF50+ PA++++',),],
        [(7207, '即可拍～棉花糖柔妍氣墊蜜粉餅',), (7033, '即可拍~棉花糖柔妍氣墊蜜粉餅'),],
        [(7369, '好氣色漸層三色CC輕唇膏'), (18364, '好氣色 漸層三色CC輕唇膏',),],
        [(7372, '超激細抗暈眼線液 抗手震版'), (18838, '超激細抗暈眼線液-抗手震版',),],
        [(9190, '完美保濕化粧水(滋潤型)'), (9589, '完美保濕化粧水 滋潤型',),],
        [(11515, '全效微膠深層潔膚乳'), (12925, '全效微膠深層潔膚乳',),],
        [(11638, '絕對完美防曬隔離乳 SPF50'), (15226, '絕對完美防曬隔離乳SPF50',),],
        [(12316, '控油礦物蜜粉餅'), (12823, '控油礦物蜜粉餅',),],
        [(16576, '美透白雙核晶白淨斑遮瑕筆\u3000SPF25\u3000PA+++'), (17728, '美透白雙核晶白淨斑遮瑕筆SPF25 PA+++',),],
        [(19945, '即可拍～微霧光無瑕氣墊粉餅',), (19027, '即可拍微霧光無瑕氣墊粉餅'),],
    ]

    rename_list = [
        (583, '美透白集中淡斑精華素+', '美透白集中淡斑精華素',),
        (2761, '水感透顏粉底精華SFP30/PA+++', '水感透顏粉底精華SPF30/PA+++',),
        (11449, '魚子高效活氧亮白精', '魚子高效活氧亮白精華液',),
        (12502, '無瑕娃娃粉餅SPA18 PA+', '無瑕娃娃粉餅SPF18 PA+',),
        (13315, '保濕修復膠囊面膜A', '保濕修復膠囊面膜A',),
        (13324, '保濕舒緩膠囊面膜B', '保濕舒緩膠囊面膜B',),
        (13336, '緊緻抗皺膠囊面膜', '緊緻抗皺膠囊面膜E',),
        (13342, '再生煥膚膠囊面膜', '再生煥膚膠囊面膜D',),
        (13345, '瞬效亮白膠囊面膜', '瞬效亮白膠囊面膜C',),
    ]
