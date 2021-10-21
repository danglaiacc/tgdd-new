import scrapy
from scrapy_splash import SplashRequest


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
        script = '''
          function main(splash, args)
            splash:on_request(function(request)
              if request.url:find('css') then
                request.abort()
              end
            end)
            splash.images_enabled = false 
            
            time = 0.5
            assert(splash:go(args.url))
            assert(splash:wait(time))
            
            btn = assert(splash:select(".view-more a"))
            assert(splash:wait(time))
          
            while btn:visible() do
              btn:mouse_click()
              assert(splash:wait(time))
              btn = assert(splash:select(".view-more a"))
            end
            
            return {
              html = splash:html(),
              png = splash:png(),
              har = splash:har(),
            }
          end
        '''

        yield SplashRequest(
                    endpoint='execute',
                    callback = self.check,
                    args = {'lua_source': script},
                    url = 'https://www.thegioididong.com/dtdd-samsung#c=42&m=2,1971,2236&o=9&pi=0'
                    )

    def check(self, resp):
        links = resp.xpath('//ul[@class="listproduct"]/li/a[@class="main-contain"]/@href').getall()
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

        sale_price = resp.xpath('translate(//p[@class="box-price-present"]/text(), "₫. ", "")').get()
        origin_price = resp.xpath('translate(//p[@class="box-price-old"]/text(), "₫. ", "")')
        orig_price = sale_price
        if len(origin_price)>1:
            orig_price = origin_price.get()

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

    def get_another_param(self,response,  param_title):
        return response.xpath(f"//ul[contains(@class,'parameter__list')]/li/p[contains(text(), '{param_title}')]/following-sibling::node()//text()[normalize-space()]").get()

