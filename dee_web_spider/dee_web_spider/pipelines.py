# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import copy
import hashlib
from datetime import datetime
from pymysql import cursors
from twisted.enterprise import adbapi


class DeeWebSpiderPipeline:
    def __init__(self, db_pool):
        # self.db_pool = db_pool
        pass

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            use_unicode=True,
            cursorclass=cursors.DictCursor
        )
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(db_pool)

    def process_item(self, item, spider):
        # 不同的爬虫使用不同的关键字
        if spider.name == 'dee_web_jiangsu' or spider.name == 'dee_web_zhejiang':
            setting_keyword_list = spider.settings['KEYWORDS_B']
        elif spider.name == 'mee_web':
            setting_keyword_list = spider.settings['KEYWORDS_M']
        else:
            setting_keyword_list = []

        keywords = []
        for setting_keyword in setting_keyword_list:
            if setting_keyword in item["title"]:
                keywords.append({
                    "kid": hashlib.md5((item["url"] + setting_keyword).encode('utf-8')).hexdigest(),
                    "kw": setting_keyword
                })
                continue
            if setting_keyword in item["content"]:
                keywords.append({
                    "kid": hashlib.md5((item["url"] + setting_keyword).encode('utf-8')).hexdigest(),
                    "kw": setting_keyword
                })

        # 只有匹配上关键字的条目才会被保存
        if len(keywords) > 1:
            sql_item = {
                "url": item["url"],
                "title": item["title"],
                "content": item["content"],
                "sub_time": item["sub_time"],
                "grab_time": item["grab_time"],
                "source_name": spider.name,
                "keywords": keywords,
                "id": hashlib.md5(item["url"].encode('utf-8')).hexdigest(),
                "source_type": '01',
                "bus_status": 0,
                "create_time": datetime.now().strftime('%Y-%m-%d'),
                "create_by": 'dee_web_spider',
                "sign_type": 'PRI',
                "delete_flag": '0',
                "data_type": 'D',
                "department_name": spider.department_name,
                "region_code": spider.region_code
            }
            print(sql_item)
            logging.warning(sql_item)
            # 对象拷贝，深拷贝，这里是解决数据重复问题！！！
            async_item = copy.deepcopy(sql_item)

            # 把要执行的sql放入连接池
            # 保存新闻条目
            insert_info = self.db_pool.runInteraction(self.insert_info, async_item)
            insert_info.addErrback(self.handle_error, sql_item, spider)
            # 保存标签
            insert_sign = self.db_pool.runInteraction(self.insert_sign, async_item)
            insert_sign.addErrback(self.handle_error, sql_item, spider)
            return sql_item

    def insert_info(self, cursor, item):
        sql = "REPLACE INTO crm_sale_pub_information (" \
              "id, infoTitle, infoDate, grapDate, grapUser, sourceType, sourceName, infoUrl, " \
              "busiStatus, createTime, createBy, deleteFlag) " \
              "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            item["id"], item["title"], item["sub_time"], item["grab_time"], item['source_name'], item['source_type'],
            item['source_name'], item['url'], item["bus_status"], item["create_time"], item["create_by"], item["delete_flag"])
        cursor.execute(sql)

    def insert_sign(self, cursor, item):
        for keyword in item['keywords']:
            sql = "REPLACE INTO system_data_sign (id, signType, dataName, parentId, " \
                  "busiStatus, createTime, createBy, deleteFlag, dataType) VALUES (" \
                  "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
                keyword['kid'], item['sign_type'], keyword['kw'], item['id'],
                item['bus_status'], item['create_time'], item['create_by'], item['delete_flag'], item['data_type'])
            cursor.execute(sql)

    def handle_error(self, failure, item, spider):
        print("failure", failure)
