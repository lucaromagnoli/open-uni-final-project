import json

import scrapy
import scrapy.exceptions
from scrapy.loader import ItemLoader

from ..items import Product
from ..pipelines import ProcessProduct


class CuoieriaCrawler(scrapy.Spider):
    name = 'cuoieria-fiorentina'
    pipeline = {ProcessProduct}

    def __init__(self, **kwargs):
        with open('cuoieriafiorentina.txt') as f:
            self.start_urls = f.readlines()
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_item)

    def parse_item(self, response):
        product_data = json.loads(
            response.xpath('//script[contains(., "http:\/\/schema.org")]/text()').extract()[1]
        )
        item = ItemLoader(item=Product(), response=response)
        item.add_value('url', response.url)
        item.add_value('name', product_data['name'])
        item.add_value('price', product_data['offers'][1]['price'])
        item.add_value('currency', 'EUR')
        item.add_value('description', product_data['description'])
        item.add_value('sku', product_data['sku'])
        item.add_value(
            'image_urls',
            [response.xpath('.//div[starts-with(@id, "item-0")]//img/@src').extract_first()]
        )
        yield item.load_item()
