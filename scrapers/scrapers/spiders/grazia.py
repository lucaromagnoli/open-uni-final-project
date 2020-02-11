import scrapy
import scrapy.exceptions
from scrapy.loader import ItemLoader

from ..items import Product
from ..pipelines import ProcessProduct


class Crawler(scrapy.Spider):
    name = 'grazia'
    pipeline = {ProcessProduct}
    allowed_sites = ['graziamadeinitaly.com']

    def __init__(self, **kwargs):
        self.start_urls = ['https://www.graziamadeinitaly.com/collection-fw-17']
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_sections)

    def parse_sections(self, response):
        for url in response.css('a.list-group-item ::attr(href)').extract():
            yield scrapy.Request(url, self.parse_collection)

    def parse_collection(self, response):
        for url in response.css('div.image a::attr(href)').extract():
            yield scrapy.Request(url, self.parse_item)
        next_page = response.xpath('//*[@id="content"]/div[3]/div[1]/ul/li[4]/a//@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, self.parse_collection)

    def parse_item(self, response):
        item = ItemLoader(item=Product(), response=response)
        item.add_value('url', response.url)
        item.add_css('name', 'div.ckearfix h1::text')
        item.add_css('price', 'div.prezzo-scheda p::text', re='\\u2002(.*)')
        item.add_value('currency', 'EUR')
        item.add_css('description', 'div.descrizione-prodotto p::text')
        item.add_css('sku', 'p.dato-scheda span::text')
        item.add_css('dimensions', 'div.dimensioni-scheda.dato-scheda span::text')
        item.add_css('color', 'div.colore-scheda.dato-scheda span::text')
        item.add_css('material', 'div.materiale-scheda.dato-scheda span::text')
        item.add_xpath('image_urls', ['//*[@id="content"]/div/div[1]/div[2]/*//@src'])
        yield item.load_item()
