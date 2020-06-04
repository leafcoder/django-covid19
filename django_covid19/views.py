from django.http import Http404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from . import filters
from . import models
from . import serializers
from .settings import CACHE_PAGE_TIMEOUT

import json

DEFAULT_COUNTRY_CODE = 'CHN'

class LatestStatisticsView(APIView):

    """最新统计信息"""

    def get_object(self):
        result = {}
        inst = models.Statistics.objects.order_by('-id').first()
        if inst is None:
            raise Http404
        return inst

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='statistics-lastest'))
    def get(self, request):
        obj = self.get_object()
        result = {}
        for field in models.Statistics._meta.fields:
            name = field.attname
            value = getattr(obj, name)
            if name not in models.Statistics.JSON_FIELDS:
                result[name] = value
                continue
            try:
                value = json.loads(value)
            except ValueError:
                value = None
            result[name] = value
        serializer = serializers.LatestStatisticsSerializer(result)
        return Response(serializer.data)


class StatisticsListView(ListAPIView):

    """统计信息列表"""

    serializer_class = serializers.StatisticsSerializer

    def get_queryset(self):
        result = []
        qs = models.Statistics.objects.all().order_by('-modifyTime')
        values_fields = (
            'globalStatistics', 'domesticStatistics',
            'internationalStatistics', 'modifyTime', 'createTime')
        for item in qs.values_list(*values_fields):
            item = dict(zip(values_fields, item))
            statistics = {}
            for name, value in item.items():
                if name not in models.Statistics.JSON_FIELDS:
                    statistics[name] = value
                    continue
                try:
                    value = json.loads(value)
                except ValueError:
                    value = None
                statistics[name] = value
            result.append(statistics)
        return result

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='statistics-list'))
    def dispatch(self, *args, **kwargs):
        return super(StatisticsListView, self).dispatch(*args, **kwargs)


class CountryListView(ListAPIView):

    serializer_class = serializers.CountrySerializer
    filter_class = filters.CountryFilter

    def get_queryset(self):
        return models.Country.objects.all().order_by(
            'continents', 'countryCode')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-list'))
    def dispatch(self, *args, **kwargs):
        return super(CountryListView, self).dispatch(*args, **kwargs)


class CountryListDailyView(ListAPIView):

    serializer_class = serializers.CountryDailySerializer
    filter_class = filters.CountryFilter

    def get_queryset(self):
        return models.Country.objects.all().order_by(
            'continents', 'countryCode')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        result = []
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for item in serializer.data:
                dailyData = json.loads(item['dailyData'])
                result.extend(dailyData)
            return self.get_paginated_response(result)

        serializer = self.get_serializer(queryset, many=True)
        for item in serializer.data:
            dailyData = json.loads(item['dailyData'])
            result.extend(dailyData)
        return Response(result)

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-list-daily'))
    def dispatch(self, *args, **kwargs):
        return super(CountryListDailyView, self).dispatch(*args, **kwargs)


class CountryRetrieveView(APIView):

    def get_object(self, countryCode):
        country = models.Country.objects.filter(
            countryCode=countryCode).first()
        if country is None:
            raise Http404
        return country

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-detail'))
    def get(self, request, countryCode):
        country = self.get_object(countryCode)
        serializer = serializers.CountrySerializer(country)
        return Response(serializer.data)


class CountryDailyView(APIView):

    def get_object(self, countryCode):
        country = models.Country.objects.filter(
            countryCode=countryCode).first()
        if country is None:
            raise Http404
        return country

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-daily-list'))
    def get(self, request, countryCode):
        country = self.get_object(countryCode)
        result = country.dailyData
        result = json.loads(result)
        return Response(result)


class ProvinceListView(ListAPIView):

    """省列表"""

    serializer_class = serializers.ProvinceSerializer
    filter_class = filters.ProvinceFilter

    def get_queryset(self):
        countryCode = self.kwargs['countryCode']
        if not countryCode:
            countryCode = DEFAULT_COUNTRY_CODE
        return models.Province.objects.filter(
            countryCode=countryCode).order_by('provinceCode')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-list'))
    def dispatch(self, *args, **kwargs):
        return super(ProvinceListView, self).dispatch(*args, **kwargs)


