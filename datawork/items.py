# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DataworkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PageItem(scrapy.Item):
    host = scrapy.Field()
    url = scrapy.Field()
    file = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    content = scrapy.Field()
    local_urls_set = scrapy.Field()
    external_urls_set = scrapy.Field()
