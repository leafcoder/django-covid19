from django.http import Http404
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from .serializers import CitySerializer, ProvinceSerializer, CountrySerializer
from .models import City, Province, Country
from .filters import CityFilter, ProvinceFilter, CountryFilter

class ProvinceListView(ListAPIView):

    queryset = Province.objects.all().order_by('-locationId')
    serializer_class = ProvinceSerializer
    filter_class = ProvinceFilter

class ProvinceRetrieveView(APIView):

    def get_object(self, provinceName):
        try:
            return Province.objects.get(provinceName=provinceName)
        except Province.DoesNotExist:
            raise Http404

    @cache_response
    def get(self, request, provinceName):
        province = self.get_object(provinceName)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)

class CountryListView(ListAPIView):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_class = CountryFilter

class CountryRetrieveView(APIView):

    def get_object(self, countryName):
        try:
            return Country.objects.get(countryName=countryName)
        except Country.DoesNotExist:
            raise Http404

    @cache_response
    def get(self, request, countryName):
        country = self.get_object(countryName)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

class CityListView(ListAPIView):

    queryset = City.objects.all()
    serializer_class = CitySerializer
    # filter_class = CityFilter

class CityRetrieveView(APIView):

    def get_object(self, cityName):
        try:
            return City.objects.get(cityName=cityName)
        except City.DoesNotExist:
            raise Http404

    @cache_response
    def get(self, request, cityName):
        city = self.get_object(cityName)
        serializer = CitySerializer(city)
        return Response(serializer.data)