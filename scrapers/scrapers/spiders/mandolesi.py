from babel.numbers import parse_decimal

from extruct.w3cmicrodata import MicrodataExtractor
import scrapy
import scrapy.exceptions
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose

from ..items import Product
from ..pipelines import ProcessProduct


def pair_items(items):
    items = iter(items)
    return {k: v for k, v in list(zip(items, items))}


def parse_description(items):
    desc = "".join([x.strip() for x in items])
    return desc.replace('\xa0', '').strip()


class MandolesiLoader(ItemLoader):
    dimensions_out = Compose(pair_items)
    description_in = Compose(parse_description)


class Crawler(scrapy.Spider):
    name = 'mandolesi'
    mde = MicrodataExtractor()
    pipeline = {ProcessProduct}

    def __init__(self, **kwargs):
        self.start_urls = [f'https://www.masciamandolesi.com/en/shop/page/{i}/' for i in range(1, 4)]
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_shop)

    def parse_shop(self, response):
        for url in response.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link::attr(href)').extract():
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        item = MandolesiLoader(item=Product(), response=response)
        item.add_value('url', response.url)
        item.add_css('name', 'h1.product_title.entry-title ::text')
        item.add_css('price', 'div.summary.entry-summary span.woocommerce-Price-amount.amount::text')
        item.add_value('currency', 'EUR')
        item.add_css('description', 'div.woocommerce-product-details__short-description *::text')
        table = item.nested_css('#tab-additional_information')
        table.add_xpath('color', '//table/tr[2]/td/p/text()')
        table.add_xpath('material', '//table/tr[3]/td/p/text()')
        table.add_xpath('dimensions', '//table/tr[4]/th/text()')
        table.add_xpath('dimensions', '//table/tr[4]/td/p/text()')
        table.add_xpath('dimensions', '//table/tr[5]/th/text()')
        table.add_xpath('dimensions', '//table/tr[5]/td/p/text()')
        item.add_css('image_urls', 'figure.woocommerce-product-gallery__wrapper img::attr(data-src)')
        yield item.load_item()
