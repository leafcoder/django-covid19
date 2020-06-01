from . import models
from rest_framework import serializers
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


class ProvinceSerializer(serializers.HyperlinkedModelSerializer):

    provinceName = serializers.CharField(read_only=True)

    class Meta:
        model = models.Province
        fields = [
            'provinceName', 'provinceShortName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount'
        ]


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = [
            'provinceName', 'cityName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount'
        ]

class CountrySerializer(serializers.HyperlinkedModelSerializer):

    def to_representation(self, inst):
        data = super().to_representation(inst)
        incrVo = data.get('incrVo')
        if incrVo:
            data['incrVo'] = json.loads(incrVo)
        return data

    class Meta:
        model = models.Country
        fields = [
            'continents', 'countryShortCode', 'countryName',
            'countryFullName', 'currentConfirmedCount', 'confirmedCount',
            'suspectedCount', 'curedCount', 'deadCount', 'incrVo'
        ]


class StateSerializer(serializers.ModelSerializer):

    countryShortCode = serializers.CharField()
    currentConfirmedCount = serializers.SerializerMethodField()
    confirmedCount = serializers.IntegerField(source='positive')
    curedCount = serializers.IntegerField(source='recovered')
    deadCount = serializers.IntegerField(source='death')
    suspectedCount = serializers.IntegerField(source='pending')

    def get_currentConfirmedCount(self, obj):
        positive = obj.positive if obj.positive else 0
        death = obj.death if obj.death else 0
        recovered = obj.recovered if obj.recovered else 0
        return positive - death - recovered

    class Meta:
        model = models.State
        fields = [
            'currentConfirmedCount', 'confirmedCount', 'curedCount',
            'deadCount', 'suspectedCount', 'stateName', 'state',
            'countryShortCode', 'dailyUrl', 'currentUrl'
        ]


class StateRawSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.State
        exclude = ('id', 'dailyData')


class StateDailySerializer(serializers.Serializer):

    state = serializers.CharField()
    date = serializers.CharField()
    stateName = serializers.CharField()
    countryShortCode = serializers.CharField()

    currentConfirmedCount = serializers.IntegerField()
    confirmedCount = serializers.IntegerField()
    curedCount = serializers.IntegerField()
    deadCount = serializers.IntegerField()
    suspectedCount = serializers.IntegerField()

    currentConfirmedIncr = serializers.IntegerField()
    confirmedIncr = serializers.IntegerField()
    curedIncr = serializers.IntegerField()
    deadIncr = serializers.IntegerField()
    suspectedIncr = serializers.IntegerField()
