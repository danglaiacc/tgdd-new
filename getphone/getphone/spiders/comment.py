# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest
from scrapy.loader import ItemLoader
from ..items import CommentItem
from scrapy.selector import Selector
from getphone.utils import get_phone_id


class CommentSpider(Spider):
    name = 'comment'
    allowed_domains = ['www.thegioididong.com']

    url = 'https://www.thegioididong.com/Rating/RatingCommentList/'
    formdata = {'productid': '213031',
                'page': '1', 'ilsBuy': '1', 'iOrder': '1'}

    def start_requests(self):
        modal_ids = get_phone_id('phones.csv')
        print('~~ len modal_ids',len(modal_ids))
        for modal_id in modal_ids:
            self.formdata['productid'] = str(modal_id)
            self.formdata['page'] = '1'
            yield FormRequest(
                url=self.url,
                formdata=self.formdata,
                callback=self.parse,
                meta = {'modal_id': self.formdata['productid']}
            )

    def parse(self, response):
#        with open('comment_raw.html', 'a', encoding='utf8') as f:
#            f.write(response.xpath(
#                '//div[@class="comment comment--all ratingLst"]').get()+'\n')
        comments = response.xpath(
            '//div[@class="comment__item par"]').getall()
        if len(comments) ==0:
            return 

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

        # next page
        self.formdata['page'] = str(int(self.formdata['page'])+1)
        yield FormRequest(
            url=self.url,
            callback=self.parse,
            meta = {'modal_id': self.formdata['productid']},
            formdata=self.formdata,
        )


