# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from dmproperties.items import DmpropertiesItem

class PropertiesSpider(scrapy.Spider):
    name = 'properties'
    allowed_domains = ['www.dmproperties.com']
    start_urls = ['https://www.dmproperties.com/property/']

    def parse(self, response):
        links=response.xpath('//h2//a//@href').extract()
        for link in links:
            #yield{'url':link}
            yield Request(link, callback=self.parse_property)
            #meta={'Url':link})

    def parse_property(self,response):
        l = ItemLoader(item=DmpropertiesItem(), response=response)

        Name=response.xpath('//h1//text()').extract_first()
        Price=response.xpath('//td[2]//text()').extract()[1]
        #link = response.meta['Url']
        image_urls = response.xpath('//*[@class="image-link"]//@href').extract_first()
        image_urls = response.urljoin(image_urls)

        l.add_value('image_urls', image_urls)
        l.add_value('Name',Name)
        l.add_value('Price',Price)
        #l.add_value('link',link)

        return l.load_item()

        """yield{"name":Name,
                "price":Price,
                'Url':link,
                'Img':Img}
                """
