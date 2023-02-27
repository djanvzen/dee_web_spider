from abc import ABC
import re
import scrapy
from scrapy.spiders import XMLFeedSpider


class DeeWebJiangsuSpider(XMLFeedSpider, ABC):
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
            # 用正则解析url 我们去里面获取时间标题和内容
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
        title = response.xpath("//h1[@class='title']/text()").extract_first()
        content = response.xpath("//div[@class='zoom']//text()").extract_first()
        sub_time = response.xpath("//div[@class='sub-title']/span/text()").extract_first()
        item_article = {
            "title": title,
            "content": content,
            "sub_time": sub_time
        }
        print(item_article)


