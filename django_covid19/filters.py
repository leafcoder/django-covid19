import django_filters
from django.db.models import Q
from . import models


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class CityFilter(django_filters.rest_framework.FilterSet):

    provinceNames = CharInFilter(
        field_name='provinceName', lookup_expr='in')
    provinceCodes = CharInFilter(
        field_name='provinceCode', lookup_expr='in')
    cityNames = CharInFilter(
        field_name='cityName', lookup_expr='in')
 
    class Meta:
        model = models.City
        fields = ['provinceName', 'provinceCode', 'cityName']


class ProvinceFilter(django_filters.rest_framework.FilterSet):

    provinceNames = CharInFilter(
        field_name='provinceName', lookup_expr='in')
    provinceCodes = CharInFilter(
        field_name='provinceCode', lookup_expr='in')

    class Meta:
        model = models.Province
        fields = ['provinceName', 'provinceCode']


class CountryFilter(django_filters.rest_framework.FilterSet):

    continents = CharInFilter(
        field_name='continents', lookup_expr='in')
    countryCodes = CharInFilter(
        field_name='countryCode', lookup_expr='in')
    countryNames = CharInFilter(
        field_name='countryName', lookup_expr='in')

    class Meta:
        model = models.Country
        fields = [
            'continents', 'countryCode', 'countryName'
        ]
