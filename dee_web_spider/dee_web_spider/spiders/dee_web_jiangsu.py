# -*- coding: utf-8 -*-

import re
from abc import ABC
from datetime import datetime
import scrapy


class DeeWebJiangsuSpider(scrapy.spiders.XMLFeedSpider, ABC):
    name = "dee_web_jiangsu"
    allowed_domains = ["sthjt.jiangsu.gov.cn"]
    start_urls = [
        "http://sthjt.jiangsu.gov.cn/col/col83545",
        "http://sthjt.jiangsu.gov.cn/col/col83554"
    ]

    itertag = 'recordset'

    def parse_node(self, response, selector):
        source_li = selector.css("recordset record ::text").getall()
        for li in source_li:
            relative_url = re.search(r'href=\"(.*\.html)\"', li).group(1)
            article_url = "http://sthjt.jiangsu.gov.cn" + relative_url
            yield scrapy.Request(
                                    article_url,
                                    callback=self.parse,  # 处理响应的回调函数。
                                    # method="GET",  # 默认GET
                                    # headers={},  # 这里的headers不能存放cookie信息。 默认None
                                    # cookies={},  # 默认None
                                    # meta = {"mydata":item},  # 可以在不同的回调函数中传递数据
                                    # dont_filter=False    # 默认False。 (scrapy默认过滤重复的url)
                                )

    def parse(self, response):
        url = response.request.url
        title = response.xpath("//h1[@class='title']/text()").extract_first()
        content = response.xpath("//div[@class='zoom']").xpath('string(.)').extract_first()
        sub_time_str = response.xpath("//div[@class='sub-title']/span/text()").extract_first()

        if '发布时间：' in sub_time_str:
            sub_time = datetime.strptime(sub_time_str.replace('发布时间：', ''), '%Y-%m-%d %H:%M')
        else:
            sub_time = None

        item_article = {
            "url": url,
            "title": title,
            "content": content,
            "sub_time": sub_time
        }
        yield item_article
