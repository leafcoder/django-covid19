# -*- coding: utf-8 -*-
# @Author: zhanglei3
# @Date:   2020-04-08 09:08:13
# @Last Modified by:   leafcoder
# @Last Modified time: 2020-04-29 13:51:25

"""丁香园数据源"""

import json
import scrapy
import logging
from scrapy.selector import Selector
from .. import items

from django.utils.timezone import datetime, make_aware

logger = logging.getLogger()

class DXYSpider(scrapy.Spider):

    name = "dxy"
    allowed_domains = ["ncov.dxy.cn"]
    start_urls = [
        "http://ncov.dxy.cn/ncovh5/view/pneumonia",
    ]

    def parse(self, response):
        sel = Selector(response)
        scripts = sel.xpath('//script')

        # 判断是否需要保存抓取的数据
        statistics = self.get_dict(scripts, '#getStatisticsService')
        createTime = make_aware(
            datetime.fromtimestamp(statistics['createTime'] / 1000.0))
        modifyTime = make_aware(
            datetime.fromtimestamp(statistics['modifyTime'] / 1000.0))
        qs = items.CrawlerItem.django_model.objects.all().order_by('-id')
        if qs.count() > 1 and qs[1].modifyTime == modifyTime:
            logger.info('Data does not change.')
            self.crawler.delete()
            self.crawler = None
            return
        self.crawler.createTime = createTime
        self.crawler.modifyTime = modifyTime
        self.crawler.save()

        # 统计信息
        statistics = self.parse_statistics(statistics)
        for item in statistics:
            yield item

        # 国内数据
        provinces = self.get_list(scripts, '#getAreaStat')
        for province in provinces:
            cities = province.pop('cities', [])
            province = items.ProvinceItem(**province)
            yield province
            for city in cities:
                location_id = province['locationId']
                yield items.CityItem(province=location_id, **city)

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
            country['incrVo'] = json.dumps(country['incrVo'])
            yield items.CountryItem(**country)

        # 时间线事件，id=“getTimelineService2” 为英文内容
        timelines = self.get_list(scripts, '#getTimelineService1')
        for item in timelines:
            timeline = {}
            for key in ('title', 'summary', 'infoSource', 'sourceUrl',
                        'pubDate', 'pubDateStr'):
                timeline[key] = item.get(key)
            yield items.TimelineItem(**timeline)

        # 建议，id=“#getIndexRecommendList2” 为英文内容
        recommends = self.get_list(
            scripts, '#getIndexRecommendListundefined')
        for item in recommends:
            recommend = {}
            for key in ('title', 'linkUrl', 'imgUrl', 'countryType',
                        'contentType', 'recordStatus', 'sort'):
                recommend[key] = item.get(key)
            yield items.RecommendItem(**recommend)

        # WHO 文章
        item = self.get_dict(scripts, '#fetchWHOArticle')
        article = {}
        for key in ('title', 'linkUrl', 'imgUrl'):
            article[key] = item.get(key)
        yield items.WHOArticleItem(**article)

        # wiki
        wiki_result = self.get_dict(scripts, '#getWikiList')
        wikis = wiki_result['result']
        for item in wikis:
            wiki = {}
            for key in ('title', 'linkUrl', 'imgUrl', 'description'):
                wiki[key] = item.get(key)
            yield items.WikiItem(**wiki)

        # 购物指南
        guides = self.get_list(scripts, '#fetchGoodsGuide')
        for item in guides:
            guide = {}
            for key in ('categoryName', 'title', 'recordStatus',
                        'contentImgUrls'):
                guide[key] = item.get(key)
            yield items.GoodsGuideItem(**guide)

        # 辟谣与防护
        rumors = self.get_list(scripts, '#getIndexRumorList')
        for item in rumors:
            rumor = {}
            for key in ('title', 'mainSummary', 'summary', 'body',
                        'sourceUrl', 'score', 'rumorType'):
                rumor[key] = item.get(key)
            yield items.RumorItem(**rumor)

    def parse_statistics(self, data):
        statistics = data['globalStatistics']
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount'):
            item[key] = statistics.get(key, 0)
        item['countryType'] = items.StatisticsItem.django_model.GLOBAL
        yield items.StatisticsItem(**item)

        statistics = data['foreignStatistics']
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount'):
            item[key] = statistics.get(key, 0)
        item['countryType'] \
            = items.StatisticsItem.django_model.INTERNATIONAL
        yield items.StatisticsItem(**item)

        statistics = data
        item = {}
        for key in (
                'currentConfirmedCount', 'curedCount', 'confirmedCount',
                'seriousCount', 'suspectedCount', 'deadCount'):
            item[key] = statistics.get(key, 0)
        item['countryType'] = items.StatisticsItem.django_model.DOMESTIC
        yield items.StatisticsItem(**item)

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
        yield items.NoticeItem(**item)

    def get_list(self, scripts, data_id):
        ret = scripts.css(data_id).re(r'(\[.+\])')
        return json.loads(ret[0])

    def get_dict(self, scripts, data_id):
        ret = scripts.css(data_id).re(r'\=\s*(\{.+\})\}catch\(e\)\{\}')
        return json.loads(ret[0])
