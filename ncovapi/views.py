from django.db.models import Q, Sum
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from .serializers import LatestStatisticsSerializer, StatisticsSerializer, \
                         CitySerializer, ProvinceSerializer, \
                         CountrySerializer, RecommendSerializer, \
                         TimelineSerializer
from .models import Crawler, Statistics, WHOArticle, Recommend, \
                    City, Province, Country
from .filters import CityFilter, ProvinceFilter, CountryFilter

from collections import OrderedDict
import json

TIMEOUT = 60 * 60

class LatestStatisticsView(APIView):

    """最新统计信息"""

    def get_object(self):
        crawler = Crawler.objects.exclude(
            modifyTime__isnull=True).order_by('-id').first()
        if crawler is None:
            raise Http404
        result = {}
        insts = Statistics.objects.filter(crawler=crawler).all()
        for inst in insts:
            item = {}
            item['currentConfirmedCount'] = inst.currentConfirmedCount
            item['confirmedCount'] = inst.confirmedCount
            item['suspectedCount'] = inst.suspectedCount
            item['seriousCount'] = inst.seriousCount
            item['curedCount'] = inst.curedCount
            item['deadCount'] = inst.deadCount
            item['currentConfirmedIncr'] = inst.currentConfirmedIncr
            item['confirmedIncr'] = inst.confirmedIncr
            item['suspectedIncr'] = inst.suspectedIncr
            item['curedIncr'] = inst.curedIncr
            item['deadIncr'] = inst.deadIncr
            countryType = inst.countryType
            if countryType == Statistics.GLOBAL:
                result['globalStatistics'] = item
            elif countryType == Statistics.DOMESTIC:
                result['domesticStatistics'] = item
            elif countryType == Statistics.INTERNATIONAL:
                result['internationalStatistics'] = item
        result['createTime'] = crawler.createTime
        result['modifyTime'] = crawler.modifyTime
        result['remarks'] = []
        result['notes'] = []
        result['generalRemark'] = ''
        notice = crawler.notices.first()
        if notice:
            result['remarks'] = notice.remarks
            result['notes'] = notice.notes
            result['generalRemark'] = notice.generalRemark
        try:
            article = crawler.WHO_article
        except WHOArticle.DoesNotExist:
            result['WHOArticle'] = None
        else:
            result['WHOArticle'] = {
                'title': article.title,
                'linkUrl': article.linkUrl,
                'imgUrl': article.imgUrl
            }
        result['recommends'] = crawler.recommends.all()
        result['timelines'] = crawler.timelines.all()
        result['wikis'] = crawler.wikis.all()
        result['goodsGuides'] = crawler.goods_guides.all()
        result['rumors'] = crawler.rumors.all()
        return result

    @method_decorator(cache_page(TIMEOUT))
    def get(self, request):
        data = self.get_object()
        serializer = LatestStatisticsSerializer(data)
        return Response(serializer.data)

class StatisticsListView(ListAPIView):

    """统计信息列表"""

    serializer_class = StatisticsSerializer

    def get_queryset(self):
        result = OrderedDict()
        for inst in Statistics.objects.all():
            crawler_id = inst.crawler_id
            country_type = inst.countryType
            if country_type == Statistics.GLOBAL:
                statistics = result.setdefault(crawler_id, {})
                statistics['globalStatistics'] = inst
            elif country_type == Statistics.DOMESTIC:
                statistics = result.setdefault(crawler_id, {})
                statistics['domesticStatistics'] = inst
            elif country_type == Statistics.INTERNATIONAL:
                statistics = result.setdefault(crawler_id, {})
                statistics['internationalStatistics'] = inst
            statistics = result.setdefault(crawler_id, {})
            statistics['modifyTime'] = inst.crawler.modifyTime
            statistics['createTime'] = inst.crawler.createTime
        return reversed(result.values())

    @method_decorator(cache_page(TIMEOUT))
    def dispatch(self, *args, **kwargs):
        return super(StatisticsListView, self).dispatch(*args, **kwargs)

