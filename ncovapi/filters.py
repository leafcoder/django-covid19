import django_filters
from django.db.models import Q
from .models import City, Province, Country


class CityFilter(django_filters.rest_framework.FilterSet):

    province = django_filters.NumberFilter(
        field_name='provinceId', lookup_expr='iexact')

    class Meta:
        model = City
        fields = ['locationId', 'province', 'cityName']

class ProvinceFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Province
        fields = ['locationId', 'provinceName', 'provinceShortName']

class CountryFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Country
        fields = [
            'locationId', 'continents', 'countryShortCode', 'countryType',
            'countryName', 'countryFullName'
        ]