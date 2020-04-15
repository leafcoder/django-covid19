import django_filters
from django.db.models import Q
from .models import City, Province, Country


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class CityFilter(django_filters.rest_framework.FilterSet):

    locationId = django_filters.CharFilter(lookup_expr='iexact')
    provinceName = django_filters.CharFilter(
        field_name='province__provinceName', lookup_expr='iexact')
    cityName = django_filters.CharFilter(lookup_expr='iexact')
    cityNames = CharInFilter(
        field_name='cityName', lookup_expr='in')

    class Meta:
        model = City
        fields = ['locationId', 'provinceName', 'cityName']

class ProvinceFilter(django_filters.rest_framework.FilterSet):

    locationId = django_filters.CharFilter(lookup_expr='iexact')
    provinceName = django_filters.CharFilter(lookup_expr='iexact')
    provinceShortName = django_filters.CharFilter(lookup_expr='iexact')
    provinceNames = CharInFilter(
        field_name='provinceyName', lookup_expr='in')

    class Meta:
        model = Province
        fields = ['id', 'locationId', 'provinceName', 'provinceShortName']

class CountryFilter(django_filters.rest_framework.FilterSet):

    locationId = django_filters.CharFilter(lookup_expr='iexact')
    continents = django_filters.CharFilter(lookup_expr='iexact')
    countryShortCode = django_filters.CharFilter(lookup_expr='iexact')
    countryType = django_filters.CharFilter(lookup_expr='iexact')
    countryName = django_filters.CharFilter(lookup_expr='iexact')
    countryFullName = django_filters.CharFilter(lookup_expr='iexact')
    countryNames = CharInFilter(
        field_name='countryName', lookup_expr='in')

    class Meta:
        model = Country
        fields = [
            'locationId', 'continents', 'countryShortCode', 'countryType',
            'countryName', 'countryFullName'
        ]