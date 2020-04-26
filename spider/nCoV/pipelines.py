# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import sqlite3

from django.core.cache import cache

from . import items


class NcovPipeline(object):

    def open_spider(self, spider):
        spider.crawler = items.CrawlerItem.django_model.objects.create()

    def process_item(self, item, spider):
        if isinstance(item, items.CityItem):
            provice_location_id = item.pop('province')
            province = items.ProvinceItem.django_model.objects.filter(
                locationId=provice_location_id,
                crawler=spider.crawler).first()
            item['province'] = province
            items.CityItem.django_model.objects.create(
                crawler=spider.crawler, **item
            )
            return item
        elif isinstance(item, (items.ProvinceItem, items.CountryItem,
                               items.StatisticsItem, items.NoticeItem,
                               items.WHOArticleItem, items.RecommendItem,
                               items.TimelineItem, items.WikiItem,
                               items.GoodsGuideItem, items.RumorItem)):
            klass = item.__class__
            klass.django_model.objects.create(
                crawler=spider.crawler, **item
            )
            return item

    def close_spider(self, spider):
        if spider.crawler is not None:
            cache.set('crawled', 1)
