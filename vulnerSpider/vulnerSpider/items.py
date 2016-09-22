# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
class VulnerspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
"""
class WooyunItem(scrapy.Item):
    # define the fields for your item here like:
    detail=scrapy.Field()
    zhengming=scrapy.Field()
    msolution=scrapy.Field()
    guanzhu=scrapy.Field()
    description=scrapy.Field()
    hashcode=scrapy.Field()
    rank=scrapy.Field()
    bianhao=scrapy.Field()
    factory=scrapy.Field()
    author=scrapy.Field()
    resource=scrapy.Field()
    title=scrapy.Field()
    buydate=scrapy.Field()
    online=scrapy.Field()
    sort=scrapy.Field()
    dengji=scrapy.Field()
    state=scrapy.Field()
    tags=scrapy.Field()
    modify=scrapy.Field()
    cve=scrapy.Field()
    patch=scrapy.Field()
    shoulu=scrapy.Field()
    fresh=scrapy.Field()
    send=scrapy.Field()
