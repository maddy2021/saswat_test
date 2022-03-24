# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CodingTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    tcin = scrapy.Field()
    upc = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    specs = scrapy.Field()
    pass
