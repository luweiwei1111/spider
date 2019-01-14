# -*- coding: utf-8 -*-
import scrapy
from air_history.items import AirHistoryItem

class AreaSpiderSpider(scrapy.Spider):
    name = 'area_spider'
    allowed_domains = ['aqistudy.cn']  # 爬取的域名，不会超出这个顶级域名
    base_url = "https://www.aqistudy.cn/historydata/"
    start_urls = [base_url]

    def parse(self, response):
        print('爬取城市信息....')
        url_list = response.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li/a/@href").extract()  # 全部链接
        city_list = response.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li/a/text()").extract()  # 城市名称
        for url, city in zip(url_list, city_list):
            url = self.base_url + url
            yield scrapy.Request(url=url, callback=self.parse_month, meta={'city': city})

    def parse_month(self, response):
        print('爬取{}月份...'.format(response.meta['city']))
        url_list = response.xpath('//tbody/tr/td/a/@href').extract()
        for url in url_list:
            url = self.base_url + url
            yield scrapy.Request(url=url, callback=self.parse_day, meta={'city': response.meta['city']})

    def parse_day(self, response):
        print('爬取最终数据...')
        item = AirHistoryItem()
        node_list = response.xpath('//tr')
        node_list.pop(0)  # 去除第一行标题栏
        for node in node_list:
            item['data'] = node.xpath('./td[1]/text()').extract_first()
            item['city'] = response.meta['city']
            item['aqi'] = node.xpath('./td[2]/text()').extract_first()
            item['level'] = node.xpath('./td[3]/text()').extract_first()
            item['pm2_5'] = node.xpath('./td[4]/text()').extract_first()
            item['pm10'] = node.xpath('./td[5]/text()').extract_first()
            item['so2'] = node.xpath('./td[6]/text()').extract_first()
            item['co'] = node.xpath('./td[7]/text()').extract_first()
            item['no2'] = node.xpath('./td[8]/text()').extract_first()
            item['o3'] = node.xpath('./td[9]/text()').extract_first()
            yield item