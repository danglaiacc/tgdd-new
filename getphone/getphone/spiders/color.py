import scrapy
from scrapy_splash import SplashRequest


class ColorSpider(scrapy.Spider):
    name = 'color'
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
            callback=self.check,
            args={'lua_source': script},
            url='https://www.thegioididong.com/dtdd#c=42&m=2326&o=9&pi=0'
        )

 
