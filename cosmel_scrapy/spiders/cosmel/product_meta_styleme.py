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

        db.execute('SELECT id, orig_name FROM cosmel.product ORDER BY id')
        self.skip_set_product_meta = {pid: pname for (pid, pname,) in db.fetchall()}

        db.execute('SELECT id, cosmel_id FROM cosmel_styleme.product ORDER BY id')
        self.skip_set_product_styleme = {styleme_id: cosmel_id for (styleme_id, cosmel_id,) in db.fetchall()}

        db.execute('''
            SELECT product.id, product.name, product.descr, brand.cosmel_id
            FROM cosmel_styleme.product AS product
            INNER JOIN cosmel_styleme.brand AS brand ON product.brand_id = brand.id
            ORDER BY id
        ''')
        res = db.fetchall()

        del db

        cosmel_dict = {}
        styleme_dict = {}
        for (pid, pname, pdescr, bid,) in res:
            # logger().spam((pid, pname,))
            assert pid not in cosmel_dict
            assert pid not in styleme_dict
            cosmel_dict[pid] = [pname, pdescr, bid,]
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
        for (pid, (pname, pdescr, bid,),) in cosmel_dict.items():
            if '\u3000' in pname:
                logger().warning(f'u3000? {pid} {pname}')
            if pname != self.skip_set_product_meta.get(pid):
                if not pdescr: pdescr = ''
                items.append(
                    ProductMetaItem(
                        id         = pid,
                        brand_id   = bid,
                        orig_name  = pname,
                        orig_descr = pdescr.replace('\n', ''),
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
        [(307, '皇家蜂王乳平衡油'), (19726, '皇家蜂王乳平衡油',),],
        [(409, '雪紡瞬白BB霜SPF50/PA+++'), (6499, '雪紡瞬白BB霜 SPF50 PA+++',),],
        [(463, 'BB輕粉霜SPF30/PA++'), (6484, 'BB輕粉霜 SPF30 PA++',),],
        [(520, '經典修容N'), (18865, '經典修容 Ｎ',),],
        [(1192, '魔法肌密防曬隔離乳霜SPF50/PA+++'), (7183, '魔法肌密防曬隔離乳霜SPF 50 PA+++',),],
        [(1225, '極效賦活全能防禦乳SPF50/PA++++'), (7186, '極效賦活全能防禦乳SPF50 PA++++',),],
        [(2722, '無瑕輕裸CC霜SPF30/PA++'), (11071, '無瑕輕裸CC霜SPF30 PA++',),],
        [(3940, '時空琉璃御藏防晒乳SPF50/PA++++'), (7579, '時空琉璃御藏防晒乳SPF50+PA++++',),],
        [(5749, '極透氣清爽運動防曬乳SPF50+/PA++++'), (18562, '極透氣清爽運動防曬乳SPF50+ PA++++',),],
        [(6478, '有機橄欖潔顏油'), (19483, '有機橄欖潔顏油',),],
        [(7207, '即可拍～棉花糖柔妍氣墊蜜粉餅',), (7033, '即可拍~棉花糖柔妍氣墊蜜粉餅'),],
        [(7369, '好氣色漸層三色CC輕唇膏'), (18364, '好氣色 漸層三色CC輕唇膏',),],
        [(7372, '超激細抗暈眼線液 抗手震版'), (18838, '超激細抗暈眼線液-抗手震版',),],
        [(8902, '晶透唇膏'), (10651, '晶透唇膏',),],
        [(9190, '完美保濕化粧水(滋潤型)'), (9589, '完美保濕化粧水 滋潤型',),],
        [(9487, '八分子玻尿酸前導機能水'), (14965, '八分子玻尿酸前導機能水',),],
        [(9814, '八分子玻尿酸前導精華乳'), (14968, '八分子玻尿酸前導精華乳',),],
        [(11479, '臉部淨白去角質凝露'), (13375, '臉部淨白去角質凝露',),],
        [(11515, '全效微膠深層潔膚乳'), (12925, '全效微膠深層潔膚乳',),],
        [(11524, '舒緩高效潔膚液'), (14665, '舒緩高效潔膚液',),],
        [(11605, '胺基酸洗顏霜'), (14836, '胺基酸洗顏霜',),],
        [(11608, '極潤橙萃滋養精華霜'), (14959, '極潤橙萃滋養精華霜',),],
        [(11611, '極潤橙萃滋養精華油'), (14962, '極潤橙萃滋養精華油',),],
        [(11614, '逆齡角鯊濃縮精華'), (14944, '逆齡角鯊濃縮精華',),],
        [(11617, '超補水玻尿酸濃縮精華'), (14956, '超補水玻尿酸濃縮精華',),],
        [(11620, '極潤橙萃滋養美白面膜'), (14971, '極潤橙萃滋養美白面膜',),],
        [(11626, '玻尿酸保濕淨化卸妝神水'), (14641, '玻尿酸保濕淨化卸妝神水',),],
        [(11629, '白素肌熬夜霜'), (14974, '白素肌熬夜霜',),],
        [(11632, '白素肌美白霜'), (14977, '白素肌美白霜',),],
        [(11638, '絕對完美防曬隔離乳 SPF50'), (15226, '絕對完美防曬隔離乳SPF50',),],
        [(11641, '白瓷娃娃杏仁酸煥膚素30%'), (14986, '白瓷娃娃杏仁酸煥膚素30%',),],
        [(11644, '神奇剋痘修瑕水'), (14983, '神奇剋痘修瑕水',),],
        [(11647, '酵素洗卸凝露'), (14995, '酵素洗卸凝露',),],
        [(11650, '極潤橙萃滋養精華乳'), (15001, '極潤橙萃滋養精華乳',),],
        [(11653, '極潤橙萃滋養水精華'), (14998, '極潤橙萃滋養水精華',),],
        [(12316, '控油礦物蜜粉餅'), (12823, '控油礦物蜜粉餅',),],
        [(12355, '我愛唇膏'), (17893, '我愛唇膏',),],
        [(13081, '我愛修容魔法棒'), (17611, '我愛修容魔法棒',),],
        [(13828, '我愛腮紅魔法棒'), (17617, '我愛腮紅魔法棒',),],
        [(17134, '我愛亮顏魔法棒'), (17608, '我愛亮顏魔法棒',),],
        [(17137, '我愛氣墊QQ唇'), (17641, '我愛氣墊QQ唇',),],
        [(17140, '我愛粉底魔法棒'), (17614, '我愛粉底魔法棒',),],
        [(17164, 'PONY女王花漾唇膏'), (17605, 'PONY女王花漾唇膏',),],
        [(17728, '美透白雙核晶白淨斑遮瑕筆SPF25 PA+++',), (16576, '美透白雙核晶白淨斑遮瑕筆\u3000SPF25\u3000PA+++'),],
        [(17851, '滋養潔面油'), (19342, '滋養潔面油',),],
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
        (15118, 'SS肌膚補給\u3000亮顏柔嫩Vit C恆白霜', 'SS肌膚補給 亮顏柔嫩Vit C恆白霜',),
        (15124, 'SS肌膚補給\u30002+2雙效淡斑C精華', 'SS肌膚補給 2+2雙效淡斑C精華',),
        (15595, 'SS肌膚補給\u3000Vit A撫紋精華', 'SS肌膚補給 Vit A撫紋精華',),
        (15601, 'SS肌膚補給\u3000美妍醒肌Vit B保濕熬夜霜', 'SS肌膚補給 美妍醒肌Vit B保濕熬夜霜',),
        (20974, '飽水控油雙效日間防護乳SPF50+ PA++++\u3000', '飽水控油雙效日間防護乳SPF50+ PA++++',),
    ]
