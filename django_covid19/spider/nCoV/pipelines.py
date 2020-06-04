# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import sqlite3
from uuid import uuid4

from django.core.cache import cache

from . import items

class BasePipeline(object):

    def open_spider(self, spider):
        spider.object_id = uuid4().hex
        cache.set('running_spider_id', spider.object_id)
        spider.crawled = 0

    def close_spider(self, spider):
        cache.set('crawled', spider.crawled)
        cache.delete('running_spider_id')


class CovidTrackingPipeline(BasePipeline):

    def process_item(self, item, spider):
        if isinstance(item, items.ProvinceItem) \
                and item['countryCode'] == 'USA':
            provinceCode = item['provinceCode']
            countryCode = item['countryCode']
            items.ProvinceItem.django_model.objects.update_or_create(
                countryCode=countryCode,
                provinceCode=provinceCode,
                defaults=item)
            return item


class NcovPipeline(BasePipeline):

    def process_item(self, item, spider):
        if isinstance(item, items.CityItem):
            countryCode = item['countryCode']
            provinceCode = item['provinceCode']
            items.CityItem.django_model.objects.update_or_create(
                countryCode=countryCode,
                provinceCode=provinceCode,
                cityName=item['cityName'],
                defaults=item)
            return item
        elif isinstance(item, items.ProvinceItem) \
                and item['countryCode'] == 'CHN':
            items.ProvinceItem.django_model.objects.update_or_create(
                provinceName=item['provinceName'],
                defaults=item)
            return item
        elif isinstance(item, items.CountryItem):
            items.CountryItem.django_model.objects.update_or_create(
                countryName=item['countryName'],
                defaults=item)
            return item
        elif isinstance(item, items.StatisticsItem):
            klass = item.__class__
            klass.django_model.objects.create(**item)
            return item
        else:
            return item