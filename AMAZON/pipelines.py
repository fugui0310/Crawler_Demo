# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from pymongo import MongoClient


class MongoPipeline(object):
    def __init__(self,db,collection,host,port,user,pwd):
        self.db=db
        self.collection=collection
        self.host=host
        self.port=port
        self.user=user
        self.pwd=pwd

    @classmethod
    def from_crawler(cls, crawler):
        """
        Scrapy会先通过getattr判断我们是否自定义了from_crawler,有则调它来完
        成实例化
        """
        db = crawler.settings.get('DB')
        collection = crawler.settings.get('COLLECTION')
        host = crawler.settings.get('HOST')
        port = crawler.settings.getint('PORT')
        user = crawler.settings.get('USER')
        pwd = crawler.settings.get('PWD')

        return cls(db,collection,host,port,user,pwd)

    def open_spider(self,spider):
        """
        爬虫刚启动时执行一次
        """
        print('==============>爬虫程序刚刚启动')
        self.client = MongoClient("mongodb://%s:%s@%s:%s" %(
            self.user,
            self.pwd,
            self.host,
            self.port
        ))

    def close_spider(self,spider):
        """
        爬虫关闭时执行一次
        """
        print('==============>爬虫程序运行完毕')
        self.client.close()

    def process_item(self, item, spider):
        # 操作并进行持久化

        # return表示会被后续的pipeline继续处理
        d=dict(item)
        if all(d.values()):
            self.client[self.db][self.collection].save(d)

        return item

        # 表示将item丢弃，不会被后续pipeline处理
        # raise DropItem()


class FilePipeline(object):
    def __init__(self, file_path):
        self.file_path=file_path

    @classmethod
    def from_crawler(cls, crawler):
        """
        Scrapy会先通过getattr判断我们是否自定义了from_crawler,有则调它来完
        成实例化
        """
        file_path = crawler.settings.get('FILE_PATH')


        return cls(file_path)

    def open_spider(self, spider):
        """
        爬虫刚启动时执行一次
        """
        print('==============>爬虫程序刚刚启动')
        self.fileobj=open(self.file_path,'w',encoding='utf-8')

    def close_spider(self, spider):
        """
        爬虫关闭时执行一次
        """
        print('==============>爬虫程序运行完毕')
        self.fileobj.close()

    def process_item(self, item, spider):
        # 操作并进行持久化

        # return表示会被后续的pipeline继续处理
        d = dict(item)
        if all(d.values()):
            self.fileobj.write(r"%s\n" %str(d))

        return item

        # 表示将item丢弃，不会被后续pipeline处理
        # raise DropItem()