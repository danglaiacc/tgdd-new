# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest
from scrapy.loader import ItemLoader
from ..items import CommentItem
from scrapy.selector import Selector


class CommentSpider(Spider):
    name = 'comment'
    allowed_domains = ['www.thegioididong.com']

    url = 'https://www.thegioididong.com/Rating/RatingCommentList/'
    modal_id = '213031'
    formdata = {'productid': '213031',
                'page': '1', 'ilsBuy': '1', 'iOrder': '1'}

    def start_requests(self):
        yield FormRequest(
            url=self.url,
            formdata=self.formdata,
            callback=self.parse,
            meta = {'modal_id': self.formdata['productid']}
        )

    def parse(self, response):
#        with open('index5.html', 'w', encoding='utf8') as f:
#            f.write(response.xpath(
#                '//div[@class="comment comment--all ratingLst"]').get()+'\n')
        comments = response.xpath(
            '//div[@class="comment__item par"]').getall()

        # print('~~~~ commment', comments)
        for comment in comments:
#            abc = Selector(text = comment)
#            yield{
#                    'user_name': abc.xpath('normalize-space(.//p[@class="txtname"]/text())').get()
#
#                    }
            # print('~~~~ commment', comment)
            # print('~~~~ id:', comment.xpath('./@id').get())
            loader = ItemLoader(item=CommentItem(), selector=Selector(text=comment))
            loader.add_xpath('modal_id', response.request.meta['modal_id'])
            loader.add_xpath('user_id', 'substring-after(.//@id, "r-")')
            loader.add_xpath('user_name', 'normalize-space(.//p[@class="txtname"]/text())')
            loader.add_xpath('date_buy', './/div[@class="info-buying-txt"]//p[text()="Mua ngày "]/following-sibling::p/text()')
            loader.add_xpath('time_up', './/div[@class="info-buying-txt"]//p[text()="Viết đánh giá"]/following-sibling::p/text()')
            loader.add_xpath('content', 'normalize-space(.//p[@class="cmt-txt"]/text())')
            loader.add_xpath('comment_imgs', './/img/@data-src')
            loader.add_xpath('rate_star', 'count(.//div[@class="comment-star"]/i[@class="icon-star"])')

            yield loader.load_item()
