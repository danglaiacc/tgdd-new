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
    # parse name from html to vietnamese, max length 30
    #return unescape(content)[:30]
    return unescape(content)


def parse_imgs(imgs_src):
    print('~~ img_src', imgs_src)
    print(type(imgs_src))
#    imgs = []
#    for img in imgs_src:
#        print(img)
#        imgs.append(img[28:])
    # remove https://cdn.tgdd.vn/comment/ of url img comment
    #return [img[28:] for img in imgs_src]
    return imgs_src[28:]

class CommentItem(Item):
    product_id = Field(output_processor=TakeFirst())
    customer_id = Field(output_processor=TakeFirst())
    customer_fullname = Field(
            input_processor = MapCompose(parse_html), 
            output_processor= TakeFirst()
            )
    date_buy = Field(output_processor=TakeFirst())
    time_up = Field(output_processor=TakeFirst())
    content = Field(output_processor=TakeFirst())
    comment_imgs = Field(
            input_processor = MapCompose(parse_imgs),
            )
    rate_star = Field(output_processor=TakeFirst())


