from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from . import models
import json
# Register your models here.


class BaseAdmin(admin.ModelAdmin):

    list_per_page = 50

    list_max_show_all = 200

    show_full_result_count = False

    preserve_filters = True


@admin.register(models.Statistics)
class StatisticsAdmin(BaseAdmin):

    list_display = (
        'id', 'jsonGlobalStatistics', 'jsonDomesticStatistics',
        'jsonInternationalStatistics', 'modifyTime', 'crawlTime'
    )
    search_fields = ('crawlTime', 'modifyTime')

    def jsonGlobalStatistics(self, obj):
        return self.to_json(obj.globalStatistics)
    jsonGlobalStatistics.short_description = '全球疫情'
    jsonGlobalStatistics.admin_order_field = 'globalStatistics'

    def jsonDomesticStatistics(self, obj):
        return self.to_json(obj.domesticStatistics)
    jsonDomesticStatistics.short_description = '国内疫情'
    jsonDomesticStatistics.admin_order_field = 'domesticStatistics'

    def jsonInternationalStatistics(self, obj):
        return self.to_json(obj.internationalStatistics)
    jsonInternationalStatistics.short_description = '国际疫情'
    jsonInternationalStatistics.admin_order_field = 'internationalStatistics'

    def to_json(self, data):
        try:
            data = json.loads(data)
        except:
            return
        result = []
        for k, v in sorted(data.items()):
            result.append(format_html('{}: {}', k, v))
        return mark_safe(format_html(
            '<pre>{}</pre>', format_html('<br>'.join(result))))

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