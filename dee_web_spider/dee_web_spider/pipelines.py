# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging

from pymysql import cursors
from twisted.enterprise import adbapi
import copy


class DeeWebSpiderPipeline:
    def __init__(self, db_pool):
        self.db_pool = db_pool

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
        sql_item = {
            "postId": item["url"],
            "recruitPostId": item["title"],
            "recruitPostName": item["content"],
            "countryName": item["sub_time"],
            "locationName": item["keywords"]
        }
        logging.warning(sql_item)
        # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
        async_item = copy.deepcopy(sql_item)

        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, async_item)
        query.addErrback(self.handle_error, sql_item, spider)
        return sql_item

    def insert_into(self, cursor, item):
        sql = "INSERT INTO tencent (" \
              "postId,recruitPostId,recruitPostName,countryName,locationName,categoryName,lastUpdateTime) VALUES (" \
              "'{}','{}','{}','{}','{}','{}','{}')".format(item["url"], item["title"], item["content"], item["sub_time"], item["keywords"])
        cursor.execute(sql)

    def handle_error(self, failure, item, spider):
        print("failure", failure)
