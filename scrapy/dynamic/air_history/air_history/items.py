# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AirHistoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data = scrapy.Field() #日期
    city = scrapy.Field() #城市
    aqi = scrapy.Field() #空气质量指数
    level = scrapy.Field() #空气质量等级
    pm2_5 = scrapy.Field() #pm2.5
    pm10 = scrapy.Field() #pm10
    so2 = scrapy.Field() #so2
    co = scrapy.Field() #co
    no2 = scrapy.Field() #no2
    o3 = scrapy.Field()  #o3
