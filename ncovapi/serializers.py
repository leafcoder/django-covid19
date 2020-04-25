from .models import City, Province, Country
from rest_framework import serializers


class StatisticsGroupSerializer(serializers.Serializer):

    currentConfirmedCount = serializers.IntegerField()
    confirmedCount = serializers.IntegerField()
    suspectedCount = serializers.IntegerField()
    seriousCount = serializers.IntegerField()
    curedCount = serializers.IntegerField()
    deadCount = serializers.IntegerField()

class StatisticsSerializer(serializers.Serializer):

    globalStatistics = StatisticsGroupSerializer()
    domesticStatistics = StatisticsGroupSerializer()
    internationalStatistics = StatisticsGroupSerializer()
    remarks = serializers.ListField(
       child=serializers.CharField(max_length=100), max_length=10
    )
    notes = serializers.ListField(
       child=serializers.CharField(max_length=100), max_length=10
    )
    generalRemark = serializers.CharField()
    modifyTime = serializers.IntegerField()
    createTime = serializers.IntegerField()


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