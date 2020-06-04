from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = 'django_covid19'

urlpatterns = [
    url(r'statistics/$', views.StatisticsListView.as_view(), name='statistics-list'),
    url(r'statistics/latest/$', views.LatestStatisticsView.as_view(), name='statistics-latest'),
    url(r'cities/(?P<countryCode>[A-Z]+)/$', views.CityListView.as_view(), name='city-list'),
    url(r'cities/(?P<countryCode>[A-Z]+)/(?P<cityName>[^/]+)/$', views.CityRetrieveByNameView.as_view(), name='city-detail'),

    url(r'countries/$', views.CountryListView.as_view(), name='country-list'),
    url(r'countries/daily/$', views.CountryListDailyView.as_view(), name='country-list-daily'),
    url(r'countries/(?P<countryCode>[A-Z]+)/$', views.CountryRetrieveView.as_view(), name='country-detail'),
    url(r'countries/(?P<countryCode>[A-Z]+)/daily/$', views.CountryDailyView.as_view(), name='country-daily'),

    url(r'provinces/(?P<countryCode>[A-Z]+)/$', views.ProvinceListView.as_view(), name='province-list'),
    url(r'provinces/(?P<countryCode>[A-Z]+)/daily/$', views.ProvinceListDailyView.as_view(), name='province-list-daily'),
    url(r'provinces/(?P<countryCode>[A-Z]+)/(?P<provinceCode>[A-Z\-\d]+)/daily/$', views.ProvinceDailyView.as_view(), name='province-daily'),
    url(r'provinces/(?P<countryCode>[A-Z]+)/(?P<provinceName>[^/]+)/daily/$', views.ProvinceDailyByNameView.as_view(), name='province-daily-by-name'),
    url(r'provinces/(?P<countryCode>[A-Z]+)/(?P<provinceCode>[A-Z\-\d]+)/$', views.ProvinceRetrieveView.as_view(), name='province-detail'),
    url(r'provinces/(?P<countryCode>[A-Z]+)/(?P<provinceName>[^/]+)/$', views.ProvinceRetrieveByNameView.as_view(), name='province-detail-by-name'),
]