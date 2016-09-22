# -*- coding: utf-8 -*-
import scrapy
from vulnerSpider.items import WooyunItem

class WooSpider(scrapy.Spider):
    name = "WooSpider"
    allowed_domains = ["wooyun.org"]
    start_urls = [
        'http://www.wooyun.org/bugs/'
    ]

    def parse(self, response):
        pageurls=response.xpath('//p[@class="page"]//a//@href').extract()
        holeurls=response.xpath('//table[@class="listTable"]//tbody//tr//td//a//@href').extract()
        print holeurls
        for pageurl in pageurls:
            newurl='http://www.wooyun.org'+pageurl
            yield scrapy.Request(newurl,callback=self.parse)
        for holeurl in holeurls:
            newurl='http://www.wooyun.org'+holeurl
            print newurl
            yield scrapy.Request(newurl,callback=self.parse_hole)
	
    def parse_hole(self, response):
        item=WooyunItem()
#        item['bianhao']=response.xpath('//div[@class="content"]//h3[1]//a//text()').extract()[0]
#        item['factory']=response.xpath('//div[@class="content"]//h3[3]//a//text()').extract()[0]
#        item['author']=response.xpath('//div[@class="content"]//h3[4]//a//text()').extract()[0]
#        item['resource']=response.xpath('//div[@class="content"]//h3[10]//a//text()').extract()[0]
        rank=response.xpath('//div[@class="content"]//h3[9]//text()').extract()[0]
        if u'\u81ea\u8bc4Rank' in rank:
            item['rank']=rank.split('\t')[-1]
        else:
            item['rank']=None
        
        
        item['bianhao']=response.xpath('//div[@class="content"]//h3//a//text()').extract()[0].replace('\t','').replace('\r','').replace('\n','')
        item['factory']=response.xpath('//div[@class="content"]//h3//a//text()').extract()[1].replace('\t','').replace('\r','').replace('\n','')
        item['author']=response.xpath('//div[@class="content"]//h3//a//text()').extract()[2].replace('\t','').replace('\r','').replace('\n','')
        item['resource']=response.xpath('//div[@class="content"]//h3//a//text()').extract()[3].replace('\t','').replace('\r','').replace('\n','')
       
        
        item['title']=response.xpath('//div[@class="content"]//h3[@class="wybug_title"]//text()').extract()[0].split('\t')[2]
        item['buydate']=response.xpath('//div[@class="content"]//h3[@class="wybug_date"]//text()').extract()[0].split('\t')[-1]
        item['online']=response.xpath('//div[@class="content"]//h3[@class="wybug_open_date"]//text()').extract()[0].split('\t')[-1]
        item['sort']=response.xpath('//div[@class="content"]//h3[@class="wybug_type"]//text()').extract()[0].split('\t')[-1]
        item['dengji']=response.xpath('//div[@class="content"]//h3[@class="wybug_level"]//text()').extract()[0].split('\t')[-1]
        item['state']=response.xpath('//div[@class="content"]//h3[@class="wybug_status"]//text()').extract()[0].replace('\t','').split('\n')[1]
        tags11=response.xpath('//div[@class="content"]//h3[11]//text()').extract()[0]
        tags12=response.xpath('//div[@class="content"]//h3[12]//text()').extract()[0]
        tags13=response.xpath('//div[@class="content"]//h3[13]//text()').extract()[0]
        if u'Tags\u6807\u7b7e\uff1a' in tags11:
            newtag=tags11.replace('\t','').split('\n')[1]
            if newtag=='':
                item['tags']=''.join(response.xpath('//div[@class="content"]//h3[11]//a//text()').extract())
            else:
                item['tags']=newtag
        elif u'Tags\u6807\u7b7e\uff1a' in tags12:
            newtag=tags12.replace('\t','').split('\n')[1]
            if newtag=='':
                item['tags']=''.join(response.xpath('//div[@class="content"]//h3[12]//a//text()').extract())
            else:
                item['tags']=newtag
        else:
            newtag=tags13.replace('\t','').split('\n')[1]
            if newtag=='':
                item['tags']=''.join(response.xpath('//div[@class="content"]//h3[13]//a//text()').extract())
            else:
                item['tags']=newtag
        modify=response.xpath('//div[@class="content"]//h3[6]//text()').extract()[0]
        if  u'\u4fee\u590d\u65f6\u95f4\uff1a' in modify:
            item['modify']=modify.split("\t")[2]
        else:
            item['modify']=None
        info=response.xpath('//div[@class="content"]//p[@class="detail wybug_description"]//text()').extract()
        if info==[]:
            item['description']=None
        else:
            item['description']=info[0]
        
        info=response.xpath('//div[@class="content"]//h3[@class="detailTitle"]//text()').extract()[2]
        if u'\u6f0f\u6d1ehash\uff1a' in info:
            item['hashcode']=info
        else:
            item['hashcode']=None
        item['guanzhu']=response.xpath('//div[@class="content"]//span[@id="attention_num"]//text()').extract()[0]
        info= response.xpath('//div[@class="content"]//div[@class="wybug_patch"]')
        if info==[]:
            item['msolution']=None
        else:
            item['msolution']=info.xpath('p[@class="detail"]//text()').extract()[0]
        info=response.xpath('//div[@class="content"]//div[@class="wybug_poc"]')
        information=""
        if info!=[]:
            for p in info.xpath('p'):
                if p.xpath('a')==[]:
                    if p.xpath('text()').extract()==[]:
                        information+=""
                    else:
                        information+=''.join(p.xpath('text()').extract())
                else:
                    information+=",picture url:"+p.xpath('a//@href').extract()[0]+","
        if information=="":
            item['zhengming']=None
        else:
            item['zhengming']=information
        
        info=response.xpath('//div[@class="content"]//div[@class="wybug_detail"]')
        information=""
        if info!=[]:
            for p in info.xpath('p'):
                if p.xpath('a')==[]:
                    if p.xpath('text()').extract()==[]:
                        information+=""
                    else:
                        information+=''.join(p.xpath('text()').extract())
                else:
                    information+=",picture url:"+p.xpath('a//@href').extract()[0]+","
        if information=="":
            item['detail']=None
        else:
            item['detail']=information
        item['cve']=None
        item['patch']=None
        item['shoulu']=None
        item['fresh']=None
        item['send']=None
        yield item
