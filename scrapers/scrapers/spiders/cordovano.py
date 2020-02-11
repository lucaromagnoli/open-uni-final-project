import json

import scrapy
import scrapy.exceptions
from scrapy.loader import ItemLoader

from ..items import Product
from ..pipelines import ProcessProduct


class Crawler(scrapy.Spider):
    name = 'cordovano'
    pipeline = {ProcessProduct}

    def __init__(self, **kwargs):
        self.start_urls = ['https://www.cordovano.it/shop/']
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_shop)

    def parse_shop(self, response):
        for url in response.css('div.product-header a::attr(href)').extract():
            if url.startswith(self.start_urls[0]):
                yield scrapy.Request(url, self.parse_item)
        next_url = response.xpath('//*[@id="primary"]/nav/ul/li[4]/a//@href').extract_first()
        if next_url:
            yield scrapy.Request(next_url, self.parse_shop)

    def parse_item(self, response):
        product_data = json.loads(response.xpath('//script[contains(., "@graph")]//text()').get())['@graph'][1]
        try:
            price = product_data['offers'][0]['price']
        except KeyError:
            price = product_data['offers'][0]['highPrice']
        image_data = json.loads(
            response.xpath('//script[contains(., "WOOSVIDATA")]//text()').get().replace('\n', '').replace(
                '/* <![CDATA[ */var WOOSVIDATA = ', '').replace(';/* ]]> */', ''))
        item = ItemLoader(item=Product(), response=response)
        item.add_value('url', response.url)
        item.add_value('name', product_data['name'])
        item.add_value('price', price)
        item.add_value('currency', 'EUR')
        item.add_value('description', product_data['description'])
        item.add_value('sku', product_data['sku'])
        item.add_value(
            'image_urls',
            [image['fullimg']['src'] for image in image_data['gallery']['thumbs']]
        )
        yield item.load_item()

