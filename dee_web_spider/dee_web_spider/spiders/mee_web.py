# -*- coding: utf-8 -*-


import scrapy
from datetime import datetime


class MeeWebSpider(scrapy.Spider):
    name = "mee_web"
    department_name = "生态环境部"
    region_code = "110000"
    allowed_domains = ["mee.gov.cn"]
    start_urls = [
        # 中央有关文件
        "https://www.mee.gov.cn/govsearch/wenjiankujs.jsp?orderby=date&Stype=2&type=1&channelid=29030&keyword=",
        # 国务院有关文件
        "https://www.mee.gov.cn/govsearch/wenjiankujs.jsp?orderby=date&Stype=2&type=1&channelid=29031&keyword=",
        # 部文件
        "https://www.mee.gov.cn/govsearch/wenjiankujs.jsp?orderby=date&Stype=2&type=1&channelid=29032&keyword=",
        # 办公厅文件
        "https://www.mee.gov.cn/govsearch/wenjiankujs.jsp?orderby=date&Stype=2&type=1&channelid=29037&keyword="
    ]

    def parse(self, response):
        article_url_list = response.xpath("//td/a[@target='_blank']/@href").extract()
        for article_url in article_url_list:
            yield scrapy.Request(
                article_url,
                callback=self.parse_article
            )

    def parse_article(self, response):
        # 解析文章
        url = response.request.url
        title = response.xpath("//div/h1[@class='cjcs_phone_title']/text()").extract_first()
        content = response.xpath("//div[@class='Custom_UnionStyle']").xpath('string(.)').extract_first()
        sub_time_str = response.xpath('//div[@class="wjkFontBox"]/em[1]/text()').extract_first()

        if '发布时间：' in sub_time_str:
            # sub_time = datetime.strptime(sub_time_str.replace('发布时间：', ''), '%Y-%m-%d %H:%M')
            sub_time = sub_time_str.replace('发布时间：', '')
        else:
            sub_time = None

        item = {
            "url": url,
            "title": title,
            "content": content,
            "sub_time": sub_time,
            "grab_time": datetime.now().strftime('%Y-%m-%d')
        }
        # item数据类型扔给pipline处理
        yield item
