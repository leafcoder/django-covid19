# -*- coding: utf-8 -*-
# @Author: zhanglei3
# @Date:   2020-04-08 09:08:13
# @Last Modified by:   leafcoder
# @Last Modified time: 2020-04-17 22:51:26

"""丁香园数据源"""

import json
import scrapy
from scrapy.selector import Selector
from ..items import StatisticsItem, NoticeItem, WHOArticleItem, \
                    RecommendItem, ProvinceItem, CountryItem, CityItem, \
                    TimelineItem, WikiItem, GoodsGuideItem, RumorItem

from django.utils.timezone import datetime, make_aware

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

        # 时间线事件，id=“getTimelineService2” 为英文内容
        timelines = self.get_list(scripts, '#getTimelineService1')
        for item in timelines:
            timeline = {}
            for key in ('title', 'summary', 'infoSource', 'sourceUrl',
                        'pubDate', 'pubDateStr'):
                timeline[key] = item.get(key)
            yield TimelineItem(**timeline)


        # 建议，id=“#getIndexRecommendList2” 为英文内容
        recommends = self.get_list(
            scripts, '#getIndexRecommendListundefined')
        for item in recommends:
            recommend = {
                'title': item['title'],
                'linkUrl': item['linkUrl'],
                'imgUrl': item['imgUrl'],
                'countryType': item['countryType'],
                'contentType': item['contentType'],
                'recordStatus': item['recordStatus'],
                'sort': item['sort']
            }
            yield RecommendItem(**recommend)

        # # WHO 文章
        article = self.get_dict(scripts, '#fetchWHOArticle')
        yield WHOArticleItem(
            title=article['title'], linkUrl=article['linkUrl'],
            imgUrl=article['imgUrl'])

        # wiki
        wiki_result = self.get_dict(scripts, '#getWikiList')
        wikis = wiki_result['result']
        for item in wikis:
            wiki = {}
            for key in ('title', 'linkUrl', 'imgUrl', 'description'):
                wiki[key] = item.get(key)
            yield WikiItem(**wiki)

        # 购物指南
        guides = self.get_list(scripts, '#fetchGoodsGuide')
        for item in guides:
            guide = {}
            for key in ('categoryName', 'title', 'recordStatus',
                        'contentImgUrls'):
                guide[key] = item.get(key)
            yield GoodsGuideItem(**guide)

        # 辟谣与防护
        rumors = self.get_list(scripts, '#getIndexRumorList')
        for item in rumors:
            rumor = {}
            for key in ('title', 'mainSummary', 'summary', 'body',
                        'sourceUrl', 'score', 'rumorType'):
                rumor[key] = item.get(key)
            yield RumorItem(**rumor)

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
        item['countryType'] = StatisticsItem.django_model.INTERNATIONAL
        yield StatisticsItem(**item)


        statistics = data
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount'):
            item[key] = statistics.get(key, 0)
        item['countryType'] = StatisticsItem.django_model.DOMESTIC
        yield StatisticsItem(**item)


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

        item = {
            'remarks': remarks,
            'notes': notes,
            'generalRemark': data.get('generalRemark')
        }
        yield NoticeItem(**item)


        self.crawler.createTime \
            = make_aware(datetime.fromtimestamp(data['createTime'] / 1000.0))
        self.crawler.modifyTime \
            = make_aware(datetime.fromtimestamp(data['modifyTime'] / 1000.0))
        self.crawler.save()
