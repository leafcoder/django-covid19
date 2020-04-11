from .models import City, Province, Country
from rest_framework import serializers

class ProvinceSerializer(serializers.HyperlinkedModelSerializer):

    # cities = CitySerializer(many=True)

    class Meta:
        model = Province
        fields = [
            'locationId', 'provinceName', 'provinceShortName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount'
            # 'comment', 'statisticsData'
        ]


class CitySerializer(serializers.HyperlinkedModelSerializer):

    province = ProvinceSerializer()

    class Meta:
        model = City
        fields = [
            'locationId', 'province', 'cityName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount',
            # 'comment', 'statisticsData'
        ]

class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country
        fields = [
            'locationId', 'continents', 'countryShortCode',
            'countryType', 'countryName', 'countryFullName',
            'currentConfirmedCount', 'confirmedCount', 'suspectedCount',
            'curedCount', 'deadCount',
            # 'showRank', 'deadRateRank',
            # 'deadCountRank', 'confirmedCountRank', 'deadRate', 'tags',
            # 'statisticsData', 'comment', 'incrVo', 'sort', 'operator',
            # 'modifyTime', 'createTime'
        ]