from django.http import Http404
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from .serializers import CitySerializer, ProvinceSerializer, CountrySerializer
from .models import Crawler, City, Province, Country
from .filters import CityFilter, ProvinceFilter, CountryFilter


class ProvinceListView(ListAPIView):

    """省列表"""

    serializer_class = ProvinceSerializer
    filter_class = ProvinceFilter

    def get_queryset(self):
        crawler = Crawler.objects.order_by('-id').first()
        queryset = Province.objects.filter(crawler=crawler)
        return queryset


class ProvinceRetrieveByNameView(APIView):
    """通过省名获取数据"""

    def get_object(self, provinceName):
        try:
            crawler = Crawler.objects.order_by('-id').first()
        except Crawler.DoesNotExist:
            raise Http404
        try:
            return Province.objects.filter(
                crawler=crawler, provinceName=provinceName).first()
        except Province.DoesNotExist:
            raise Http404

    def get(self, request, provinceName):
        province = self.get_object(provinceName)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)


class ProvinceRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return Province.objects.get(pk=pk)
        except Province.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        province = self.get_object(pk)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)


class CountryListView(ListAPIView):

    serializer_class = CountrySerializer
    filter_class = CountryFilter

    def get_queryset(self):
        crawler = Crawler.objects.order_by('-id').first()
        queryset = Country.objects.filter(crawler=crawler)
        return queryset.all()


class CountryRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        country = self.get_object(pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)


class CountryRetrieveByNameView(APIView):

    def get_object(self, countryName):
        try:
            crawler = Crawler.objects.order_by('-id').first()
        except Crawler.DoesNotExist:
            raise Http404
        try:
            return Country.objects.filter(
                crawler=crawler, countryName=countryName).first()
        except Country.DoesNotExist:
            raise Http404

    def get(self, request, countryName):
        country = self.get_object(countryName)
        serializer = CountrySerializer(country)
        return Response(serializer.data)


class CityListView(ListAPIView):

    serializer_class = CitySerializer
    filter_class = CityFilter

    def get_queryset(self):
        crawler = Crawler.objects.order_by('-id').first()
        queryset = City.objects.filter(crawler=crawler)
        return queryset


class CityRetrieveView(APIView):

    def get_object(self, pk):
        try:
            return City.objects.get(pk=pk)
        except City.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        city = self.get_object(pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)


class CityRetrieveByNameView(APIView):

    def get_object(self, cityName):
        try:
            crawler = Crawler.objects.order_by('-id').first()
        except Crawler.DoesNotExist:
            raise Http404
        try:
            return City.objects.filter(
                crawler=crawler, cityName=cityName).first()
        except City.DoesNotExist:
            raise Http404

    def get(self, request, cityName):
        city = self.get_object(cityName)
        serializer = CitySerializer(city)
        return Response(serializer.data)