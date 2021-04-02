from . import models
from rest_framework import serializers
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

import json

class WHOArticleSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=100)
    linkUrl = serializers.URLField()
    imgUrl = serializers.URLField()


class RecommendSerializer(serializers.Serializer):

    title = serializers.CharField()
    linkUrl = serializers.URLField()
    imgUrl = serializers.URLField()
    contentType = serializers.IntegerField()
    recordStatus = serializers.IntegerField()
    countryType = serializers.IntegerField()


class TimelineSerializer(serializers.Serializer):

    pubDate = serializers.IntegerField()
    pubDateStr = serializers.CharField()
    title = serializers.CharField()
    summary = serializers.CharField()
    infoSource = serializers.CharField()
    sourceUrl = serializers.URLField()


class WikiSerializer(serializers.Serializer):

    title = serializers.CharField()
    linkUrl = serializers.URLField()
    imgUrl = serializers.URLField()
    description = serializers.CharField()


class GoodsGuideSerializer(serializers.Serializer):

    title = serializers.CharField()
    categoryName = serializers.CharField()
    recordStatus = serializers.IntegerField()
    contentImgUrls = serializers.ListField(
        serializers.URLField(max_length=200), max_length=10)


class RumorSerializer(serializers.Serializer):

    title = serializers.CharField()
    mainSummary = serializers.CharField()
    summary = serializers.CharField()
    body = serializers.CharField()
    sourceUrl = serializers.URLField()
    score = serializers.IntegerField()
    rumorType = serializers.IntegerField()


class LatestStatisticsSerializer(serializers.Serializer):

    globalStatistics = serializers.DictField()
    domesticStatistics = serializers.DictField()
    internationalStatistics = serializers.DictField()
    remarks = serializers.JSONField()
    notes = serializers.ListField(
       child=serializers.CharField(max_length=100), max_length=10
    )
    generalRemark = serializers.CharField()
    WHOArticle = WHOArticleSerializer()
    recommends = RecommendSerializer(many=True)
    timelines = TimelineSerializer(many=True)
    wikis = WikiSerializer(many=True)
    goodsGuides = GoodsGuideSerializer(many=True)
    rumors = RumorSerializer(many=True)
    modifyTime = serializers.DateTimeField()
    createTime = serializers.DateTimeField()


class StatisticsSerializer(serializers.Serializer):

    globalStatistics = serializers.DictField()
    domesticStatistics = serializers.DictField()
    internationalStatistics = serializers.DictField()
    modifyTime = serializers.DateTimeField()
    createTime = serializers.DateTimeField()

    class Meta:
        model = models.Statistics
        fields = (
            'globalStatistics', 'domesticStatistics',
            'internationalStatistics', 'modifyTime', 'createTime'
        )


class CountrySerializer(serializers.ModelSerializer):

    def to_representation(self, inst):
        data = super().to_representation(inst)
        incrVo = data.get('incrVo')
        if incrVo:
            data['incrVo'] = json.loads(incrVo)
        return data

    class Meta:
        model = models.Country
        fields = [
            'continents', 'countryCode', 'countryName',
            'currentConfirmedCount', 'confirmedCount',
            'suspectedCount', 'curedCount', 'deadCount', 'incrVo'
        ]


class CountryDailySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = ['dailyData']


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Province
        fields = [
            'countryCode', 'provinceCode', 'provinceName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount', 'dailyUrl', 'currentUrl'
        ]


class ProvinceDailySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Province
        fields = ['provinceCode', 'provinceName', 'dailyData']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = [
            'provinceCode', 'provinceName', 'cityName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount'
        ]


