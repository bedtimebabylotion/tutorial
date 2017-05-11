# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals

from twisted.enterprise import adbapi
import datetime
import logging
import MySQLdb.cursors
from scrapy.exceptions import DropItem
from tutorial.items import TutorialItem

class TutorialPipeline(object):
    def __init__(self):
        try:
            self.conn = MySQLdb.connect(user='root', passwd='1234', db='testDB', host='localhost', charset='utf8', use_unicode=True)
            self.cursor = self.conn.cursor()
        except MySQLdb.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

    def process_item(self, item, spider):
        add_data = ("INSERT INTO parseTest "
                    "(co_id, article_date, content) "
                    "VALUES (%s, %s, %s)")
        try:
            self.cursor.execute(add_data, (str(item['cp']).encode('utf-8'),
                                      item['aDate'].encode('utf-8'),
                                      item['aTxt'].encode('utf-8')))
            self.conn.commit()
        except MySQLdb.Error as e :
            print("Error %d: %s" %(e.args[0], e.args[1]))
            return item

#    def spider_closed(self, spider):
