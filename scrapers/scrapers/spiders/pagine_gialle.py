import urllib.parse

from extruct.w3cmicrodata import MicrodataExtractor
import scrapy
import scrapy.exceptions

from ..items import PagineGialleBusiness


class PagineGialleCrawler(scrapy.Spider):
    name = "pagine-gialle"
    allowed_domains = ['paginegialle.it']
    mde = MicrodataExtractor()

    def __init__(self, url, category, **kwargs):
        self.start_urls = [url]
        self.category = category
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_page = response.css('a.btn.btn-blank.arrBtn.rightArrBtn ::attr(href)').extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)
        business_links = response.css('section[itemtype="https://schema.org/LocalBusiness"]')
        for business in business_links:
            try:
                schema_data = self.mde.extract(business.extract())[0]
            except IndexError:
                schema_data = dict()
            yield PagineGialleBusiness(
                name=schema_data.get('properties', dict()).get('name', ''),
                location=schema_data.get('properties', dict()).get('location', dict()).get('value').split('\n')[0],
                description=schema_data.get('properties', dict()).get('description'),
                telephone=business.css('span.phone-label ::text').extract_first(),
                website=business.css('a[data-pag="www"] ::attr(href)').extract_first(),
                pagine_gialle_url=business.css('a[data-pag="vetrina"] ::attr(href)').extract_first().replace('//', ''),
                search_url=self.start_urls[0]
            )
