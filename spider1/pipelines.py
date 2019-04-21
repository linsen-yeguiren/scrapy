# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb as pymysql
import spider1.settings as settings


class Spider1Pipeline(object):
    def process_item(self, item, spider):
        try:
            # 插入数据
            print("==================================")
            print(item['price'])
            print(item['name'])
            print(item['dos'])
            print(item['number'])
            self.cursor.execute(
                """select * from doubanmovie where name = %s""",
                item['name'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()

            # 重复
            if repetition:
                pass

            self.cursor.execute("insert into tuniuNew(name, price, dos, number )value (%s, %s, %s, %s)", (item['name'],item['price'],item['dos'],item['number'],))
            # self.cursor.execute("insert into tuniu(name, price, dos, number )value (%s, %s, %s, %s)",
            #                     ('price', '50', '50', '10',))
            # 提交sql语句
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
        return item

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor();