class ProvinceDailyView(APIView):

    """省按天返回列表"""

    def get_object(self, countryCode, provinceCode):
        province = models.Province.objects.filter(
            countryCode=countryCode, provinceCode=provinceCode).first()
        if province is None:
            raise Http404
        return province

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-daily-list'))
    def get(self, request, countryCode, provinceCode):
        if countryCode is None:
            countryCode = DEFAULT_COUNTRY_CODE
        province = self.get_object(countryCode, provinceCode)
        result = province.dailyData
        result = json.loads(result)
        return Response(result)


class ProvinceDailyByNameView(APIView):

    """省按天返回列表"""

    def get_object(self, countryCode, provinceName):
        province = models.Province.objects.filter(
            countryCode=countryCode, provinceName=provinceName).first()
        if province is None:
            raise Http404
        return province

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-daily-list-by-name'))
    def get(self, request, countryCode, provinceName):
        if countryCode is None:
            countryCode = DEFAULT_COUNTRY_CODE
        province = self.get_object(countryCode, provinceName)
        result = province.dailyData
        result = json.loads(result)
        return Response(result)


class ProvinceListDailyView(ListAPIView):

    serializer_class = serializers.ProvinceDailySerializer
    filter_class = filters.ProvinceFilter

    def get_queryset(self):
        countryCode = self.kwargs['countryCode']
        if not countryCode:
            countryCode = DEFAULT_COUNTRY_CODE
        return models.Province.objects.filter(
            countryCode=countryCode).order_by('provinceCode')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        result = []
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for item in serializer.data:
                dailyData = json.loads(item['dailyData'])
                result.extend(dailyData)
            return self.get_paginated_response(result)

        serializer = self.get_serializer(queryset, many=True)
        for item in serializer.data:
            dailyData = json.loads(item['dailyData'])
            result.extend(dailyData)
        return Response(result)

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-list-daily'))
    def dispatch(self, *args, **kwargs):
        return super(ProvinceListDailyView, self).dispatch(*args, **kwargs)


class ProvinceRetrieveView(APIView):

    """通过省编码获取数据"""

    def get_object(self, countryCode, provinceCode):
        province = models.Province.objects.filter(
            countryCode=countryCode, provinceCode=provinceCode).first()
        if province is None:
            raise Http404
        return province

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-detail'))
    def get(self, request, countryCode, provinceCode):
        if countryCode is None:
            countryCode = DEFAULT_COUNTRY_CODE
        province = self.get_object(countryCode, provinceCode)
        serializer = serializers.ProvinceSerializer(province)
        return Response(serializer.data)


class ProvinceRetrieveByNameView(APIView):

    """通过省名获取数据"""

    def get_object(self, countryCode, provinceName):
        province = models.Province.objects.filter(
            countryCode=countryCode, provinceName=provinceName).first()
        if province is None:
            raise Http404
        return province

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-detail-by-name'))
    def get(self, request, countryCode, provinceName=None):
        if countryCode is None:
            countryCode = DEFAULT_COUNTRY_CODE
        province = self.get_object(countryCode, provinceName)
        serializer = serializers.ProvinceSerializer(province)
        return Response(serializer.data)


class CityListView(ListAPIView):

    serializer_class = serializers.CitySerializer
    filter_class = filters.CityFilter

    def get_queryset(self):
        countryCode = self.kwargs['countryCode']
        if not countryCode:
            countryCode = DEFAULT_COUNTRY_CODE
        return models.City.objects.filter(
            countryCode=countryCode).order_by('provinceCode', 'cityName')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='city-list'))
    def dispatch(self, *args, **kwargs):
        return super(CityListView, self).dispatch(*args, **kwargs)


class CityRetrieveByNameView(APIView):

    def get_object(self, countryCode, cityName):
        city = models.City.objects.filter(
            countryCode=countryCode, cityName=cityName).first()
        if city is None:
            raise Http404
        return city

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='city-detail-by-name'))
    def get(self, request, countryCode, cityName):
        if countryCode is None:
            countryCode = DEFAULT_COUNTRY_CODE
        city = self.get_object(countryCode, cityName)
        serializer = serializers.CitySerializer(city)
        return Response(serializer.data)