class CountryCodeSerializer(serializers.ModelSerializer):

    # 丁香园支持的国家编码
    DXY_COUNTRY_CODES = (
        'ABW', 'AFG', 'AGO', 'AI', 'ALB', 'AND', 'ARE', 'ARG', 'ARM', 'ATG',
        'AUS', 'AUT', 'AZE', 'BDI', 'BEL', 'BEN', 'BES', 'BFA', 'BGD',
        'BGR', 'BHR', 'BHS', 'BIH', 'BL', 'BLR', 'BLZ', 'BMU', 'BOL', 'BRA',
        'BRB', 'BRN', 'BTN', 'BWA', 'CAF', 'CAN', 'CHE', 'CHL', 'CHN',
        'CIB', 'CIV', 'CMR', 'CNMI', 'COD', 'COG', 'COL', 'COM', 'CPV',
        'CRI', 'CUB', 'CW', 'CYM', 'CYP', 'CZE', 'DEU', 'DJI', 'DMA', 'DNK',
        'DOM', 'DZA', 'ECU', 'EGY', 'ERI', 'ESP', 'EST', 'ETH', 'FIN',
        'FJI', 'FLK', 'FO', 'FRA', 'GAB', 'GBN', 'GBR', 'GEO', 'GG', 'GHA',
        'GIN', 'GLP', 'GMB', 'GNQ', 'GRC', 'GRD', 'GRL', 'GTM', 'GU', 'GUF',
        'GUY', 'HND', 'HRV', 'HTI', 'HUN', 'IDN', 'IND', 'IRL', 'IRN',
        'IRQ', 'ISL', 'ISR', 'ITA', 'JAM', 'JE', 'JOR', 'JPN', 'KAZ', 'KEN',
        'KGZ', 'KHM', 'KNA', 'KOR', 'KWT', 'LAO', 'LBN', 'LBR', 'LBY',
        'LCA', 'LIE', 'LKA', 'LSO', 'LTU', 'LUX', 'LVA', 'MAR', 'MCO',
        'MDA', 'MDG', 'MDV', 'MEX', 'MKD', 'MLI', 'MLT', 'MMR', 'MNE',
        'MNG', 'MOZ', 'MRT', 'MS', 'MTQ', 'MUS', 'MWI', 'MYS', 'MYT',
        'Mann', 'NAM', 'NCL', 'NER', 'NGA', 'NIC', 'NLD', 'NOR', 'NPL',
        'NZL', 'OMN', 'PAK', 'PAN', 'PER', 'PHL', 'PNG', 'POL', 'PRI',
        'PRT', 'PRY', 'PSE', 'PYF', 'Princess', 'QAT', 'REU', 'ROU', 'RUS',
        'RWA', 'SAU', 'SDN', 'SEN', 'SGP', 'SLE', 'SLV', 'SMR', 'SOM',
        'SPM', 'SRB', 'SSD', 'STP', 'SUR', 'SVK', 'SVN', 'SWE', 'SWZ',
        'SYC', 'SYR', 'Saint Martin', 'Sint Maarten', 'TCA', 'TCD', 'TGO',
        'THA', 'TJK', 'TLS', 'TTO', 'TUN', 'TUR', 'TZA', 'UGA', 'UKR',
        'URY', 'USA', 'USVI', 'UZB', 'VAT', 'VCT', 'VEN', 'VG', 'VNM',
        'YEM', 'ZAF', 'ZMB', 'ZWE')

    def to_representation(self, inst):
        data = super().to_representation(inst)
        context = self.context
        request = context['request']
        countryCode = data['countryCode']
        if countryCode not in self.DXY_COUNTRY_CODES:
            data['existApi'] = False
            data['currentApi'] = None
            data['dailyApi'] = None
            return data
        kwargs = { 'countryCode': countryCode }
        data['existApi'] = True
        data['currentApi'] = request.build_absolute_uri(reverse(
            'django_covid19:country-detail', kwargs=kwargs))
        data['dailyApi'] = request.build_absolute_uri(reverse(
            'django_covid19:country-daily', kwargs=kwargs))
        return data

    class Meta:
        model = models.CountryCode
        fields = [
            'numericCode', 'countryCode', 'shortCountryCode', 'countryName',
            'englishCountryName', 'englishCountryFullName', 'comment'
        ]
