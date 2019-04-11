# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RottentomatoesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    url = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    genre = scrapy.Field()
    rating = scrapy.Field()
    level = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    runtime = scrapy.Field()
    studio = scrapy.Field()
