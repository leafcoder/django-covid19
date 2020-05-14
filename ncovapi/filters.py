import django_filters
from django.db.models import Q
from .models import City, Province, Country


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class CityFilter(django_filters.rest_framework.FilterSet):

    provinceShortNames = CharInFilter(
        field_name='province__provinceShortName', lookup_expr='in')
    cityNames = CharInFilter(
        field_name='cityName', lookup_expr='in')

    class Meta:
        model = City
        fields = ['provinceShortNames', 'cityName']


class ProvinceFilter(django_filters.rest_framework.FilterSet):

    provinceShortNames = CharInFilter(
        field_name='provinceShortName', lookup_expr='in')
    provinceNames = CharInFilter(
        field_name='provinceName', lookup_expr='in')

    class Meta:
        model = Province
        fields = ['provinceName', 'provinceShortName']


class CountryFilter(django_filters.rest_framework.FilterSet):

    continents = CharInFilter(
        field_name='continents', lookup_expr='in')
    countryShortCodes = CharInFilter(
        field_name='countryShortCode', lookup_expr='in')
    countryNames = CharInFilter(
        field_name='countryName', lookup_expr='in')

    class Meta:
        model = Country
        fields = [
            'continents', 'countryShortCode', 'countryName'
        ]
