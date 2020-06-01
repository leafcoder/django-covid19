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


class ProvinceListView(ListAPIView):

    """省列表"""

    serializer_class = serializers.ProvinceSerializer
    filter_class = filters.ProvinceFilter

    def get_queryset(self):
        return models.Province.objects.all().order_by('provinceName')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-list'))
    def dispatch(self, *args, **kwargs):
        return super(ProvinceListView, self).dispatch(*args, **kwargs)


class ProvinceDailyListView(APIView):

    """省按天返回列表"""

    def get_object(self, provinceShortName):
        province = models.Province.objects.filter(
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
        province = models.Province.objects.filter(
            provinceShortName=provinceShortName).first()
        if province is None:
            raise Http404
        return province

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-detail-by-name'))
    def get(self, request, provinceShortName):
        province = self.get_object(provinceShortName)
        serializer = serializers.ProvinceSerializer(province)
        return Response(serializer.data)


class ProvinceRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return models.Province.objects.get(pk=pk)
        except models.Province.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='province-detail'))
    def get(self, request, pk):
        province = self.get_object(pk)
        serializer = serializers.ProvinceSerializer(province)
        return Response(serializer.data)


class CountryListView(ListAPIView):

    serializer_class = serializers.CountrySerializer
    filter_class = filters.CountryFilter

    def get_queryset(self):
        return models.Country.objects.all().order_by(
            'continents', 'countryShortCode')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-list'))
    def dispatch(self, *args, **kwargs):
        return super(CountryListView, self).dispatch(*args, **kwargs)


class CountryRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return models.Country.objects.get(pk=pk)
        except models.Country.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-detail'))
    def get(self, request, pk):
        country = self.get_object(pk)
        serializer = serializers.CountrySerializer(country)
        return Response(serializer.data)


class CountryDailyListView(APIView):

    def get_object(self, countryName):
        country = models.Country.objects.filter(countryName=countryName).first()
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
        country = models.Country.objects.filter(
            countryName=countryName).first()
        if country is None:
            raise Http404
        return country

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='country-detail-by-name'))
    def get(self, request, countryName):
        country = self.get_object(countryName)
        serializer = serializers.CountrySerializer(country)
        return Response(serializer.data)


class CityListView(ListAPIView):

    serializer_class = serializers.CitySerializer
    filter_class = filters.CityFilter

    def get_queryset(self):
        return models.City.objects.all().order_by('province', 'cityName')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='city-list'))
    def dispatch(self, *args, **kwargs):
        return super(CityListView, self).dispatch(*args, **kwargs)


class CityRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return models.City.objects.get(pk=pk)
        except models.City.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='city-detail'))
    def get(self, request, pk):
        city = self.get_object(pk)
        serializer = serializers.CitySerializer(city)
        return Response(serializer.data)


class CityRetrieveByNameView(APIView):

    def get_object(self, cityName):
        city = models.City.objects.filter(cityName=cityName).first()
        if city is None:
            raise Http404
        return city

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='city-detail-by-name'))
    def get(self, request, cityName):
        city = self.get_object(cityName)
        serializer = serializers.CitySerializer(city)
        return Response(serializer.data)


class StateListView(ListAPIView):

    serializer_class = serializers.StateSerializer
    filter_class = filters.StateFilter

    def get_queryset(self):
        countryShortCode = self.kwargs['countryShortCode']
        return models.State.objects.filter(
            countryShortCode=countryShortCode).order_by('state')

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='state-list'))
    def dispatch(self, *args, **kwargs):
        if kwargs.get('raw') == 'raw':
            self.serializer_class = serializers.StateRawSerializer
        return super(StateListView, self).dispatch(*args, **kwargs)


class StateRetrieveByNameView(APIView):

    def get_object(self, countryShortCode, stateName):
        state = models.State.objects.filter(
            countryShortCode=countryShortCode,
            stateName__iexact=stateName
        ).first()
        if state is None:
            raise Http404
        return state

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='state-detail-by-name'))
    def get(self, request, countryShortCode, stateName, raw=None):
        inst = self.get_object(countryShortCode, stateName)
        if raw == 'raw':
            serializer = serializers.StateRawSerializer(inst)
        else:
            serializer = serializers.StateSerializer(inst)
        return Response(serializer.data)


