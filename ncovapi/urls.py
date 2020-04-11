from django.urls import include, path
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'provinces', views.ProvinceViewSet)
# router.register(r'cities', views.CityViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


app_name = 'ncovapi'

urlpatterns = [
    path(r'cities/', views.CityListView.as_view(), name='city-list'),
    path(r'cities/<str:cityName>/', views.CityRetrieveView.as_view(), name='city-detail'),
    path(r'provinces/', views.ProvinceListView.as_view(), name='province-list'),
    path(r'provinces/<str:provinceName>/', views.ProvinceRetrieveView.as_view(), name='province-detail'),
    path(r'countries/', views.CountryListView.as_view(), name='country-list'),
    path(r'countries/<str:countryName>/', views.CountryRetrieveView.as_view(), name='country-detail'),
    # path('', include(router.urls))
]