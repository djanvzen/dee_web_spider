import scrapy


class DeeWebJiangsuSpider(scrapy.Spider):
    name = "dee_web_jiangsu"
    allowed_domains = ["sthjt.jiangsu.gov.cn"]
    start_urls = [
        "http://sthjt.jiangsu.gov.cn/col/col83545",
        # "http://sthjt.jiangsu.gov.cn/col/col83554/index.html"
    ]

    def parse(self, response):
        print(response.text)
        # article_title = response.xpath("//[@class='default_pgContainer']/li/a/text()")
        # print(article_title)
