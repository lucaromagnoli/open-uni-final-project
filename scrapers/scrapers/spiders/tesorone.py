import json
import re

from extruct.w3cmicrodata import MicrodataExtractor
import scrapy
import scrapy.exceptions
from scrapy.loader import ItemLoader

from ..items import Product
from ..pipelines import ProcessProduct


class TesoroneCrawler(scrapy.Spider):
    name = 'tesorone'
    allowed_domains = ['tesorone.it']
    mde = MicrodataExtractor()
    pipeline = {ProcessProduct}
    filename = 'tesorone'

    def __init__(self, **kwargs):
        self.start_urls = [f'https://www.tesorone.it/shop.html?p={i}' for i in range(1, 10)]
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_shop)

    def parse_shop(self, response):
        for url in response.css('li.product-item a::attr(href)').extract():
            if url != '#':
                yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        schema_data = self.mde.extract(response.body)[0]
        image_data = json.loads(
            response.xpath("//script[contains(., 'mage/gallery/gallery')]/text()").extract_first().replace('\n', '')
        )
        item = ItemLoader(item=Product(), response=response)
        item.add_value('url', response.url)
        item.add_value('name', schema_data['properties']['name'])
        item.add_css('price', 'meta[property="product:price:amount"]::attr(content)')
        item.add_value('currency', 'EUR')
        item.add_value('description', schema_data['properties']['description'].replace('\n', ''))
        item.add_value('sku', schema_data['properties']['sku'])
        item.add_value(
            'image_urls',
            [image_data['[data-gallery-role=gallery-placeholder]']['mage/gallery/gallery']['data'][0]['full']]
        )
        yield item.load_item()
