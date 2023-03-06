# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DeeWebSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 目前只要解析url，文章title，文章内容，发布时间，抓取时间
    ulr = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    sub_time = scrapy.Field()
    grab_time = scrapy.Field()
