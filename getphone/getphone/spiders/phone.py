# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_splash import SplashRequest
from getphone.utils import script_full, script_more, url_full, clean_phone_name, get_url_img_from_tag


class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['www.thegioididong.com']
    absolute_url = 'https://www.thegioididong.com{}'

    def start_requests(self):
        yield SplashRequest(
            endpoint='execute',
            callback=self.get_links,
            args={'lua_source': script_more},
            url=url_full
        )

    def get_links(self, response):

        phone_items = response.xpath(
            '//ul[@class="listproduct"]/li/a[@class="main-contain"]')

        for phone_item in phone_items:
            link = phone_item.xpath('./@href').get()
           # if (solveNone:=phone_item.xpath('.//img[1]/@src')):
           #     img_demo = get_url_img(solveNone.get())
           #     with open('has1.txt', 'a', encoding='utf8') as f:
           #         f.write(solveNone.get()+'\n')
           # else:
           #     with open('has2.txt', 'a', encoding='utf8')as f:
           #         f.write(phone_item.get()+'\n')

            img_demo = get_url_img_from_tag(phone_item.xpath('.//img[1]').get())

            #img_demo = get_url_img(phone_item.xpath('.//img[1]/@src').get())
            yield SplashRequest(
                endpoint='execute',
                callback=self.get_info,
                args={'lua_source': script_full},
                url=self.absolute_url.format(link),
                meta={
                    'img_demo': img_demo
                }
            )

    def get_info(self, response):
        id = response.xpath('//div[@class="box02__right"]/@data-id').get()
        name = response.xpath(
            'substring-after(//h1/text(), "Điện thoại ")').get()
        response_param = response.xpath(
            "//ul[contains(@class,'parameter__list')]")
        screen = ' '.join(response_param.xpath("//ul[contains(@class,'parameter__list')]\
            /li/p[contains(text(), 'Màn hình')]\
            /following-sibling::node()//text()[normalize-space()]").extract())

        img_kit = response.xpath('//div[@class="img-main"]/img/@data-src')
        if len(img_kit) > 0:
            img_kit = f'<img src="{img_kit.extract()[0]}" alt="kit">'
        else:
            img_kit = ''

        img_sliders = response.xpath('.//div[@class="box01__show"]\
                 //div[@class="detail-slider owl-carousel"]//img[not(starts-with(@data-src,"//cdn"))]')

#        url_img_slider = []
#        for img_tag in img_sliders.getall():
#            with open('err1.txt','a', encoding='utf8') as f:
#                f.write(img_tag+'\n')
#            url_img_slider.append(
#                    get_url_img_from_tag(img_tag)
#                    )
            
        url_img_slider = [
                get_url_img_from_tag(img_tag, 'Slider/') 
                for img_tag in img_sliders.getall()
                ]

#        first_img_slider = img_sliders.xpath('./@src').get()
#        orther_img_slider = img_sliders.xpath('./@data-src').getall()[:-2]

        # remove Slider/ before url
#        img_slider = ','.join([get_url_img(img)[7:]
#                              for img in orther_img_slider])
#        img_slider = get_url_img(first_img_slider)[7:]+','+img_slider
        img_slider = ','.join(url_img_slider)

        param_titles = ["Hệ điều hành", "Camera sau", "Camera trước",
                        "Chip", "RAM", "Bộ nhớ trong", "SIM", "Pin, Sạc"]
        params = [self.get_another_param(
            response_param, param_title) for param_title in param_titles]
        sale_price = response.xpath(
            'translate(//p[contains(@class,"box-price-present")]/text(), "₫. *", "")').get()
        origin_price = response.xpath(
            'translate(//p[contains(@class,"box-price-old")]/text(), "₫. *", "")')

        orig_price = sale_price
        if len(origin_price) > 1:
            orig_price = origin_price.get()

        article_url = 'https://www.thegioididong.com/Product/GetGalleryItemInPopup?productId={}&galleryType=6'
        yield SplashRequest(
            url=article_url.format(id),
            endpoint='execute',
            callback=self.get_info_article,
            args={'lua_source': script_full},
            meta={
                'id': id, 'name': name, 'sale_price': sale_price, 'orig_price': orig_price, 'screen': screen, 'os': params[0], 'camera_truoc': params[2], 'camera_sau': params[1], 'cpu': params[3], 'ram': params[4], 'rom': params[5], 'sim': params[6], 'pin': params[7], 'img_slider': img_slider, 'img_kit': img_kit,
                'img_demo': response.request.meta['img_demo'],
            }
        )

        # Sản phẩm cùng tên khác cấu hình
        #same_item = response.xpath(
        #    '//a[@class="box03__item item act"]/following-sibling::node()//@href[not(contains(., "code="))]')
        #if len(same_item) > 1:
        #    for link in same_item.getall():
        #        yield SplashRequest(
        #            endpoint='execute',
        #            callback=self.get_info,
        #            args={'lua_source': script_full},
        #            url=self.absolute_url.format(link),
        #            meta = {
        #                'img_demo': response.request.meta['img_demo'],
        #                }
        #        )

    def get_info_article(self, response):
        article = ''.join(response.xpath(
            '//div[contains(@class,"article__content")]/*[not(self::script or self::form or self::div[@id="highlighter--hover-tools"])]').getall())
        article = re.sub(
            r' (?:style|id|class|onclick|target|title)=\".*?\"', '', article)
        article = re.sub('data-src', 'src', article)
        article = re.sub('"  >', '">', article)
        article = re.sub(r'  |\xa0', ' ', article)
        article = response.request.meta['img_kit'] + article

        phone_name = response.request.meta['name']
        parent_info = clean_phone_name(phone_name)

        yield{
            'id': response.request.meta['id'],
            'sale_price': response.request.meta['sale_price'],
            'orig_price': response.request.meta['orig_price'],
            'screen': response.request.meta['screen'],
            'os': response.request.meta['os'],
            'camera_truoc': response.request.meta['camera_truoc'],
            'camera_sau': response.request.meta['camera_sau'],
            'cpu': response.request.meta['cpu'],
            'ram': response.request.meta['ram'],
            'rom': response.request.meta['rom'],
            'sim': response.request.meta['sim'],
            'pin': response.request.meta['pin'],
            'img_demo': response.request.meta['img_demo'],
            'img_slider': response.request.meta['img_slider'],
            'article': article,
            'manu_text': parent_info['manu_text'],
            'version_text': parent_info['version_text'],
            'name': parent_info['modal_text']
        }

    def get_another_param(self, response,  param_title):
        return response.xpath(f"//ul[contains(@class,'parameter__list')]/li/p[contains(text(), '{param_title}')]/following-sibling::node()//text()[normalize-space()]").get()
