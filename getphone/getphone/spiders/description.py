import scrapy
import pandas as pd
from getphone.utils import get_phone_id


class DescriptionSpider(scrapy.Spider):
    name = 'description'
    allowed_domains = ['www.thegioididong.com']


    def start_request(self):
        abs_url = 'https://www.thegioididong.com/Product/GetGalleryItemInPopup?productId={}&galleryType=6'
        ids = get_phone_id('../iphone.csv', 'id')
        print(ids)

        for id in ids:
            scrapy.Request(
                url = abs_url,
                callback = self.parse
                )

    def parse(self, response):
        print(response)

