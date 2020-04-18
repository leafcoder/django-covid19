from django.urls import include, path
from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = 'ncovapi'

urlpatterns = [
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('cities/', views.CityListView.as_view(), name='city-list'),
    path('cities/<int:pk>/', views.CityRetrieveView.as_view(), name='city-detail'),
    path('cities/<str:cityName>/', views.CityRetrieveByNameView.as_view(), name='city-detail-by-name'),
    path('provinces/', views.ProvinceListView.as_view(), name='province-list'),
    path('provinces/<int:pk>/', views.ProvinceRetrieveView.as_view(), name='province-detail'),
    path('provinces/<str:provinceName>/', views.ProvinceRetrieveByNameView.as_view(), name='province-detail-by-name'),
    path('countries/', views.CountryListView.as_view(), name='country-list'),
    path('countries/<int:pk>/', views.CountryRetrieveView.as_view(), name='country-detail'),
    path('countries/<str:countryName>/', views.CountryRetrieveByNameView.as_view(), name='country-detail-by-name'),
]