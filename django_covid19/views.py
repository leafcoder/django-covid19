from django.http import Http404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .serializers import LatestStatisticsSerializer, StatisticsSerializer, \
                         CitySerializer, ProvinceSerializer, \
                         CountrySerializer
from .models import Statistics, City, Province, Country
from .filters import CityFilter, ProvinceFilter, CountryFilter
from .settings import CACHE_PAGE_TIMEOUT

import json


class LatestStatisticsView(APIView):

    """最新统计信息"""

    def get_object(self):
        result = {}
        inst = Statistics.objects.order_by('-id').first()
        if inst is None:
            raise Http404
        return inst

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='statistics-lastest'))
    def get(self, request):
        obj = self.get_object()
        result = {}
        for field in Statistics._meta.fields:
            name = field.attname
            value = getattr(obj, name)
            if name not in Statistics.JSON_FIELDS:
                result[name] = value
                continue
            try:
                value = json.loads(value)
            except ValueError:
                value = None
            result[name] = value
        serializer = LatestStatisticsSerializer(result)
        return Response(serializer.data)


class StatisticsListView(ListAPIView):

    """统计信息列表"""

    serializer_class = StatisticsSerializer

    def get_queryset(self):
        result = []
        qs = Statistics.objects.all().order_by('-modifyTime')
        values_fields = (
            'globalStatistics', 'domesticStatistics',
            'internationalStatistics', 'modifyTime', 'createTime')
        for item in qs.values_list(*values_fields):
            item = dict(zip(values_fields, item))
            statistics = {}
            for name, value in item.items():
                if name not in Statistics.JSON_FIELDS:
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


class ProvinceListView(ListAPIView):

    """省列表"""

    serializer_class = ProvinceSerializer
    filter_class = ProvinceFilter

    def get_queryset(self):
        return Province.objects.all().order_by('provinceName')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-list'))
    def dispatch(self, *args, **kwargs):
        return super(ProvinceListView, self).dispatch(*args, **kwargs)


class ProvinceDailyListView(APIView):

    """省按天返回列表"""

    def get_object(self, provinceShortName):
        province = Province.objects.filter(
            provinceShortName=provinceShortName).first()
        if province is None:
            raise Http404
        return province

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-daily-list'))
    def get(self, request, provinceShortName):
        province = self.get_object(provinceShortName)
        result = province.dailyData
        result = json.loads(result)
        return Response(result)


class ProvinceRetrieveByNameView(APIView):
    """通过省名获取数据"""

    def get_object(self, provinceShortName):
        province = Province.objects.filter(
            provinceShortName=provinceShortName).first()
        if province is None:
            raise Http404
        return province

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-detail-by-name'))
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

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-detail'))
    def get(self, request, pk):
        province = self.get_object(pk)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)


class CountryListView(ListAPIView):

    serializer_class = CountrySerializer
    filter_class = CountryFilter

    def get_queryset(self):
        return Country.objects.all().order_by(
            'continents', 'countryShortCode')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-list'))
    def dispatch(self, *args, **kwargs):
        return super(CountryListView, self).dispatch(*args, **kwargs)


class CountryRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-detail'))
    def get(self, request, pk):
        country = self.get_object(pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)


class CountryDailyListView(APIView):

    def get_object(self, countryName):
        country = Country.objects.filter(countryName=countryName).first()
        if country is None:
            raise Http404
        return country

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-daily-list'))
    def get(self, request, countryName):
        country = self.get_object(countryName)
        result = country.dailyData
        result = json.loads(result)
        return Response(result)


class CountryRetrieveByNameView(APIView):

    def get_object(self, countryName):
        country = Country.objects.filter(countryName=countryName).first()
        if country is None:
            raise Http404
        return country

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-detail-by-name'))
    def get(self, request, countryName):
        country = self.get_object(countryName)
        serializer = CountrySerializer(country)
        return Response(serializer.data)


class CityListView(ListAPIView):

    serializer_class = CitySerializer
    filter_class = CityFilter

    def get_queryset(self):
        return City.objects.all().order_by('province', 'cityName')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='city-list'))
    def dispatch(self, *args, **kwargs):
        return super(CityListView, self).dispatch(*args, **kwargs)


class CityRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return City.objects.get(pk=pk)
        except City.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='city-detail'))
    def get(self, request, pk):
        city = self.get_object(pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)


class CityRetrieveByNameView(APIView):

    def get_object(self, cityName):
        city = City.objects.filter(cityName=cityName).first()
        if city is None:
            raise Http404
        return city

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='city-detail-by-name'))
    def get(self, request, cityName):
        city = self.get_object(cityName)
        serializer = CitySerializer(city)
        return Response(serializer.data)