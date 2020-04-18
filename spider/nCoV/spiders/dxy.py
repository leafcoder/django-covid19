# -*- coding: utf-8 -*-
# @Author: zhanglei3
# @Date:   2020-04-08 09:08:13
# @Last Modified by:   leafcoder
# @Last Modified time: 2020-04-17 22:51:26

"""丁香园数据源"""

import json
import scrapy
from scrapy.selector import Selector
from ..items import StatisticsItem, ProvinceItem, CountryItem, CityItem

from datetime import datetime

class DXYSpider(scrapy.Spider):

    name = "dxy"
    allowed_domains = ["ncov.dxy.cn"]
    start_urls = [
        "http://ncov.dxy.cn/ncovh5/view/pneumonia",
    ]

    def parse(self, response):
        sel = Selector(response)
        scripts = sel.xpath('//script')

        # 国内数据
        provinces = self.get_list(scripts, '#getAreaStat')
        for province in provinces:
            cities = province.pop('cities', [])
            province = ProvinceItem(**province)
            yield province
            for city in cities:
                yield CityItem(province=province['locationId'], **city)

        # 国外数据
        countries = self.get_list(scripts, '#getListByCountryTypeService2true')
        for country in countries:
            country.pop('id', None)
            country['countryName'] = country.pop('provinceName', None)
            country['provinceName'] = ''
            country.pop('cityName')
            country.pop('provinceId')
            country.pop('provinceName')
            country.pop('provinceShortName')
            yield CountryItem(**country)

        # 统计信息
        statistics = self.get_statistics(scripts, '#getStatisticsService')
        for item in statistics:
            yield item

    def get_list(self, scripts, data_id):
        ret = scripts.css(data_id).re(r'(\[.+\])')
        return json.loads(ret[0])

    def get_dict(self, scripts, data_id):
        ret = scripts.css(data_id).re(r'\=\s*(\{.+\})\}catch\(e\)\{\}')
        return json.loads(ret[0])

    def get_statistics(self, scripts, data_id):
        data = self.get_dict(scripts, data_id)
        statistics = data['globalStatistics']
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount'):
            item[key] = statistics.get(key, 0)
        item['countryType'] = StatisticsItem.django_model.GLOBAL
        yield StatisticsItem(**item)


        statistics = data['foreignStatistics']
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount'):
            item[key] = statistics.get(key, 0)
        item['countryType'] = StatisticsItem.django_model.DOMESTIC
        yield StatisticsItem(**item)


        statistics = data
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount'):
            item[key] = statistics.get(key, 0)
        item['countryType'] = StatisticsItem.django_model.INTERNATIONAL
        yield StatisticsItem(**item)

        self.crawler.createTime \
            = datetime.fromtimestamp(data['createTime'] / 1000.0)
        self.crawler.modifyTime \
            = datetime.fromtimestamp(data['modifyTime'] / 1000.0)
        self.crawler.save()