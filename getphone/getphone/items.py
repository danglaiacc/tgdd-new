from scrapy import Item, Field
from itemloaders.processors import Join, TakeFirst, MapCompose
# from w3lib.html import replace_entities
from html import unescape

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


def parse_html(content):
    return unescape(content)

def parse_imgs(imgs_src):
    imgs = []
    for img in imgs_src:
        print(img)
        imgs.append(img[28:])
    return imgs

class CommentItem(Item):
    user_id = Field(output_processor=TakeFirst())
    user_name = Field(
            input_processor = MapCompose(parse_html), 
            output_processor= TakeFirst()
            )
    date_buy = Field(output_processor=TakeFirst())
    modal_id = Field(output_processor=TakeFirst())
    time_up = Field(output_processor=TakeFirst())
    content = Field(output_processor=TakeFirst())
    comment_imgs = Field(
            input_processor = MapCompose(parse_imgs)
            )
    rate_star = Field(output_processor=TakeFirst())
