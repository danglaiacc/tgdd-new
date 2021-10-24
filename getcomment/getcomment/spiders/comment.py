from scrapy import Spider, FormRequest
from scrapy.loader import ItemLoader
from ..items import CommentItem

class CommentSpider(Spider):
    name = 'comment'
    allowed_domains = ['www.thegioididong.com']

    url = 'https://www.thegioididong.com/Rating/RatingCommentList/'
    formdata = {'productid': '213031', 'page':'3', 'iIsBuy': '1', 'iOrder': '1'}

    def start_requests(self):
        yield FormRequest(
                url = self.url,
                formdata = self.formdata,
                callback = self.parse,
                meta = {'modal_id': self.formdata['productid']}
                )


    def parse(self, response):
       # with open('index3.html', 'w', encoding='utf8') as f:
       #     f.write(response.xpath('//div[@class="comment comment--all ratingLst"]').get()+'\n')
        comments = response.xpath('//div[contains(@class,"comment__item")]').getall()
        for comment in comments:
            loader = ItemLoader( item = CommentItem(), selector=comment)
            loader.add_xpath('user_id', './@id')
            loader.add_xpath('user_name', './/p[@class="txtname"]/text()')
            loader.add_xpath('modal_id', response.request.meta['modal_id'])
            loader.add_xpath('date_buy', './/div[@class="info-buying-txt"]//p[text()="Mua ngày "]/following-sibling::p/text()')
            loader.add_xpath('time_up', './/div[@class="info-buying-txt"]//p[text()="Viết đánh giá"]/following-sibling::p/text()')
            loader.add_xpath('content', './/p[@class="cmt-txt"]/text()')
            loader.add_xpath('comment_imgs', './/img')
            loader.add_xpath('rate_star', './/div[@class="comment-star"]/i')

            yield loader.load_item()
