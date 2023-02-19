import scrapy


class DeeWebZhejiangSpider(scrapy.Spider):
    name = "dee_web_zhejiang"
    allowed_domains = ["sthjt.zj.gov.cn"]
    start_urls = ["http://sthjt.zj.gov.cn/"]

    def parse(self, response):
        pass
