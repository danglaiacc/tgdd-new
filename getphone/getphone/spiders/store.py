import scrapy, re
from scrapy_splash.request import SplashRequest
from getphone.utils import script_full,script_btn_more

class StoreSpider(scrapy.Spider):
    name = 'store'
    allowed_domains = ['thegioididong.com']
    absolute_url = 'https://www.thegioididong.com{}'
    address_pattern = re.compile(r'(.+),\s*(.+),')
    map_pattern = re.compile(r'query=([\.\d]+),([\d\.]+)')
    error_match = []

    def start_requests(self):
        yield SplashRequest(
            endpoint='execute',
            url='https://www.thegioididong.com/he-thong-sieu-thi-the-gioi-di-dong',
            args={'lua_source': script_full},
            callback=self.get_provinces
        )


    def get_provinces(self, response):
        #        with open('store.html', 'w', encoding='utf8') as f:
        #            f.write(response.text)
        li_province = response.xpath('//div[@class="scroll-box__store"]/ul/li/a')
        for province in li_province:
            province_href = province.xpath('./@href').get()
            province_name = province.xpath('normalize-space(./text())').get()
            yield SplashRequest(
                endpoint='execute',
                url=self.absolute_url.format(province_href),
                args={'lua_source': script_btn_more.format('.storeaddress a.seemore')},
                callback=self.get_stores,
                meta = {'province_name': province_name}
            )

    def check_match(self, pattern, text):
        if (match := re.search(pattern, text)):
            return match.groups()
        self.error_match.append(text)
        return ['','']


    def get_stores(self, response):
        province_name = response.request.meta['province_name']
        stores = response.xpath('//div[@class="storeaddress"]/ul/li')
        for store in stores:
            store_address = store.xpath('normalize-space(./a[1]/text())').get()
            map_address = store.xpath('./a[2]/@href').get()
            #address_match = self.check_match(self.address_pattern, store_address)
            map_match = self.check_match(self.map_pattern, map_address)
            yield {
                    'province': province_name,
                    'store_address':store_address,
                    #'district': address_match[1],
                    #'address': address_match[0],
                    'latitude': map_match[0],
                    'longitude': map_match[1]
                    }