class ProvinceListView(ListAPIView):

    """省列表"""

    serializer_class = ProvinceSerializer
    filter_class = ProvinceFilter

    def get_queryset(self):
        crawler = Crawler.objects.exclude(
            modifyTime__isnull=True).order_by('-id').first()
        queryset = Province.objects.filter(crawler=crawler)
        return queryset

    @method_decorator(cache_page(TIMEOUT))
    def dispatch(self, *args, **kwargs):
        return super(ProvinceListView, self).dispatch(*args, **kwargs)


class ProvinceDailyListView(APIView):

    """省按天返回列表"""

    def get_object(self, provinceShortName):
        crawler = Crawler.objects.exclude(
            modifyTime__isnull=True).order_by('-id').first()
        province = Province.objects.filter(
            crawler=crawler,
            provinceShortName=provinceShortName).first()
        if province is None:
            raise Http404
        return province

    @method_decorator(cache_page(TIMEOUT))
    def get(self, request, provinceShortName):
        province = self.get_object(provinceShortName)
        result = province.dailyData
        result = json.loads(result)
        return Response(result)


class ProvinceRetrieveByNameView(APIView):
    """通过省名获取数据"""

    def get_object(self, provinceShortName):
        crawler = Crawler.objects.exclude(
            modifyTime__isnull=True).order_by('-id').first()
        province = Province.objects.filter(
            crawler=crawler,
            provinceShortName=provinceShortName).first()
        if province is None:
            raise Http404
        return province

    @method_decorator(cache_page(TIMEOUT))
    def get(self, request, provinceShortName):
        province = self.get_object(provinceShortName)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)


class ProvinceRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return Province.objects.get(pk=pk)
        except Province.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(TIMEOUT))
    def get(self, request, pk):
        province = self.get_object(pk)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)


class CountryListView(ListAPIView):

    serializer_class = CountrySerializer
    filter_class = CountryFilter

    def get_queryset(self):
        crawler = Crawler.objects.exclude(
            modifyTime__isnull=True).order_by('-id').first()
        queryset = Country.objects.filter(crawler=crawler)
        return queryset.all()

    @method_decorator(cache_page(TIMEOUT))
    def dispatch(self, *args, **kwargs):
        return super(CountryListView, self).dispatch(*args, **kwargs)


class CountryRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(TIMEOUT))
    def get(self, request, pk):
        country = self.get_object(pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)


class CountryDailyListView(APIView):

    def get_object(self, countryName):
        crawler = Crawler.objects.exclude(
            modifyTime__isnull=True).order_by('-id').first()
        country = Country.objects.filter(
            crawler=crawler, countryName=countryName).first()
        if country is None:
            raise Http404
        return country

    @method_decorator(cache_page(TIMEOUT))
    def get(self, request, countryName):
        country = self.get_object(countryName)
        result = country.dailyData
        result = json.loads(result)
        return Response(result)


class CountryRetrieveByNameView(APIView):

    def get_object(self, countryName):
        crawler = Crawler.objects.exclude(
            modifyTime__isnull=True).order_by('-id').first()
        country = Country.objects.filter(
            crawler=crawler, countryName=countryName).first()
        if country is None:
            raise Http404
        return country

    @method_decorator(cache_page(TIMEOUT))
    def get(self, request, countryName):
        country = self.get_object(countryName)
        serializer = CountrySerializer(country)
        return Response(serializer.data)


class CityListView(ListAPIView):

    serializer_class = CitySerializer
    filter_class = CityFilter

    def get_queryset(self):
        crawler = Crawler.objects.exclude(
            modifyTime__isnull=True).order_by('-id').first()
        queryset = City.objects.filter(crawler=crawler)
        return queryset

    @method_decorator(cache_page(TIMEOUT))
    def dispatch(self, *args, **kwargs):
        return super(CityListView, self).dispatch(*args, **kwargs)


class CityRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return City.objects.get(pk=pk)
        except City.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(TIMEOUT))
    def get(self, request, pk):
        city = self.get_object(pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)


class CityRetrieveByNameView(APIView):

    def get_object(self, cityName):
        crawler = Crawler.objects.exclude(
            modifyTime__isnull=True).order_by('-id').first()
        city = City.objects.filter(
            crawler=crawler, cityName=cityName).first()
        if city is None:
            raise Http404
        return city

    @method_decorator(cache_page(TIMEOUT))
    def get(self, request, cityName):
        city = self.get_object(cityName)
        serializer = CitySerializer(city)
        return Response(serializer.data)