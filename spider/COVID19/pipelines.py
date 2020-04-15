# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import sqlite3
from posixpath import join, exists
from django.conf import settings
from django.forms.models import model_to_dict
from .items import CrawlerItem, CityItem, ProvinceItem, CountryItem

class Covid19Pipeline(object):

    def open_spider(self, spider):
        spider.crawler = CrawlerItem.django_model.objects.create()

    def process_item(self, item, spider):
        if isinstance(item, ProvinceItem):
            ProvinceItem.django_model.objects.create(
                crawler=spider.crawler, **item
            )
            return item
        elif isinstance(item, CityItem):
            provice_location_id = item.pop('province')
            province = ProvinceItem.django_model.objects.filter(
                locationId=provice_location_id,
                crawler=spider.crawler).first()
            item['province'] = province
            CityItem.django_model.objects.create(
                crawler=spider.crawler, **item
            )
            return item
        elif isinstance(item, CountryItem):
            CountryItem.django_model.objects.create(
                crawler=spider.crawler, **item
            )
            return item