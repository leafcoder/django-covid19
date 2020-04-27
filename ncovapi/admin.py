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


@admin.register(models.Crawler)
class CrawlerAdmin(BaseAdmin):

    list_display = (
        'id', 'crawlTime', 'createTime', 'modifyTime'
    )


@admin.register(models.Statistics)
class StatisticsAdmin(BaseAdmin):

    list_display = (
        'id', 'countryType', 'seriousCount', 'currentConfirmedCount',
        'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount'
    )
    search_fields = ('crawler_id', )
    list_filter = ('countryType', )


@admin.register(models.Notice)
class NoticeAdmin(BaseAdmin):

    list_display = (
        'id', 'crawler', 'remarks', 'notes', 'generalRemark'
    )

@admin.register(models.WHOArticle)
class WHOArticleAdmin(BaseAdmin):

    list_display = ('id', 'title', 'linkUrl', 'imgUrl')

@admin.register(models.Recommend)
class RecommendAdmin(BaseAdmin):

    list_display = (
        'id', 'title', 'linkUrl', 'imgUrl', 'contentType',
        'countryType', 'recordStatus')

@admin.register(models.Timeline)
class TimelineAdmin(BaseAdmin):

    list_display = (
        'id', 'title', 'summary', 'pubDateStr', 'infoSource', 'sourceUrl')

@admin.register(models.Wiki)
class WikiAdmin(BaseAdmin):

    list_display = ('id', 'title', 'linkUrl', 'imgUrl', 'description')

@admin.register(models.GoodsGuide)
class GoodsGuideAdmin(BaseAdmin):

    list_display = (
        'categoryName', 'title', 'recordStatus', 'contentImgUrls')

@admin.register(models.Rumor)
class RumorAdmin(BaseAdmin):

    list_display = (
        'title', 'mainSummary', 'summary', 'body',
        'sourceUrl', 'score', 'rumorType')

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