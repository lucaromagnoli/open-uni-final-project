import re

import scrapy
import scrapy.exceptions
from scrapy.loader import ItemLoader

from ..items import Product
from ..pipelines import ProcessProduct


class Crawler(scrapy.Spider):
    name = 'verniani'
    pipeline = {ProcessProduct}

    def __init__(self, **kwargs):
        self.start_urls = ['http://www.vernianibags.com/negozio/']
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_sections)

    def parse_sections(self, response):
        for url in response.css('a.vc_single_image-wrapper.vc_box_border_grey ::attr(href)').extract():
            yield scrapy.Request(url, self.parse_collection)

    def parse_collection(self, response):
        for url in response.css('div.item-wrapper a::attr(href)').extract():
            if url != '#':
                yield scrapy.Request(url, self.parse_item)

    def parse_item(self, response):
        description = (
            "".join(response.css('div[itemprop="description"] *::text').extract())
                .replace('\n', '')
                .replace('\t', '')
                .replace('–', '')
        )

        def get_dimensions():
            match = re.search(
                'Dimensioni: larghezza ([0-9,]+) cm, altezza ([0-9,]+) cm, profondità ([0-9,]+) cm',
                description
            )
            dimensions = [match.group(i).replace(',', '.') for i in range(1, 4)]
            return " x ".join(dimensions)

        def get_color():
            match = re.search(
                'col. (.*) Dimensioni',
                description
            )
            return ", ".join(match.group(1).split(' e '))

        def get_material():
            match = re.search(
                'Composizione:(.*)',
                description
            )
            return match.group(1).replace('\xa0', '').strip()

        item = ItemLoader(item=Product(), response=response)
        item.add_value('url', response.url)
        item.add_css('name', 'h2.product_title entry-title ::text')
        item.add_css('price', 'p.price span.woocommerce-Price-amount.amount::text')
        item.add_value('currency', 'EUR')
        item.add_value('description', description)
        item.add_css('sku', 'span.sku::text')
        item.add_value('dimensions', get_dimensions())
        item.add_value('color', get_color())
        item.add_value('material', get_material())
        item.add_value(
            'image_urls',
            [i.split(',')[0].split()[0] for i in response.css('a[itemprop="image"] ::attr(srcset)').extract()]
        )
        yield item.load_item()

