# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem
from ncovapi import models


class CrawlerItem(DjangoItem):

    django_model = models.Crawler


class StatisticsItem(DjangoItem):

    django_model = models.Statistics


class NoticeItem(DjangoItem):

    django_model = models.Notice


class WHOArticleItem(DjangoItem):

    django_model = models.WHOArticle


class RecommendItem(DjangoItem):

    django_model = models.Recommend


class TimelineItem(DjangoItem):

    django_model = models.Timeline


class WikiItem(DjangoItem):

    django_model = models.Wiki


class GoodsGuideItem(DjangoItem):

    django_model = models.GoodsGuide


class RumorItem(DjangoItem):

    django_model = models.Rumor


class ProvinceItem(DjangoItem):

    django_model = models.Province


class CountryItem(DjangoItem):

    django_model = models.Country


class CityItem(DjangoItem):

    django_model = models.City