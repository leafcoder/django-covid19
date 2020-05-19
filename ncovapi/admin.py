from django.contrib import admin
from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html

from . import models
# Register your models here.


class BaseAdmin(admin.ModelAdmin):

    list_per_page = 50

    list_max_show_all = 200

    show_full_result_count = False

    preserve_filters = True


@admin.register(models.Statistics)
class StatisticsAdmin(BaseAdmin):

    pass


@admin.register(models.City)
class CityAdmin(BaseAdmin):

    list_display = (
        'province', 'cityName', 'currentConfirmedCount',
        'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount'
    )
    search_fields = ('cityName', 'province__provinceName')


@admin.register(models.Province)
class ProvinceAdmin(BaseAdmin):

    list_display = (
        'provinceName', 'currentConfirmedCount',
        'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount'
    )
    search_fields = ('provinceName', )


@admin.register(models.Country)
class CountryAdmin(BaseAdmin):

    list_display = (
        'continents', 'countryName', 'countryFullName',
        'currentConfirmedCount', 'confirmedCount',
        'suspectedCount', 'curedCount', 'deadCount'
    )
    search_fields = (
        'continents', 'countryFullName', 'countryShortCode', 'countryName'
    )