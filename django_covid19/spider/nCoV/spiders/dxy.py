# -*- coding: utf-8 -*-
# @Author: zhanglei3
# @Date:   2020-04-08 09:08:13
# @Last Modified by:   leafcoder
# @Last Modified time: 2020-05-21 10:49:20

"""丁香园数据源"""

import json
import scrapy
import logging
from scrapy.selector import Selector

from .. import items

from django.core.cache import cache
from django.utils.timezone import datetime, make_aware

logger = logging.getLogger()

class DXYSpider(scrapy.Spider):

    name = "dxy"
    allowed_domains = ["ncov.dxy.cn", "file1.dxycdn.com"]
    start_urls = [
        "http://ncov.dxy.cn/ncovh5/view/pneumonia",
    ]

    def parse(self, response):
        object_id = self.object_id
        spider_id = cache.get('running_spider_id')
        if object_id != spider_id:
            logger.info('Spider is running.')
            self.crawled = 0
            return

        sel = Selector(response)
        scripts = sel.xpath('//script')

        # 判断是否需要保存抓取的数据
        statistics = self.get_dict(scripts, '#getStatisticsService')
        createTime = make_aware(
            datetime.fromtimestamp(statistics['createTime'] / 1000.0))
        modifyTime = make_aware(
            datetime.fromtimestamp(statistics['modifyTime'] / 1000.0))
        qs = items.StatisticsItem.django_model.objects.all().order_by('-id')
        if qs.count() > 1 and qs[0].modifyTime == modifyTime:
            logger.info('Data does not change.')
            self.crawled = 0
            return

        # 统计信息
        statistics = self.explain_statistics(statistics)
        statistics['createTime'] = createTime
        statistics['modifyTime'] = modifyTime

        # 国内数据
        provinces = self.get_list(scripts, '#getAreaStat')
        for province in provinces:
            cities = province.pop('cities', [])
            yield scrapy.Request(
                province['statisticsData'],
                callback=self.parse_province_statistics_data,
                meta={
                    'province': province,
                    'cities': cities
                }
            )

        # 时间线事件，id=“getTimelineService2” 为英文内容
        timelines = self.get_list(scripts, '#getTimelineService1')
        result = []
        for item in timelines:
            timeline = {}
            for key in ('title', 'summary', 'infoSource', 'sourceUrl',
                        'pubDate', 'pubDateStr'):
                timeline[key] = item.get(key)
            result.append(timeline)
        statistics['timelines'] = json.dumps(result)

        # 建议，id=“#getIndexRecommendList2” 为英文内容
        recommends = self.get_list(
            scripts, '#getIndexRecommendListundefined')
        result = []
        for item in recommends:
            recommend = {}
            for key in ('title', 'linkUrl', 'imgUrl', 'countryType',
                        'contentType', 'recordStatus', 'sort'):
                recommend[key] = item.get(key)
            result.append(recommend)
        statistics['recommends'] = json.dumps(result)

        # WHO 文章
        item = self.get_dict(scripts, '#fetchWHOArticle')
        article = {}
        for key in ('title', 'linkUrl', 'imgUrl'):
            article[key] = item.get(key)
        statistics['WHOArticle'] = json.dumps(article)

        # wiki
        wiki_result = self.get_dict(scripts, '#getWikiList')
        wikis = wiki_result['result']
        result = []
        for item in wikis:
            wiki = {}
            for key in ('title', 'linkUrl', 'imgUrl', 'description'):
                wiki[key] = item.get(key)
            result.append(wiki)
        statistics['wikis'] = json.dumps(result)


        # 购物指南
        guides = self.get_list(scripts, '#fetchGoodsGuide')
        result = []
        for item in guides:
            guide = {}
            for key in ('categoryName', 'title', 'recordStatus',
                        'contentImgUrls'):
                guide[key] = item.get(key)
            result.append(guide)
        statistics['goodsGuides'] = json.dumps(result)

        # 辟谣与防护
        rumors = self.get_list(scripts, '#getIndexRumorList')
        result = []
        for item in rumors:
            rumor = {}
            for key in ('title', 'mainSummary', 'summary', 'body',
                        'sourceUrl', 'score', 'rumorType'):
                rumor[key] = item.get(key)
            result.append(rumor)
        statistics['rumors'] = json.dumps(result)
        yield statistics

        # 国外数据
        countries = self.get_list(
            scripts, '#getListByCountryTypeService2true')
        for country in countries:
            country.pop('id', None)
            country['countryName'] = country.pop('provinceName', None)
            country['provinceName'] = ''
            country.pop('countryType')
            country.pop('cityName')
            country.pop('provinceId')
            country.pop('provinceName')
            country.pop('provinceShortName')
            country.pop('modifyTime', None)
            country.pop('createTime', None)
            country['incrVo'] = json.dumps(country.get('incrVo', {}))
            statistics_data = country.get('statisticsData')
            if statistics_data:
                yield scrapy.Request(
                    statistics_data,
                    callback=self.parse_country_statistics_data,
                    meta={
                        'country': country
                    }
                )
            else:
                yield items.CountryItem(dailyData=[], **country)

        self.crawled = 1  # 代表爬虫已爬取数据

    def parse_province_statistics_data(self, response):
        result = json.loads(response.text)
        data = json.dumps(result['data'])
        meta = response.meta
        cities = meta['cities']
        province = meta['province']
        yield items.ProvinceItem(dailyData=data, **province)
        for city in cities:
            location_id = province['locationId']
            yield items.CityItem(province=location_id, **city)

    def parse_country_statistics_data(self, response):
        result = json.loads(response.text)
        data = json.dumps(result['data'])
        meta = response.meta
        country = meta['country']
        yield items.CountryItem(dailyData=data, **country)

    def explain_statistics(self, data):
        statistics = data['globalStatistics']
        instance = {}
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount',
                'currentConfirmedIncr', 'curedIncr', 'confirmedIncr',
                'suspectedIncr', 'deadIncr'):
            item[key] = statistics.get(key, 0)
        instance['globalStatistics'] = json.dumps(item)

        statistics = data['foreignStatistics']
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount',
                'currentConfirmedIncr', 'curedIncr', 'confirmedIncr',
                'suspectedIncr', 'deadIncr'):
            item[key] = statistics.get(key, 0)
        instance['internationalStatistics'] = json.dumps(item)


        statistics = data
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount',
                'currentConfirmedIncr', 'curedIncr', 'confirmedIncr',
                'suspectedIncr', 'deadIncr'):
            item[key] = statistics.get(key, 0)
        instance['domesticStatistics'] = json.dumps(item)

        # Remark and Note
        remarks = []
        for key in ('remark1', 'remark2', 'remark3', 'remark4', 'remark5'):
            remark = data.get(key)
            if remark:
                remarks.append(remark)

        notes = []
        for key in ('note1', 'note2', 'note3'):
            note = data.get(key)
            if note:
                notes.append(note)

        instance['remarks'] = json.dumps(remarks)
        instance['notes'] = json.dumps(notes)
        instance['generalRemark'] = data.get('generalRemark')
        return items.StatisticsItem(**instance)

    def get_list(self, scripts, data_id):
        ret = scripts.css(data_id).re(r'(\[.+\])')
        return json.loads(ret[0])

    def get_dict(self, scripts, data_id):
        ret = scripts.css(data_id).re(r'\=\s*(\{.+\})\}catch\(e\)\{\}')
        return json.loads(ret[0])
