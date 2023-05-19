# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TeamItem(scrapy.Item):
    # define the fields for your item here
    id  = scrapy.Field()
    name = scrapy.Field()
    abbr = scrapy.Field()
    color = scrapy.Field()
    seoName = scrapy.Field()
    table = scrapy.Field()
