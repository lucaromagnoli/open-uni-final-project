import re

from extruct.w3cmicrodata import MicrodataExtractor
import scrapy
import scrapy.exceptions

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
        impage_pattern = re.compile(
            r'(https:\\/\\/www.tesorone.it\\/pub\\/media\\/catalog\\/product\\/cache\\/\\/960x720\\/.*.jpg)'
        )
        try:
            price = schema_data['properties']['offers'][0]['properties']['price']
            currency = schema_data['properties']['offers'][0]['properties']['priceCurrency']
        except KeyError:
            price = schema_data['properties']['offers']['properties']['price']
            currency = schema_data['properties']['offers']['properties']['priceCurrency']
        yield Product(
            url=response.url,
            name=schema_data['properties']['name'],
            description=schema_data['properties']['description'],
            price=price,
            currency=currency,
            sku=schema_data['properties']['sku'],
            image_urls=[
                re.search(impage_pattern, response.text).group(1).replace('\\', '')
            ]
        )
