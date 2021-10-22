# -*- coding: utf-8 -*-
import scrapy, re
from scrapy_splash import SplashRequest
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

        description_url = 'https://www.thegioididong.com/Product/GetGalleryItemInPopup?productId={}&galleryType=6'
        yield SplashRequest(
            url=description_url.format(id),
            endpoint='execute',
            callback=self.get_info_description,
            args={'lua_source': script_full},
            meta={
                'id': id,
                'name': name,
                'sale_price': sale_price,
                'orig_price': orig_price,
                'screen': screen,
                'os': params[0],
                'camera_sau': params[1],
                'camera_truoc': params[2],
                'chip': params[3],
                'ram': params[4],
                'rom': params[5],
                'sim': params[6],
                'pin': params[7]
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

    def get_info_description(self, response):
        description = ''.join(response.xpath(
            '//div[contains(@class,"article__content")]/*[not(self::script or self::form or self::div[@id="highlighter--hover-tools"])]').getall())
        description = re.sub(
            r'class="preventdefault"|onclick="return false;"|class="lazyload"|title=\".*?\"|target="_blank"', '', description)
        description = re.sub('data-src', 'src', description)
        description = re.sub('"  >', '">', description)
        description = re.sub(r'  |\xa0', ' ', description)
        yield{
            'id': response.request.meta['id'],
            'name': response.request.meta['name'],
            'sale_price': response.request.meta['sale_price'],
            'orig_price': response.request.meta['orig_price'],
            'screen': response.request.meta['screen'],
            'os': response.request.meta['os'],
            'camera_sau': response.request.meta['camera_sau'],
            'camera_truoc': response.request.meta['camera_truoc'],
            'chip': response.request.meta['chip'],
            'ram': response.request.meta['ram'],
            'rom': response.request.meta['rom'],
            'sim': response.request.meta['sim'],
            'pin': response.request.meta['pin'],
            'description': description
        }

    def get_another_param(self, response,  param_title):
        return response.xpath(f"//ul[contains(@class,'parameter__list')]/li/p[contains(text(), '{param_title}')]/following-sibling::node()//text()[normalize-space()]").get()
