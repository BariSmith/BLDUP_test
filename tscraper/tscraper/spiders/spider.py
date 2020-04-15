# # -*- coding: utf-8 -*-
# import scrapy
#
#
# class SpiderSpider(scrapy.spiders.Spider):
#     name = 'spider'
#     allowed_domains = ['http://www.tauntondeeds.com/Searches/ImageSearch.aspx']
#     start_urls = ['http://www.tauntondeeds.com/Searches/ImageSearch.aspx/']
#
#     def parse(self, response):
#         all_docs = response.xpath('//div[@class="gridGrow"]')
#
#         for doc in all_docs:
#             view = doc.xpath('.//div[@class="gridRow"]/tbody/tr/td/a/@href').extract_first()
#             data = doc.xpath('.//div[@class="gridRow"]/tbody/tr/td//td').extract_first()
#             type = doc.xpath('.//div[@class="gridRow"]/tbody/tr/td//td').extract_first()
#             book = doc.xpath('.//div[@class="gridRow"]/tbody/tr/td//td').extract_first()
#             page_num = doc.xpath('.//div[@class="gridRow"]/tbody/tr/td//td').extract_first()
#             doc_num = doc.xpath('.//div[@class="gridRow"]/tbody/tr/td//td').extract_first()
#             city = doc.xpath('.//div[@class="gridRow"]/tbody/tr/td//td').extract_first()
#             description = doc.xpath('.//div[@class="gridRow"]/tbody/tr/td//td').extract_first()
#             # cost =
#             # street_address =
#             # state =
#             # zip =
#
#             print(view, data, type, book, page_num, doc_num, city, description)
import re
from datetime import datetime

import scrapy

from ..items import TauntondeedsItem
from ..post_request import headers, data


class DataSpider(scrapy.Spider):
    name = "dataspider"
    url = 'http://www.tauntondeeds.com/Searches/ImageSearch.aspx'

    def start_requests(self):
        return [scrapy.FormRequest(url=self.url, method='POST',
                                   headers=headers, formdata=data, callback=self.parse)]

    def parse(self, response):
        for page in range(1, 3):
            formdat = {
                # next page
                "__EVENTTARGET": "ctl00$cphMainContent$gvSearchResults",
                "__EVENTARGUMENT": "Page$" + str(page),
            }
            yield scrapy.FormRequest.from_response(response, formdata=formdat, callback=self.parse_page, dont_click=True)

    def parse_page(self, response):
        items = response.css('tr[class*="grid"]:not([class*="gridHeader"]):not([class*="gridPager"])')
        pattern = r'(?:(.*)\s+)(\d?\s*?[A-Za-z0-9-&]+\s*\w+\s+(?:ST|AVE|BLV|DR|LN|WAY|RD|LANE))(?:\s*,\s*\$(\d+\.\d+))?$'
        for item in items:
            page_details = TauntondeedsItem()
            page_details['date'] = datetime.strptime(items.css('td::text')[1].get(), '%m/%d/%Y')
            page_details['type'] = item.css('td::text')[2].get()
            page_details['book'] = item.css('td::text')[3].get()
            # page_details['book'] = page_details['book'].replace(u'\xa0', u' ')
            if page_details['book'] == u'\xa0':
                page_details['book'] = None

            page_details['page_num'] = item.css('td::text')[4].get()
            if page_details['page_num'] == u'\xa0':
                page_details['page_num'] = None

            page_details['doc_num'] = item.css('td::text')[5].get()
            page_details['city'] = item.css('td::text')[6].get()

            text = item.css('td > span::text').get().strip()
            match = re.match(pattern, text)
            state = None
            zip_index = None
            page_details['description'] = match.group(1)
            page_details['street_address'] = match.group(2)
            cost = match.group(3)
            if cost:
                page_details['cost'] = float(cost)
            else:
                page_details['cost'] = cost  # None
            page_details['state'] = None
            page_details['zip'] = None
            yield page_details