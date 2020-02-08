# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class PagineGialleBusiness(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    pagine_gialle_url = scrapy.Field()
    website = scrapy.Field()
    telephone = scrapy.Field()
    search_url = scrapy.Field()


class Product(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    unique_id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    sku = scrapy.Field(output_processor=TakeFirst())
    dimensions = scrapy.Field(output_processor=TakeFirst())
    weight = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field()
    images = scrapy.Field(output_processor=TakeFirst())