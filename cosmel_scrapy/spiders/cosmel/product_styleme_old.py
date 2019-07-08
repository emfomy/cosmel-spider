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

        db.execute('SELECT id, orig_name FROM cosmel.product ORDER BY id')
        self.skip_set_product_meta = {pid: pname for (pid, pname,) in db.fetchall()}

        db.execute('SELECT id, cosmel_id FROM cosmel_styleme.product ORDER BY id')
        styleme_dict_new = {styleme_id: cosmel_id for (styleme_id, cosmel_id,) in db.fetchall()}

        db.execute('SELECT id, cosmel_id FROM cosmel_styleme_old.product ORDER BY id')
        self.skip_set_product_styleme = {styleme_id: cosmel_id for (styleme_id, cosmel_id,) in db.fetchall()}

        db.execute('SELECT id, name, descr, brand_id FROM cosmel_styleme_old.product ORDER BY id')
        res = db.fetchall()

        del db

        # Import
        cosmel_dict = {}
        styleme_dict = {}
        for (pid, pname, pdescr, bid,) in res:
            # logger().spam((pid, pname,))
            assert pid not in cosmel_dict
            assert pid not in styleme_dict
            cosmel_dict[pid] = [pname, pdescr, bid,]
            styleme_dict[pid] = pid

        # Link cosmel_id
        for (styleme_id, cosmel_id,) in styleme_dict_new.items():
            if styleme_id in styleme_dict:
                if styleme_id != cosmel_id: logger().verbose(f'{cosmel_id} <- {styleme_id} {cosmel_dict[styleme_id][0]}')
                del cosmel_dict[styleme_id]
                styleme_dict[styleme_id] = cosmel_id

        # Delete product w/o brand
        cosmel_bad_set = {pid for pid, (pname, _, bid,) in cosmel_dict.items() if not bid}
        for pid in cosmel_bad_set:
            logger().spam(f'DELETE! {pid} {cosmel_dict[pid][0]}')
            del cosmel_dict[pid]

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
        for (pid, (pname, pdescr, bid,),) in cosmel_dict.items():
            if pname != self.skip_set_product_meta.get(pid):
                items.append(
                    ProductMetaItem(
                        id         = pid,
                        brand_id   = bid,
                        orig_name  = pname,
                        orig_descr = pdescr.replace('\n', '') if pdescr else None,
                    )
                )

        for (styleme_id, cosmel_id,) in styleme_dict.items():
            if cosmel_id not in cosmel_dict: continue
            if cosmel_id != self.skip_set_product_styleme.get(styleme_id):
                items.append(
                    ProductStylemeOldItem(
                        styleme_id = styleme_id,
                        cosmel_id  = cosmel_id,
                    )
                )

        yield from self.do_items(*items)

    merge_list = [
        [(6175, '純淨植物洗面乳(瑩透型)',), (11995, '純淨植物洗面乳(瑩透型)',),]
    ]

    rename_list = [
    ]
