# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 写字楼
class OfficeItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 标题名字
    name = scrapy.Field()
    # 价格
    dengji = scrapy.Field()
    title = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    type = scrapy.Field()
    price = scrapy.Field()
    total_price = scrapy.Field()
    big_address = scrapy.Field()
    address = scrapy.Field()
    xiaoqu = scrapy.Field()
    origin_url = scrapy.Field()
    ruzhushijian = scrapy.Field()
    shifoufenge = scrapy.Field()
    wuyefei = scrapy.Field()
    zhifufangshi = scrapy.Field()
    use_for = scrapy.Field()
    zhuangxiu = scrapy.Field()
    guapaishijian = scrapy.Field()
    height = scrapy.Field()
    deep = scrapy.Field()
    weight = scrapy.Field()
    mianzuqi = scrapy.Field()
    qizuqi = scrapy.Field()
    zhuanrangfei = scrapy.Field()


# 商铺
class ShopItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 二手房名称
    title = scrapy.Field()
    xiaoqu = scrapy.Field()
    address = scrapy.Field()
    floor = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    total_price = scrapy.Field()
    type = scrapy.Field()
    origin_url = scrapy.Field()
    wuyefei = scrapy.Field()
    zhifufangshi = scrapy.Field()
    use_for = scrapy.Field()
    zhuangxiu = scrapy.Field()
    guapaishijian = scrapy.Field()
    height = scrapy.Field()
    deep = scrapy.Field()
    weight = scrapy.Field()
    mianzuqi = scrapy.Field()
    qizuqi = scrapy.Field()
    zhuanrangfei = scrapy.Field()




