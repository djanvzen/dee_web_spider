# -*- coding: utf-8 -*-

import scrapy
from datetime import datetime


class DeeWebZhejiangSpider(scrapy.Spider):
    name = "dee_web_zhejiang"
    department_name = "浙江省生态环境厅"
    region_code = "330000"
    allowed_domains = ["sthjt.zj.gov.cn"]
    start_urls = [
        # 规划信息-专项规划
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=K001C001&jdid=1756",
        # 规划信息-空间规划
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=K001A011&jdid=1756",
        # 政府采购
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=AH001A001&jdid=1756",
        # 重大项目-重大项目推进情况
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=AZ001B001&jdid=1756",
        # 重大决策
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=SB122sb232&jdid=1756",
        # 政策文件及解读-上级文件
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=B001A012&jdid=1756",
        # 政策文件及解读-地方性法规规章
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=B001A013&jdid=1756",
        # 政策文件及解读-政府规章
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=B001A014&jdid=1756",
        # 政策文件及解读-行政规范性文件
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=B001G001&jdid=1756",
        # 政策文件及解读-其他文件
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=B001AC001&jdid=1756",
        # 政策文件及解读-政策解读
        "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?divid=div1229106886&infotypeId=B001A011&jdid=1756"
    ]

    def parse(self, response):
        article_url_list = response.xpath("//td/a[@class='bt_link' and not(@syh)]/@href").extract()
        for article_url in article_url_list:
            yield scrapy.Request(
                article_url,
                callback=self.parse_article
            )

    def parse_article(self, response):
        # 解析文章
        url = response.request.url
        title = response.xpath("//tr/td[@class='title']/text()").extract_first()
        content = response.xpath("//div[@id='zoom']").xpath('string(.)').extract_first()
        sub_time_str = response.xpath("//tr/td/span[@style='padding-left:25px;']/text()").extract_first()

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
