from scrapy import Item, Field
from itemloaders.processors import TakeFirst


class PhoneItem(Item):
    id = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    screen = Field(output_processor=TakeFirst())
    os = Field(output_processor=TakeFirst())
    camera_sau = Field(output_processor=TakeFirst())
    camera_truoc = Field(output_processor=TakeFirst())
    chip = Field(output_processor=TakeFirst())
    ram = Field(output_processor=TakeFirst())
    rom = Field(output_processor=TakeFirst())
    sim = Field(output_processor=TakeFirst())
    pin = Field(output_processor=TakeFirst())


class CommentItem(Item):
    user_id = Field(output_processor=TakeFirst())
    user_name = Field(output_processor=TakeFirst())
    date_buy = Field(output_processor=TakeFirst())
    modal_id = Field(output_processor=TakeFirst())
    time_up = Field(output_processor=TakeFirst())
    content = Field(output_processor=TakeFirst())
    comment_imgs = Field(output_processor=TakeFirst())
    rate_star = Field(output_processor=TakeFirst())
