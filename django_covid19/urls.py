from django.urls import include, path
from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = 'ncov'

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
]