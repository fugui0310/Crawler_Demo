# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from AMAZON.items import AmazonItem

# from scrapy.http import Request
# from scrapy.spiders import Spider,CrawlSpider,XMLFeedSpider,CSVFeedSpider,SitemapSpider
# from scrapy.selector import HtmlXPathSelector #response.xpath

# print(Spider is scrapy.Spider)
# print(XMLFeedSpider is scrapy.XMLFeedSpider)
# print(Request is scrapy.Request)
# from scrapy.dupefilter import RFPDupeFilter
# from scrapy.core.scheduler import Scheduler

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['http://www.amazon.cn/',]

    #self.settings.get()
    custom_settings = {
        "BOT_NAME" : 'EGON_AMAZON',
        'REQUSET_HEADERS':{

        },
    }

    def __init__(self,keyword,*args,**kwargs):
        super(AmazonSpider,self).__init__(*args,**kwargs)
        self.keyword=keyword

    def start_requests(self):
        # for start_url in start_url:
        # return [scrapy.Request('https://www.amazon.cn/s/ref=nb_sb_noss_1/461-4093573-7508641?field-keywords=iphone8',
        #                      callback=self.parse,
        #                      dont_filter=True,
        #                      ),
        #         scrapy.Request('https://www.amazon.cn/s/ref=nb_sb_noss_1/461-4093573-7508641?field-keywords=iphone8',
        #                        callback=self.parse,
        #                        dont_filter=True,
        #                        ),
        #         ]

        # yield scrapy.Request('https://www.amazon.cn/s/ref=nb_sb_noss_1/461-4093573-7508641?field-keywords=iphone8',
        #                      callback=self.parse,
        #                      dont_filter=False,
        #                      )
        #
        # yield scrapy.Request('https://www.amazon.cn/s/ref=nb_sb_noss_1/461-4093573-7508641?field-keywords=iphone8',
        #                      callback=self.parse,
        #                      dont_filter=False,
        #                      )
        #
        # yield scrapy.Request('https://www.amazon.cn/s/ref=nb_sb_noss_1/461-4093573-7508641?field-keywords=iphone8',
        #                      callback=self.parse,
        #                      dont_filter=False,
        #                      )

        url='https://www.amazon.cn/s/ref=nb_sb_noss_1/461-4093573-7508641?'
        url+=urlencode({"field-keywords" : self.keyword})
        print(url)
        yield scrapy.Request(url,
                             callback=self.parse_index,
                             dont_filter=False,
                             )

    def parse_index(self, response):
        # print('============>',self.settings['NEWSPIDER_MODULE'])
        # print('============>',self.settings['BOT_NAME'])
        # print('============>',self.settings['REQUSET_HEADERS'])
        # self.logger.warn('============>%s' %self.settings['REQUSET_HEADERS'])

        # print('======>',response.request.meta,response.meta)
        # print('======>',response.request.url,response.url)

        # print('%s 解析结果：%s' %(response.url,len(response.body)))

        detail_urls=response.xpath('//*[contains(@id,"result_")]/div/div[3]/div[1]/a/@href').extract()
        # print(detail_urls)
        for detail_url in detail_urls:
            yield scrapy.Request(url=detail_url,
                                 callback=self.parse_detail
                                 )

        next_url=response.urljoin(response.xpath('//*[@id="pagnNextLink"]/@href').extract_first())
        # print(next_url)
        yield scrapy.Request(url=next_url,
                             callback=self.parse_index
                                 )

    def parse_detail(self,response):
        # print('%s 详情页解析结果：%s' % (response.url, len(response.body)))
        name=response.xpath('//*[@id="productTitle"]/text()').extract_first().strip()
        price=response.xpath('//*[@id="price"]//*[@class="a-size-medium a-color-price"]/text()').extract_first()
        delivery_method=''.join(response.xpath('//*[@id="ddmMerchantMessage"]//text()').extract())
        print(response.url)
        print(name)
        print(price)
        print(delivery_method)
        item=AmazonItem()
        item["name"]=name
        item["price"]=price
        item["delivery_method"]=delivery_method
        return item


    def close(spider, reason):
        print('结束啦')


