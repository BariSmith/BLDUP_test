# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


import scrapy


class TauntondeedsItem(scrapy.Item):
    date = scrapy.Field()
    type = scrapy.Field()
    book = scrapy.Field()
    page_num = scrapy.Field()
    doc_num = scrapy.Field()
    city = scrapy.Field()
    description = scrapy.Field()
    cost = scrapy.Field()
    street_address = scrapy.Field()
    state = scrapy.Field()
    zip = scrapy.Field()