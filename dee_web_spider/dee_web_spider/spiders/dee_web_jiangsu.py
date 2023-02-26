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
        source_li = selector.css("recordset record::text").getall()
        item = {}
        for li in source_li:
            # 使用正则提取 名称 时间 和 地址
            pattern = re.search(r'<a href="(.*?)">(.*?)</a>.*<span>(.*?)</span>', li)
            title_name = pattern.group(2)
            title_date = pattern.group(3)
            title_url = "http://sthjt.jiangsu.gov.cn" + str(pattern.group(1))

            yield scrapy.Request(
                                    title_url,
                                    callback=self.parse_article,  # 处理响应的回调函数。
                                    # method="GET",  # 默认GET
                                    # headers={},  # 这里的headers不能存放cookie信息。 默认None
                                    # cookies={},  # 默认None
                                    # meta = {"mydata":item},  # 可以在不同的回调函数中传递数据
                                    # dont_filter=False    # 默认False。 (scrapy默认过滤重复的url)
                                )

    def parse_article(self, response):
        pass

    # def parse(self, response):
    #     html_tree = response.text.replace('<![CDATA[', '').replace(']]>', '')
    #     html_sel = scrapy.Selector(text=html_tree)
    #     recordset = html_sel.xpath("//recordset")
    #     print(recordset)
        # for record in recordset:
        #     aa = record.xpath("./record/li/a/text()")
        #     print(aa)
        # print(article_title)
