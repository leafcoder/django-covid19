# -*- coding: utf-8 -*-
# @Author: zhanglei3
# @Date:   2020-04-08 09:08:13
# @Last Modified by:   leafcoder
# @Last Modified time: 2020-04-10 21:44:27

"""丁香园数据源"""

import json
import scrapy
from scrapy.selector import Selector
from ..items import ProvinceItem, CountryItem, CityItem

class DXYSpider(scrapy.Spider):

    name = "dxy"
    allowed_domains = ["ncov.dxy.cn"]
    start_urls = [
        "http://ncov.dxy.cn/ncovh5/view/pneumonia",
    ]

    def parse(self, response):
        sel = Selector(response)
        # 处理国内数据

        ret = sel.re(r'getAreaStat\s*=\s*(\[[^\<\>]+\])[^\<\>]*\<')
        provinces = json.loads(ret[0])
        for province in provinces:
            cities = province.pop('cities', [])
            province = ProvinceItem(**province)
            yield province
            for city in cities:
                yield CityItem(province=province['locationId'], **city)
        # 处理国外数据
        ret = sel.re(
            r'getListByCountryTypeService2true\s*=\s*(\[[^\<\>]+\])[^\<\>]*\<')
        countries = json.loads(ret[0])
        for country in countries:
            country.pop('id', None)
            country['countryName'] = country.pop('provinceName', None)
            country['provinceName'] = ''
            country.pop('cityName')
            country.pop('provinceId')
            country.pop('provinceName')
            country.pop('provinceShortName')
            yield CountryItem(**country)