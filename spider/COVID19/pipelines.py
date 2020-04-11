# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import sqlite3
from .items import CityItem, ProvinceItem, CountryItem

class Covid19Pipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ProvinceItem):
            ProvinceItem.django_model.objects.update_or_create(
                provinceName=item['provinceName'],
                defaults=item
            )
            return item
        elif isinstance(item, CityItem):
            defaults = dict(item)
            defaults['province_id'] = province_id \
                = defaults.pop('province', None)
            CityItem.django_model.objects.update_or_create(
                province_id=province_id,
                cityName=defaults['cityName'],
                defaults=defaults
            )
            return item
        elif isinstance(item, CountryItem):
            CountryItem.django_model.objects.update_or_create(
                continents=item['continents'],
                countryShortCode=item['countryShortCode'],
                defaults=item)
            return item
