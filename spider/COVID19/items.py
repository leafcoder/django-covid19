# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem
from ncovapi.models import City, Province, Country

class Covid19Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProvinceItem(DjangoItem):

    django_model = Province

class CountryItem(DjangoItem):

    django_model = Country

class CityItem(DjangoItem):

    django_model = City