import scrapy


class MeeWebSpider(scrapy.Spider):
    name = "mee_web"
    allowed_domains = ["mee.gov.cn"]
    start_urls = ["http://mee.gov.cn/"]

    def parse(self, response):
        pass
