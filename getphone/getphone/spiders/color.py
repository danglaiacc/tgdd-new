import scrapy
from scrapy_splash import SplashRequest
from getphone.utils import script_full, script_more, get_url_img_from_tag, url_full, get_product_id_from_tag


class ColorSpider(scrapy.Spider):
    name = 'color'
    allowed_domains = ['www.thegioididong.com']
    absolute_url = 'https://www.thegioididong.com{}'

    def start_requests(self):
        yield SplashRequest(
            endpoint='execute',
            callback=self.get_links,
            args={'lua_source': script_more},
            url= url_full
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
#            url = color.xpath('.//img/@data-src').get()
#            url_img = get_url_img(url,2)
#
            product_id = get_product_id_from_tag(color.xpath('.//img').get())
            url_img = get_url_img_from_tag(color.xpath('.//img').get())
            yield SplashRequest(
                url=link_img_slide.format(product_id, color_id),
                endpoint='execute',
                callback=self.get_img_slide,
                args={'lua_source': script_full},
                meta={
                    'id': color_id,
                    'name': color.xpath('.//img/@alt').get(),
                    'img_demo': url_img,
                    'product_id': product_id,
                }
            )

       # Sản phẩm cùng tên khác cấu hình
        same_item = resp.xpath(
            '//a[@class="box03__item item act"]/following-sibling::node()//@href[not(contains(., "code="))]')
        if len(same_item) > 1:
            for link in same_item.getall():
                yield SplashRequest(
                    endpoint='execute',
                    callback=self.get_colors,
                    args={'lua_source': script_full},
                    url=self.absolute_url.format(link),
                )



    def get_img_slide(self, resp):
        imgs = resp.xpath('//div[@class="detail-slider owl-carousel"]//img').getall()

        if len(imgs)==1:
            img_slide = get_url_img_from_tag(imgs[0])
        else:
            img_slide = ','.join([get_url_img_from_tag(img) for img in imgs])

        yield{
                'id' : resp.request.meta['id'],
                'name' : resp.request.meta['name'],
                'img_demo' : resp.request.meta['img_demo'],
                'product_id' : resp.request.meta['product_id'],
                'img_slide': img_slide
                }



