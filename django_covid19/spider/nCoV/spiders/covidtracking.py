# -*- coding: utf-8 -*-
# @Author: zhanglei3
# @Date:   2020-04-08 09:08:13
# @Last Modified by:   leafcoder
# @Last Modified time: 2020-06-01 12:43:31

"""美国各州疫情数据源"""

import json
import scrapy
import logging
from scrapy.selector import Selector

from .. import items

from django.core.cache import cache
from django.utils.timezone import datetime, make_aware
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger()

# For state i18n
STATES = {
    "Alabama": _("Alabama"),
    "Alaska": _("Alaska"),
    "AmericanSamoa": _("AmericanSamoa"),
    "Arizona": _("Arizona"),
    "Arkansas": _("Arkansas"),
    "California": _("California"),
    "Colorado": _("Colorado"),
    "Connecticut": _("Connecticut"),
    "Delaware": _("Delaware"),
    "DistrictOfColumbia": _("DistrictOfColumbia"),
    "Florida": _("Florida"),
    "Georgia": _("Georgia"),
    "Guam": _("Guam"),
    "Hawaii": _("Hawaii"),
    "Idaho": _("Idaho"),
    "Illinois": _("Illinois"),
    "Indiana": _("Indiana"),
    "Iowa": _("Iowa"),
    "Kansas": _("Kansas"),
    "Kentucky": _("Kentucky"),
    "Louisiana": _("Louisiana"),
    "Maine": _("Maine"),
    "Maryland": _("Maryland"),
    "Massachusetts": _("Massachusetts"),
    "Michigan": _("Michigan"),
    "Minnesota": _("Minnesota"),
    "Mississippi": _("Mississippi"),
    "Missouri": _("Missouri"),
    "Montana": _("Montana"),
    "Nebraska": _("Nebraska"),
    "Nevada": _("Nevada"),
    "NewHampshire": _("NewHampshire"),
    "NewJersey": _("NewJersey"),
    "NewMexico": _("NewMexico"),
    "NewYork": _("NewYork"),
    "NorthCarolina": _("NorthCarolina"),
    "NorthDakota": _("NorthDakota"),
    "NorthernMarianaIslands": _("NorthernMarianaIslands"),
    "Ohio": _("Ohio"),
    "Oklahoma": _("Oklahoma"),
    "Oregon": _("Oregon"),
    "Pennsylvania": _("Pennsylvania"),
    "PuertoRico": _("PuertoRico"),
    "RhodeIsland": _("RhodeIsland"),
    "SouthCarolina": _("SouthCarolina"),
    "SouthDakota": _("SouthDakota"),
    "Tennessee": _("Tennessee"),
    "Texas": _("Texas"),
    "USVirginIslands": _("USVirginIslands"),
    "Utah": _("Utah"),
    "Vermont": _("Vermont"),
    "Virginia": _("Virginia"),
    "Washington": _("Washington"),
    "WestVirginia": _("WestVirginia"),
    "Wisconsin": _("Wisconsin"),
    "Wyoming": _("Wyoming")
}

class CovidTrackingSpider(scrapy.Spider):

    """Data source: https://covidtracking.com/api

    Covidtracking update all the data each day between 4pm and 5pm EDT.
    """

    name = "covidtracking"
    allowed_domains = ["covidtracking.com"]

    # custom attributes
    daily_state_url_template = \
        'https://covidtracking.com/api/v1/states/%s/daily.json'
    current_state_url_template = \
        'https://covidtracking.com/api/v1/states/%s/current.json'
    country_short_code = 'USA'
    states = {}

    def start_requests(self):
        object_id = self.object_id
        spider_id = cache.get('running_spider_id')
        if object_id != spider_id:
            logger.info('Spider is running.')
            self.crawled = 0
            return

        yield scrapy.Request(
            'https://covidtracking.com/api/v1/states/info.json',
            self.parse_info)

    def parse_info(self, response):
        country_short_code = self.country_short_code
        states = self.states
        result = json.loads(response.text)
        for item in result:
            state = item['state']
            state_name = item['name']
            state_name = ''.join(state_name.split())
            states[state] = {
                'state': state,
                'countryShortCode': country_short_code,
                'stateName': state_name
            }
        yield scrapy.Request(
            'https://covidtracking.com/api/v1/states/current.json',
            self.parse_current_states)

    def parse_current_states(self, response):
        country_short_code = self.country_short_code
        states = self.states
        result = json.loads(response.text)
        for item in result:
            state = item['state']
            daily_state_url = self.daily_state_url_template % state
            current_state_url = self.current_state_url_template % state
            state_item = states[state]
            state_item.update(item)
            state_item.pop('grade', None)
            state_item.pop('total', None)
            state_item['countryShortCode'] = country_short_code
            state_item['currentUrl'] = current_state_url
            state_item['dailyUrl'] = daily_state_url
            yield scrapy.Request(
                daily_state_url,
                self.parse_daily_state,
                meta={'state_item': state_item})

        self.crawled = 1  # 代表爬虫已爬取数据

    def parse_daily_state(self, response):
        meta = response.meta
        state_item = meta['state_item']
        state_item['dailyData'] = json.dumps(
            json.loads(response.text)[::-1])

        yield items.StateItem(**state_item)