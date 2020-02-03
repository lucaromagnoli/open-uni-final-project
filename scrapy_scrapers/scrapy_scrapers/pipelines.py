# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from scrapy.exporters import CsvItemExporter


class TSVItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['encoding'] = 'utf-16'
        kwargs['delimiter'] = '\t'
        super(TSVItemExporter, self).__init__(*args, **kwargs)


class CsvPipeline(object):
    def __init__(self):
        self.file = None
        self.exporter = None

    def open_spider(self, spider):
        self.file = open(f'{spider.name}_{spider.category}_{datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M")}.csv', 'wb')
        self.exporter = TSVItemExporter(self.file, encoding='utf-16')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
