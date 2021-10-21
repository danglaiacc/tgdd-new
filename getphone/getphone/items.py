# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class PhoneItem(scrapy.Item):
    id=scrapy.Field(output_processor = TakeFirst())
    name=scrapy.Field(output_processor = TakeFirst())
    screen=scrapy.Field(output_processor = TakeFirst())
    os=scrapy.Field(output_processor = TakeFirst())
    camera_sau=scrapy.Field(output_processor = TakeFirst())
    camera_truoc=scrapy.Field(output_processor = TakeFirst())
    chip=scrapy.Field(output_processor = TakeFirst())
    ram=scrapy.Field(output_processor = TakeFirst())
    rom=scrapy.Field(output_processor = TakeFirst())
    sim=scrapy.Field(output_processor = TakeFirst())
    pin=scrapy.Field(output_processor = TakeFirst())


class GetphoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
