# -*- coding: utf-8 -*-
# @Author: zhanglei3
# @Date:   2020-04-08 09:08:13
# @Last Modified by:   leafcoder
# @Last Modified time: 2020-05-30 19:02:49

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

    """data source: https://covidtracking.com/api"""

    name = "covidtracking"
    allowed_domains = ["covidtracking.com"]
    country_short_code = 'USA'
    states = {}

    def start_requests(self):
        apis = [
            'https://covidtracking.com/api/v1/states/current.json',
            'https://covidtracking.com/api/v1/states/daily.json',
            'https://covidtracking.com/api/v1/states/info.json',
            'https://covidtracking.com/api/v1/us/daily.json',
        ]
        yield scrapy.Request(
            'https://covidtracking.com/api/v1/states/info.json',
            self.parse_info)

    def parse_states_current(self, response):
        countryShortCode = self.country_short_code
        states = self.states
        result = json.loads(response.text)
        for item in result:
            state = item['state']
            state_item = states[state]
            state_item.update(item)
            state_item.pop('grade', None)
            state_item.pop('total', None)
            state_item['countryShortCode'] = countryShortCode
            yield scrapy.Request(
                'https://covidtracking.com/api/v1/states/%s/daily.json' \
                    % state,
                self.parse_state_daily,
                meta={
                    'state_item': state_item
                })

    def parse_state_daily(self, response):
        meta = response.meta
        state_item = meta['state_item']
        state_item['dailyData'] = json.dumps(
            json.loads(response.text)[::-1])
        yield items.StateItem(**state_item)

    def parse_info(self, response):
        countryShortCode = self.country_short_code
        states = self.states
        result = json.loads(response.text)
        for item in result:
            state = item['state']
            stateName = item['name']
            stateName = ''.join(stateName.split())
            states[state] = {
                'state': state,
                'countryShortCode': countryShortCode,
                'stateName': stateName
            }
        yield scrapy.Request(
            'https://covidtracking.com/api/v1/states/current.json',
            self.parse_states_current)