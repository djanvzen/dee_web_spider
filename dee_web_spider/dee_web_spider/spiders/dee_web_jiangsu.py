import scrapy


class DeeWebJiangsuSpider(scrapy.Spider):
    name = "dee_web_jiangsu"
    allowed_domains = ["sthjt.jiangsu.gov.cn"]
    start_urls = [
        "http://sthjt.jiangsu.gov.cn/col/col83545",
        # "http://sthjt.jiangsu.gov.cn/col/col83554/index.html"
    ]

    def parse(self, response):
        html_tree = response.text.replace('<![CDATA[', '')
        html_sel = scrapy.Selector(text=html_tree)
        print(html_tree)
        # article_title = html_sel.xpath("//recordset/record/")
        # print(article_title)
