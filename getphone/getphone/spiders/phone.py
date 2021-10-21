import scrapy
import json
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
import re


class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['www.thegioididong.com']
    absolute_url = 'https://www.thegioididong.com{}'
    script = '''
            function main(splash, args)
                splash:on_request(function(request)
                    if request.url:find('css') then
                        request.abort()
                    end
                end)
                splash.images_enabled = false
                splash.js_enabled = false
                assert(splash:go(args.url))
                assert(splash:wait(0.5))
                return splash:html()
            end
        '''

    def start_requests(self):
        yield scrapy.Request(
                url = 'https://www.thegioididong.com/Category/FilterProductBox?c=42&m=2&o=9&pi=0',
                callback= self.get_links,
                method = 'POST',
                headers={'Content-Type': 'applications/json'}
                )

    def get_links(self, response):
        resp = json.loads(response.body)
        html = resp.get('listproducts')
        products = Selector(text = html)
       #  print(html)
       #  with open('index.html', 'w', encoding='utf8') as f:
       #      f.write(html)
        links = products.xpath('//li[contains(@class,"item")]/a[@class="main-contain"]/@href').getall()
        for link in links:
            yield SplashRequest(
                    endpoint='execute',
                    callback = self.get_info,
                    args = {'lua_source': self.script},
                    url = self.absolute_url.format(link),
                    )

    def get_info(self, resp):
        id = resp.xpath('//div[@class="box02__right"]/@data-id').get()
        name = resp.xpath('substring-after(//h1/text(), "Điện thoại ")').get()
        resp_param = resp.xpath("//ul[contains(@class,'parameter__list')]")
        screen = ' '.join(resp_param.xpath("//ul[contains(@class,'parameter__list')]\
            /li/p[contains(text(), 'Màn hình')]\
            /following-sibling::node()//text()[normalize-space()]").extract())

        param_titles = ["Hệ điều hành", "Camera sau", "Camera trước", "Chip", "RAM", "Bộ nhớ trong", "SIM", "Pin, Sạc"]
        params = [self.get_another_param(resp_param, param_title) for param_title in param_titles]

        sale_price = resp.xpath('//p[@class="box-price-present"]/text()').get()
        orig_price = resp.xpath('//p[@class="box-price-old"]/text()').get()
        sale_price = int(re.sub(r'\D','', sale_price))
        orig_price = int(re.sub(r'\D','', orig_price))

        yield{
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

       # Sản phẩm cùng tên khác cấu hình
       # same_item= resp.xpath('//a[@class="box03__item item act"]/following-sibling::node()//@href[not(contains(., "code="))]')
       # if len(same_item)>1:
       #     for link in same_item.getall():
       #         yield SplashRequest(
       #                 endpoint='execute',
       #                 callback = self.get_info,
       #                 args = {'lua_source': self.script},
       #                 url = self.absolute_url.format(link),
       #                 )
    

    def get_another_param(self,response,  param_title):
        return response.xpath(f"//ul[contains(@class,'parameter__list')]/li/p[contains(text(), '{param_title}')]/following-sibling::node()//text()[normalize-space()]").get()

