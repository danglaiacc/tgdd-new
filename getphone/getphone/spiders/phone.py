import scrapy
import json
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['www.thegioididong.com']
    absolute_url = 'https://www.thegioididong.com{}'
    
    def start_requests(self):
        yield scrapy.Request(
                url = 'https://www.thegioididong.com/Category/FilterProductBox?c=42&m=2&o=9&pi=0',
                callback= self.get_links,
                method = 'POST',
                headers={'Content-Type': 'applications/json'}
                )

    def get_links(self, response):
        script = '''
            function main(splash, args)
                assert(splash:go(args.url))
                assert(splash:wait(0.5))
                return splash:html()
            end
        '''
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
                    args = {'lua_source': script},
                    url = self.absolute_url.format(link),
                    )

    def get_info(self, resp):
        id = resp.xpath('//div[@class="box02__right"]/@data-id').get()
        name = resp.xpath('substring-after(//h1/text(), "Điện thoại ")').get()
        resp_param = resp.xpath("//ul[contains(@class,'parameter__list')]")
        screen = ' '.join(resp_param.xpath("//ul[contains(@class,'parameter__list')]/li/p[contains(text(), 'Màn hình')]/following-sibling::node()//text()[normalize-space()]").getall())
        param_titles = ["Hệ điều hành", "Camera sau", "Camera trước", "Chip", "RAM", "Bộ nhớ trong", "SIM", "Pin, Sạc"]
        params = [self.get_another_param(resp_param, param_title) for param_title in param_titles]

        yield{
                'id': id,
                'name': name,
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

    
    def get_another_param(self,response,  param_title):
        return response.xpath(f"//ul[contains(@class,'parameter__list')]/li/p[contains(text(), '{param_title}')]/following-sibling::node()//text()[normalize-space()]").get()

