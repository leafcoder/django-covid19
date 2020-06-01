import django_filters
from django.db.models import Q
from . import models


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class CityFilter(django_filters.rest_framework.FilterSet):

    provinceShortNames = CharInFilter(
        field_name='province__provinceShortName', lookup_expr='in')
    provinceNames = CharInFilter(
        field_name='province__provinceName', lookup_expr='in')
    cityNames = CharInFilter(
        field_name='cityName', lookup_expr='in')
 
    provinceShortName = django_filters.CharFilter(
        field_name='province__provinceShortName', lookup_expr='exact')
    provinceName = django_filters.CharFilter(
        field_name='province__provinceName', lookup_expr='exact')
    cityName = django_filters.CharFilter(
        field_name='cityName', lookup_expr='exact')

    class Meta:
        model = models.City
        fields = ['provinceShortName', 'provinceName', 'cityName']


class ProvinceFilter(django_filters.rest_framework.FilterSet):

    provinceShortNames = CharInFilter(
        field_name='provinceShortName', lookup_expr='in')
    provinceNames = CharInFilter(
        field_name='provinceName', lookup_expr='in')

    provinceShortName = django_filters.CharFilter(
        field_name='provinceShortName', lookup_expr='exact')
    provinceName = django_filters.CharFilter(
        field_name='provinceName', lookup_expr='exact')

    class Meta:
        model = models.Province
        fields = ['provinceName', 'provinceShortName']


class CountryFilter(django_filters.rest_framework.FilterSet):

    continents = CharInFilter(
        field_name='continents', lookup_expr='in')
    countryShortCodes = CharInFilter(
        field_name='countryShortCode', lookup_expr='in')
    countryNames = CharInFilter(
        field_name='countryName', lookup_expr='in')

    class Meta:
        model = models.Country
        fields = [
            'continents', 'countryShortCode', 'countryName'
        ]


class StateFilter(django_filters.rest_framework.FilterSet):

    states = CharInFilter(field_name='state', lookup_expr='in')
    stateNames = CharInFilter(
        field_name='stateName', lookup_expr='in')

    class Meta:
        model = models.State
        fields = ['state', 'stateName']
