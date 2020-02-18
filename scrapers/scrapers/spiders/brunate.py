from itertools import chain


import scrapy
import scrapy.exceptions
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose

from ..items import Product
from ..pipelines import ProcessProduct


class CustomLoader(ItemLoader):
    dimensions_in = MapCompose(lambda x: x.strip(), lambda x: [{'heel': x}])


class Crawler(scrapy.Spider):
    name = 'brunate'
    pipeline = {ProcessProduct}
    filename = 'tesorone'

    def __init__(self, **kwargs):
        self.start_urls = [f'https://www.brunate.com/en/shoes/?p={i}' for i in range(1, 6)]
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_shop)

    def parse_shop(self, response):
        for url in response.css('div.bru-product__info a::attr(href)').extract():
            if url != '#':
                yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        description = response.css('p.bru-product-detail__description-txt--body ::text').extract()[1].strip()
        material = [
            i.strip() for i in response.css(
                'li.base-info--entry.entry--suppliername.bru-product-detail__buybox-listitem ::text'
            ).extract() if i.strip()
        ]
        images = list(chain(
            *[[i.split()[0].strip() for i in item.split(',')]
              for item in response.css('img[itemprop="image"] ::attr(srcset)').extract()]
        ))
        dimensions = response.xpath(
            '/html/body/div[1]/div[3]/section/div/div/div/div[1]/div[2]/ul/li[6]/span//text()').extract()
        item = CustomLoader(item=Product(), response=response)
        item.context['locale'] = 'en_US'
        item.add_value('url', response.url)
        item.add_css('name', 'h1.bru-product-detail__name ::text')
        item.add_css('price', 'meta[itemprop="price"] ::attr(content)')
        item.add_value('currency', 'EUR')
        item.add_value('description', description)
        item.add_value('dimensions', dimensions)
        item.add_value('material', ", ".join(material))
        item.add_css('sku', 'span[itemprop="sku"] ::text')
        item.add_value('image_urls', images)
        yield item.load_item()
