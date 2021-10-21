import scrapy


class DescriptionSpider(scrapy.Spider):
    name = 'description'
    allowed_domains = ['www.thegioididong.com']

    def parse(self, response):
        pass
