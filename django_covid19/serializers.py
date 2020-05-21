from .models import Statistics, City, Province, Country
from rest_framework import serializers

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
        model = Statistics
        fields = ('globalStatistics', 'domesticStatistics', 'internationalStatistics', 'modifyTime', 'createTime')

class ProvinceSerializer(serializers.HyperlinkedModelSerializer):

    provinceName = serializers.CharField(read_only=True)

    class Meta:
        model = Province
        fields = [
            'provinceName', 'provinceShortName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount'
        ]


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
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
        model = Country
        fields = [
            'continents', 'countryShortCode', 'countryName',
            'countryFullName', 'currentConfirmedCount', 'confirmedCount',
            'suspectedCount', 'curedCount', 'deadCount', 'incrVo'
        ]