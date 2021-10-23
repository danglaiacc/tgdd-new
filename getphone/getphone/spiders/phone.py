# -*- coding: utf-8 -*-
import scrapy, re
from scrapy_splash import SplashRequest
from getphone.getphone.utils import get_url_img
from getphone.utils import script_full, script_more, url_full


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

    def get_links(self, resp):
        links = resp.xpath(
            '//ul[@class="listproduct"]/li/a[@class="main-contain"]/@href').getall()
        for link in links:
            yield SplashRequest(
                endpoint='execute',
                callback=self.get_info,
                args={'lua_source': script_full},
                url=self.absolute_url.format(link),
            )

    def get_info(self, resp):
        id = resp.xpath('//div[@class="box02__right"]/@data-id').get()
        name = resp.xpath('substring-after(//h1/text(), "Điện thoại ")').get()
        resp_param = resp.xpath("//ul[contains(@class,'parameter__list')]")
        screen = ' '.join(resp_param.xpath("//ul[contains(@class,'parameter__list')]\
            /li/p[contains(text(), 'Màn hình')]\
            /following-sibling::node()//text()[normalize-space()]").extract())
        img_kit = resp.xpath('//div[@class="img-main"]/img/@data-src')
        if len(img_kit)>1:
            img_kit =f'<img src="{img_kit.get()}" alt="kit">'
        else:
            img_kit = ''

        url_img_slider = resp.xpath('//div[@class="owl-stage"]//img/@data-src').getall()
        # remove Slider/ before url
        img_slider = ','.join([get_url_img(img,2)[7:] for img in url_img_slider])

        param_titles = ["Hệ điều hành", "Camera sau", "Camera trước",
                        "Chip", "RAM", "Bộ nhớ trong", "SIM", "Pin, Sạc"]
        params = [self.get_another_param(
            resp_param, param_title) for param_title in param_titles]
        sale_price = resp.xpath(
            'translate(//p[contains(@class,"box-price-present")]/text(), "₫. *", "")').get()
        origin_price = resp.xpath(
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
                'id': id,
                'name': name,
                'sale_price': sale_price,
                'orig_price': orig_price,
                'screen': screen,
                'os': params[0],
                'camera_truoc': params[2],
                'camera_sau': params[1],
                'cpu': params[3],
                'ram': params[4],
                'rom': params[5],
                'sim': params[6],
                'pin': params[7],
                'img_slider': img_slider,
                'img_kit': img_kit
            }
        )

       # Sản phẩm cùng tên khác cấu hình
        same_item = resp.xpath(
            '//a[@class="box03__item item act"]/following-sibling::node()//@href[not(contains(., "code="))]')
        if len(same_item) > 1:
            for link in same_item.getall():
                yield SplashRequest(
                    endpoint='execute',
                    callback=self.get_info,
                    args={'lua_source': script_full},
                    url=self.absolute_url.format(link),
                )

    def get_info_article(self, response):
        article = ''.join(response.xpath(
            '//div[contains(@class,"article__content")]/*[not(self::script or self::form or self::div[@id="highlighter--hover-tools"])]').getall())
        article = re.sub(
            r'class="preventdefault"|onclick="return false;"|class="lazyload"|title=\".*?\"|target="_blank"', '', article)
        article = re.sub('data-src', 'src', article)
        article = re.sub('"  >', '">', article)
        article = re.sub(r'  |\xa0', ' ', article)
        article = response.request.meta['img_kit'] + article
        yield{
            'id': response.request.meta['id'],
            'name': response.request.meta['name'],
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
            'img_slider': response.request.meta['img_slider'],
            'article': article
        }

    def get_another_param(self, response,  param_title):
        return response.xpath(f"//ul[contains(@class,'parameter__list')]/li/p[contains(text(), '{param_title}')]/following-sibling::node()//text()[normalize-space()]").get()
