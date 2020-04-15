from .models import City, Province, Country
from rest_framework import serializers

class ProvinceSerializer(serializers.HyperlinkedModelSerializer):

    provinceName = serializers.CharField(read_only=True)

    class Meta:
        model = Province
        fields = [
            'locationId', 'provinceName', 'provinceShortName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount'
        ]


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = [
            'locationId', 'provinceName', 'cityName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount'
        ]

class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country
        fields = [
            'locationId', 'continents', 'countryShortCode',
            'countryType', 'countryName', 'countryFullName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount'
        ]