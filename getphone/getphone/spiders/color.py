import scrapy
from scrapy_splash import SplashRequest
from getphone.utils import script_full, script_more, get_url_img


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
        link_img_slide = 'https://www.thegioididong.com/Product/GetGalleryItem?productId={}&galleryType=2&colorId={}'
        for color in colors:
            color_id = color.xpath('.//@data-color-id').get()

            # get url of img demo
            url = color.xpath('.//img/@data-src').get()
            url_img = get_url_img(url,2)

            modal_id = get_url_img(url,1)
            yield SplashRequest(
                url=link_img_slide.format(modal_id, color_id),
                endpoint='execute',
                callback=self.get_img_slide,
                args={'lua_source': script_full},
                meta={
                    'id': color_id,
                    'text': color.xpath('.//img/@alt').get(),
                    'img_demo': url_img,
                    'modal_id': modal_id,
                }
            )

    def get_img_slide(self, resp):
        imgs = resp.xpath('//div[@class="detail-slider owl-carousel"]//img/@data-src').getall()

        if len(imgs)==1:
            # if phone has only 1 img in slide
            img_slide = get_url_img(imgs[0],2)
        else:
            # loại bỏ phần .jpg
            img_slide = ','.join([get_url_img(img,2)[:-4] for img in imgs])

        yield{
                'id' : resp.request.meta['id'],
                'text' : resp.request.meta['text'],
                'img_demo' : resp.request.meta['img_demo'],
                'modal_id' : resp.request.meta['modal_id'],
                'img_slide': img_slide
                }



