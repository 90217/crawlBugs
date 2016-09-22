#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-

import scrapy
from vulnerSpider.packetStormItem import packetStormItem

#定义全局变量
prefix_url = 'https://packetstormsecurity.com'

class PacketstormSpider(scrapy.Spider):
    name = "packetStorm"
    allowed_domains = ["packetstormsecurity.com"]
    start_urls = (
        'https://packetstormsecurity.com/files/tags/advisory/',
    )

    def parse(self, response):
        prefix_url = 'https://packetstormsecurity.com'
	pageurls = response.xpath("//a[contains(.//text(), 'Next')]/@href").extract()
	urls = response.xpath('//dt/a/@href').extract()
	for pageurl in pageurls:
	    next_pageurl = prefix_url + pageurl
	    yield scrapy.Request(next_pageurl, callback=self.parse)
	for url in urls:
	    gettext = prefix_url + url
	    #print gettext
	    yield scrapy.Request(gettext, callback=self.parse_text)

    def parse_text(self, response):
	#prefix_url = 'https://packetstormsecurity.com'
	item = packetStormItem()
	partHtml = response.xpath('//html/body/div[2]/div/div/dl')
	partHtmls = response.xpath('//html/body/div[2]/div/div/dl').extract()
	print response.url
	item['title'] = response.xpath('//html/body/div[2]/div/div/dl/dt/a/strong/text()').extract()
	iffield = response.xpath('//html/body/div[2]/div/div/dl/dd[2]/text()').extract()
	iffield3 = response.xpath('//html/body/div[2]/div/div/dl/dd[2]/text()').extract()[0]
	#if len(iffield) > 1:
	#    iffield4 = response.xpath('//html/body/div[2]/div/div/dl/dd[2]/text()').extract()[1]
	if '| Site' in iffield3.strip():
	    item['site'] = response.xpath('//html/body/div[2]/div/div/dl/dd[2]/a/text()').extract()
	    item['authorBy'] = ''
	    if len(iffield) > 1:
	        iffield4 = response.xpath('//html/body/div[2]/div/div/dl/dd[2]/text()').extract()[1]
	    elif '| Site' in iffield4.strip():
	    	item['authorBy'] = response.xpath('//html/body/div[2]/div/div/dl/dd[2]/a[1]/text()').extract()
	    	item['site'] = response.xpath('//html/body/div[2]/div/div/dl/dd[2]/a[2]/text()').extract()
	else:
	    item['authorBy'] = response.xpath('//html/body/div[2]/div/div/dl/dd[2]/a[1]/text()').extract()
            item['site'] = ''
	#item['site'] = response.xpath('//html/body/div[2]/div/div/dl/dd[2]/a[2]/text()').extract()
	item['posted'] = response.xpath('//html/body/div[2]/div/div/dl/dd[1]/a/text()').extract()
	item['detail'] = response.xpath('//html/body/div[2]/div/div/dl/dd[3]/p/text()').extract()
	item['tags'] = response.xpath('//html/body/div[2]/div/div/dl/dd[4]/a/text()').extract()
	iffield1 = response.xpath('//html/body/div[2]/div/div/dl/dd[5]/span/text()').extract()[0]
	if 'system' in iffield1:
	    item['system'] = response.xpath('//html/body/div[2]/div/div/dl/dd[5]/a/text()').extract()
	    iffield2 = response.xpath('//html/body/div[2]/div/div/dl/dd[6]/span/text()').extract()[0]
	    if 'advisories' in iffield2:
	        item['cveid'] = response.xpath('//html/body/div[2]/div/div/dl/dd[6]/a/text()').extract()
	        item['MD5'] =  response.xpath('//html/body/div[2]/div/div/dl/dd[7]/code/text()').extract()
                item['download'] = prefix_url + response.xpath('//html/body/div[2]/div/div/dl/dd[8]/a[1]/@href').extract()[0]
	    else:
	        item['cveid'] = ''
	        item['MD5'] =  response.xpath('//html/body/div[2]/div/div/dl/dd[6]/code/text()').extract()
                item['download'] = prefix_url + response.xpath('//html/body/div[2]/div/div/dl/dd[7]/a[1]/@href').extract()[0]
	    #item['cveid'] = response.xpath('//html/body/div[2]/div/div/dl/dd[6]/a/text()').extract()
	    #item['MD5'] =  response.xpath('//html/body/div[2]/div/div/dl/dd[7]/code/text()').extract()
            #item['download'] = response.xpath('//html/body/div[2]/div/div/dl/dd[8]/a[1]/@href').extract()
	elif 'advisories' in iffield1:
	    item['cveid'] = response.xpath('//html/body/div[2]/div/div/dl/dd[5]/a/text()').extract()
	    item['system'] = '' 
	    item['MD5'] =  response.xpath('//html/body/div[2]/div/div/dl/dd[6]/code/text()').extract()
            item['download'] = prefix_url + response.xpath('//html/body/div[2]/div/div/dl/dd[7]/a[1]/@href').extract()[0]
	else:
	    item['cveid'] = ''
	    item['system'] = ''
	    item['MD5'] =  response.xpath('//html/body/div[2]/div/div/dl/dd[5]/code/text()').extract()
            item['download'] = prefix_url + response.xpath('//html/body/div[2]/div/div/dl/dd[6]/a[1]/@href').extract()[0] 

	#item['cveid'] = response.xpath('//html/body/div[2]/div/div/dl/dd[5]/a/text()').extract()
	#item['MD5'] =  response.xpath('//html/body/div[2]/div/div/dl/dd[6]/code/text()').extract()
	#item['download'] = response.xpath('//html/body/div[2]/div/div/dl/dd[7]/a[1]/@href').extract()
	yield item	
