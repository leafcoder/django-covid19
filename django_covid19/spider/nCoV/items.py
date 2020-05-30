# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem
from django_covid19 import models


class StatisticsItem(DjangoItem):

    django_model = models.Statistics


class ProvinceItem(DjangoItem):

    django_model = models.Province


class CountryItem(DjangoItem):

    django_model = models.Country


class CityItem(DjangoItem):

    django_model = models.City

class StateItem(DjangoItem):

    django_model = models.State