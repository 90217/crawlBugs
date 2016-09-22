import scrapy

class packetStormItem(scrapy.Item):
    title = scrapy.Field()
    authorBy = scrapy.Field()
    site = scrapy.Field()
    posted = scrapy.Field()
    detail = scrapy.Field()
    tags = scrapy.Field()
    cveid = scrapy.Field()
    MD5 = scrapy.Field()
    system = scrapy.Field()
    download = scrapy.Field()
