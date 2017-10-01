# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from datetime import datetime


class GjirafaComPipeline(object):
    def __init__(self):
        self.date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.file = csv.writer(open('info_%s.csv' % self.date, 'w'), quoting=csv.QUOTE_MINIMAL)
        self.file.writerow(
            ['E-Mail Address', 'Phone Number', 'Location']
        )

    def process_item(self, item, spider):
        self.file.writerow([item['email'], item['phone'], item['location']])
        return item
