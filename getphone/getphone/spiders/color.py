import scrapy
from scrapy_splash import SplashRequest
from getphone.utils import script_full, script_more


class ColorSpider(scrapy.Spider):
    name = 'color'
    allowed_domains = ['www.thegioididong.com']
    absolute_url = 'https://www.thegioididong.com{}'

    def start_requests(self):
        yield SplashRequest(
            endpoint='execute',
            callback=self.get_links,
            args={'lua_source': script_more},
            url='https://www.thegioididong.com/dtdd#c=42&m=2235&o=9&pi=0'
        )

    def get_links(self, resp):
        links = resp.xpath(
            '//ul[@class="listproduct"]/li/a[@class="main-contain"]/@href').getall()
        for link in links:
            yield SplashRequest(
                endpoint='execute',
                callback=self.get_colors,
                args={'lua_source': script_full},
                url=self.absolute_url.format(link),
            )

    def get_colors(self, resp):
        colors = resp.xpath(
            '//div[@data-gallery-id="color-images-gallery"]')
        link_img_slide = 'https://www.thegioididong.com/Product/GetGalleryItem?productId={}&colorId={}'
        for color in colors:
            color_id = color.xpath('.//@data-color-id').get()
            modal_id = color.xpath('.//img/@data-src').get()[39:45]
            yield{
                'id': color_id,
                'color_text': color.xpath('.//img/@alt').get(),
                'color_img_demo': color.xpath('.//img/@data-src').get()[47:],
                'modal_id': modal_id,
                'link': link_img_slide.format(modal_id, color_id)
            }

