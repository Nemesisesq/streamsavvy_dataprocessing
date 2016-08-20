# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

from data_processor.models import Schedule


class CollegeFootballScraperItem(DjangoItem):

    django_model = Schedule
    # define the fields for your item here like:
    # name = scrapy.Field()
    # date_created = scrapy.Field()
    # name = scrapy.Field()
    # games = scrapy.Field()
    # logo = scrapy.Field()


class ProFootballScraperItem(scrapy.Item):


    date_crated = scrapy.Field()
    name = scrapy.Field()
    games = scrapy.Field()
