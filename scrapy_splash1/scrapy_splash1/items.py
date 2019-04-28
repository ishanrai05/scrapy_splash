# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    to = scrapy.Field()
    from_ = scrapy.Field()
    time = scrapy.Field()
    lines = scrapy.Field()