class StateRetrieveView(APIView):

    def get_object(self, countryShortCode, state):
        state = models.State.objects.filter(
            countryShortCode=countryShortCode, state=state).first()
        if state is None:
            raise Http404
        return state

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='state-detail'))
    def get(self, request, countryShortCode, state, raw=None):
        inst = self.get_object(countryShortCode, state)
        if raw == 'raw':
            serializer = serializers.StateRawSerializer(inst)
        else:
            serializer = serializers.StateSerializer(inst)
        return Response(serializer.data)


class BaseDailyView(object):

    def format(self, countryShortCode, stateName, data):
        item = {}
        item['date'] = data['date']
        item['state'] = data['state']
        item['stateName'] = stateName
        item['countryShortCode'] = countryShortCode

        item['confirmedCount'] = data.get('positive')
        item['currentConfirmedCount'] = self.get_current_confirmed(data)
        item['suspectedCount'] = data.get('pending')
        item['curedCount'] = data.get('recovered')
        item['deadCount'] = data.get('death')

        item['currentConfirmedIncr'] = self.get_current_confirmed_incr(data)
        item['confirmedIncr'] = data.get('positiveIncrease')
        item['suspectedIncr'] = data.get('totalTestResultsIncrease')
        item['curedIncr'] = None  # 未提供
        item['deadIncr'] = data.get('deathIncrease')
        return item

    def get_current_confirmed(self, data):
        positive = data['positive'] if data.get('positive') else 0
        death = data['death'] if data.get('death') else 0
        recovered = data['recovered'] if data.get('recovered') else 0
        return positive - death - recovered

    def get_current_confirmed_incr(self, data):
        positive = data['positiveIncrease'] if data.get('positiveIncrease') else 0
        death = data['deathIncrease'] if data.get('deathIncrease') else 0
        return positive - death


class StateDailyListView(APIView, BaseDailyView):

    """州按天返回列表"""

    def get_object(self, countryShortCode, state):
        state = models.State.objects.filter(
            countryShortCode=countryShortCode, state=state).first()
        if state is None:
            raise Http404
        return state

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='state-daily-list'))
    def get(self, request, countryShortCode, state, raw=None):
        inst = self.get_object(countryShortCode, state)
        result = inst.dailyData
        result = json.loads(result)
        if raw == 'raw':
            return Response(result)
        stateName = inst.stateName
        data = []
        for r in result:
            data.append(self.format(countryShortCode, stateName, r))
        serializer = serializers.StateDailySerializer(data, many=True)
        return Response(serializer.data)

class StateDailyListByNameView(APIView, BaseDailyView):

    def get_object(self, countryShortCode, stateName):
        state = models.State.objects.filter(
            countryShortCode=countryShortCode, stateName=stateName).first()
        if state is None:
            raise Http404
        return state

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='state-daily-list-by-name'))
    def get(self, request, countryShortCode, stateName, raw=None):
        inst = self.get_object(countryShortCode, stateName)
        result = inst.dailyData
        result = json.loads(result)
        if raw == 'raw':
            return Response(result)
        stateName = inst.stateName
        data = []
        for r in result:
            data.append(self.format(countryShortCode, stateName, r))
        serializer = serializers.StateDailySerializer(data, many=True)
        return Response(serializer.data)


class StateListDailyListView(ListAPIView, BaseDailyView):

    serializer_class = serializers.StateDailyListSerializer
    filter_class = filters.StateFilter

    def get_queryset(self):
        countryShortCode = self.kwargs['countryShortCode']
        return models.State.objects.filter(
                countryShortCode=countryShortCode).order_by('state')

    def list(self, request, *args, **kwargs):
        countryShortCode = kwargs['countryShortCode']
        queryset = self.filter_queryset(self.get_queryset())

        if kwargs.get('raw') == 'raw':
            self.serializer_class = serializers.StateRawSerializer

        result = []
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for item in serializer.data:
                stateName = item['stateName']
                dailyData = json.loads(item['dailyData'])
                for daily in dailyData:
                    result.append(
                        self.format(countryShortCode, stateName, daily))
            return self.get_paginated_response(result)

        serializer = self.get_serializer(queryset, many=True)
        for item in serializer.data:
            stateName = item['stateName']
            dailyData = json.loads(item['dailyData'])
            for daily in dailyData:
                result.append(
                    self.format(countryShortCode, stateName, daily))
        return Response(result)

    @method_decorator(cache_page(
            CACHE_PAGE_TIMEOUT, key_prefix='state-list-daily-list'))
    def dispatch(self, *args, **kwargs):
        return super(StateListDailyListView, self).dispatch(*args, **kwargs)

