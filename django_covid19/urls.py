from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = 'django_covid19'

urlpatterns = [
    path('statistics/', views.StatisticsListView.as_view(), name='statistics-list'),
    path('statistics/latest', views.LatestStatisticsView.as_view(), name='statistics-latest'),
    path('cities/', views.CityListView.as_view(), name='city-list'),
    path('cities/<int:pk>/', views.CityRetrieveView.as_view(), name='city-detail'),
    path('cities/<str:cityName>/', views.CityRetrieveByNameView.as_view(), name='city-detail-by-name'),

    path('provinces/', views.ProvinceListView.as_view(), name='province-list'),
    path('provinces/<int:pk>/', views.ProvinceRetrieveView.as_view(), name='province-detail'),
    path('provinces/<str:provinceShortName>/', views.ProvinceRetrieveByNameView.as_view(), name='province-detail-by-name'),
    path('provinces/<str:provinceShortName>/daily/', views.ProvinceDailyListView.as_view(), name='province-daily-list'),

    path('countries/', views.CountryListView.as_view(), name='country-list'),
    path('countries/<int:pk>/', views.CountryRetrieveView.as_view(), name='country-detail'),
    path('countries/<str:countryName>/', views.CountryRetrieveByNameView.as_view(), name='country-detail-by-name'),
    path('countries/<str:countryName>/daily/', views.CountryDailyListView.as_view(), name='country-daily-list'),

    url(r'states/(?:(?P<raw>raw)/)?(?P<countryShortCode>[^/]+)/$', views.StateListView.as_view(), name='state-list'),
    url(r'states/(?:(?P<raw>raw)/)?(?P<countryShortCode>[^/]+)/daily/$', views.StateListDailyListView.as_view(), name='state-list-daily-list'),
    url(r'states/(?:(?P<raw>raw)/)?(?P<countryShortCode>[^/]+)/(?P<state>[A-Z]+)/$', views.StateRetrieveView.as_view(), name='state-detail'),
    url(r'states/(?:(?P<raw>raw)/)?(?P<countryShortCode>[^/]+)/(?P<state>[A-Z]+)/daily/$', views.StateDailyListView.as_view(), name='state-daily-list'),
    url(r'states/(?:(?P<raw>raw)/)?(?P<countryShortCode>[^/]+)/(?P<stateName>[^/]+)/$', views.StateRetrieveByNameView.as_view(), name='state-detail-by-name'),
    url(r'states/(?:(?P<raw>raw)/)?(?P<countryShortCode>[^/]+)/(?P<stateName>[^/]+)/daily/$', views.StateDailyListByNameView.as_view(), name='state-daily-list-by-name'),
]