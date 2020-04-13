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

    def close_spider(self,spider):
        basedir = join(settings.BASE_DIR, 'spider', 'data')
        for name in ('cities', 'provinces', 'countries'):
            if not exists(basedir):
                os.makedirs(join(basedir, name))

        for inst in CityItem.django_model.objects.all():
            data = model_to_dict(inst)
            cityName = data['cityName']
            path = join(basedir, 'cities', '%s.json' % cityName)
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False)


        for inst in ProvinceItem.django_model.objects.all():
            data = model_to_dict(inst)
            provinceName = data['provinceName']
            path = join(basedir, 'provinces', '%s.json' % provinceName)
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False)


        for inst in CountryItem.django_model.objects.all():
            data = model_to_dict(inst)
            countryName = data['countryName']
            path = join(basedir, 'countries', '%s.json' % countryName)
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False)
