# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PagineGialleBusiness(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    pagine_gialle_url = scrapy.Field()
    website = scrapy.Field()
    telephone = scrapy.Field()
    search_url = scrapy.Field()
