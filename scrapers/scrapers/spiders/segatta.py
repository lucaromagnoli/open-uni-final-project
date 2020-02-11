import json

import scrapy
import scrapy.exceptions
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from ..items import Product
from ..pipelines import ProcessProduct


class Crawler(scrapy.Spider):
    name = 'segatta'
    pipeline = {ProcessProduct}

    def __init__(self, **kwargs):
        self.start_urls = ['http://www.giannisegatta.it/']
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_menu)

    def parse_menu(self, response):
        for url in response.css('li.menu-item a::attr(href)').extract():
            if url.startswith(self.start_urls[0]):
                print(0)
                yield scrapy.Request(url, self.parse_item)

    def parse_item(self, response):
        print(0)
        try:
            for elem in response.css('div.tile'):
                name_elem = elem.css('ul.crp-light-gallery ::attr(data-sub-html)').get()
                name = Selector(name_elem)
                item = ItemLoader(item=Product(), response=response)
                item.add_value('image_urls', [elem.css('img ::attr(src)').get_first()])
                item.add_value('name', name)
                yield item.load_item()
        except Exception:
            pass

