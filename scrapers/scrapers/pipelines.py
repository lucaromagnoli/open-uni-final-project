# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import functools
import logging
import hashlib
import os

from scrapy.exporters import CsvItemExporter


def check_spider_pipeline(process_item_method):
    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        # message template for debugging
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)

        # if class is in the spider's pipeline, then use the
        # process_item method normally.
        if self.__class__ in spider.pipeline:
            spider.log(msg % 'executing', level=logging.DEBUG)
            return process_item_method(self, item, spider)

        # otherwise, just return the untouched item (skip this step in
        # the pipeline)
        else:
            spider.log(msg % 'skipping', level=logging.DEBUG)
            return item
    return wrapper


class TSVItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['encoding'] = 'utf-16'
        kwargs['delimiter'] = '\t'
        super(TSVItemExporter, self).__init__(*args, **kwargs)


class CsvPipeline(object):
    data_dir = '/Users/luca.romagnoli/Dropbox/RossiRei/scraped-data'

    def __init__(self):
        self.file = None
        self.exporter = None

    def open_spider(self, spider):
        filepath = os.path.join(
            self.data_dir,
            f'{spider.filename}_{datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M")}.csv'
        )
        self.file = open(filepath, 'wb')
        self.exporter = TSVItemExporter(self.file, encoding='utf-16')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ProcessProduct(object):
    @check_spider_pipeline
    def process_item(self, item, spider):
        item['unique_id'] = hashlib.md5(item['url'].encode('utf-8')).hexdigest()
        return item
