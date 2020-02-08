import json

import scrapy
import scrapy.exceptions
from scrapy.loader import ItemLoader

from ..items import Product
from ..pipelines import ProcessProduct


class CharlotteCrawler(scrapy.Spider):
    name = 'charlotte'
    allowed_domains = ['pelletteriacharlotte.it']
    pipeline = {ProcessProduct}

    def __init__(self, **kwargs):
        with open('pelletteria-charlotte.txt') as f:
            self.start_urls = f.readlines()
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_item)

    def parse_item(self, response):
        product_data = json.loads(
            response.xpath('//script[contains(., "https://schema.org/")]/text()').extract_first()
        )
        item = ItemLoader(item=Product(), response=response)
        item.add_value('url', response.url)
        item.add_value('name', product_data['name'])
        item.add_value('price', product_data['Offers']['price'])
        item.add_value('currency', 'EUR')
        item.add_css('description', 'div[data-hook="info-section-description"] *::text')
        item.add_value('sku', product_data['sku'])
        item.add_value('image_urls', [product_data['image']['contentUrl']])
        yield item.load_item()
