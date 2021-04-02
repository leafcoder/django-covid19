from django.db import models
from django.utils import timezone
from django_mysql.models import JSONField
from django.utils.translation import ugettext_lazy as _


class Statistics(models.Model):

    JSON_FIELDS = (
        'globalStatistics', 'domesticStatistics', 'internationalStatistics',
        'remarks', 'notes', 'WHOArticle', 'recommends', 'timelines',
        'wikis', 'goodsGuides', 'rumors'
    )

    globalStatistics = models.TextField(_('globalStatistics'), default='{}')
    domesticStatistics = models.TextField(_('domesticStatistics'), default='{}')
    internationalStatistics = models.TextField(_('internationalStatistics'), default='{}')
    remarks = models.TextField(_('remarks'), default='[]')
    notes = models.TextField(_('notes'), default='[]')
    generalRemark = models.TextField(_('generalRemark'), default='')
    WHOArticle = models.TextField(_('WHOArticle'), default='{}')
    recommends = models.TextField(_('recommends'), default='[]')
    timelines = models.TextField(_('timelines'), default='[]')
    wikis = models.TextField(_('Wiki'), default='[]')
    goodsGuides = models.TextField(_('goodsGuides'), default='[]')
    rumors = models.TextField(_('rumors'), default='[]')
    modifyTime = models.DateTimeField(_('modifyTime'), null=True)
    createTime = models.DateTimeField(_('createTime'), null=True)
    crawlTime = models.DateTimeField(_('crawlTime'), default=timezone.now, editable=False)

    class Meta:
        verbose_name = _('Statistics')
        verbose_name_plural = _('Statistics')


class Country(models.Model):

    continents = models.CharField(_('continents'), max_length=50)
    countryCode = models.CharField(_('countryCode'), max_length=20)
    countryName = models.CharField(_('countryName'), max_length=50)
    countryFullName = models.CharField(_('countryFullName'), max_length=50)
    currentConfirmedCount = models.IntegerField(_('currentConfirmedCount'), default=0)
    confirmedCount = models.IntegerField(_('confirmedCount'), default=0)
    suspectedCount = models.IntegerField(_('suspectedCount'), default=0)
    curedCount = models.IntegerField(_('curedCount'), default=0)
    deadCount = models.IntegerField(_('deadCount'), default=0)

    showRank = models.BooleanField(_('showRank'), default=False)
    deadRateRank = models.IntegerField(_('deadRateRank'), null=True)
    deadCountRank = models.IntegerField(_('deadCountRank'), null=True)
    confirmedCountRank = models.FloatField(_('confirmedCountRank'), null=True)
    deadRate = models.FloatField(_('deadRate'), null=True)
    tags = models.CharField(_('tags'), max_length=200, null=True)
    statisticsData = models.CharField(_('statisticsData'), max_length=500, null=True)
    comment = models.CharField(_('comment'), max_length=200, null=True)
    incrVo = models.TextField(_('incrVo'), null=True)
    sort = models.IntegerField(_('sort'), null=True)
    operator = models.CharField(_('operator'), max_length=50, null=True)
    dailyData = models.TextField(_('dailyData'))
    createTime = models.DateTimeField(_('createTime'), auto_now_add=True, editable=False)
    modifyTime = models.DateTimeField(_('modifyTime'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Country')


class Province(models.Model):

    countryCode = models.CharField(_('countryCode'), max_length=20)
    provinceName = models.CharField(_('provinceName'), max_length=50)
    provinceCode = models.CharField(_('provinceCode'), max_length=20)
    currentConfirmedCount = models.IntegerField(_('currentConfirmedCount'), default=0)
    confirmedCount = models.IntegerField(_('confirmedCount'), default=0)
    suspectedCount = models.IntegerField(_('suspectedCount'), default=0)
    curedCount = models.IntegerField(_('curedCount'), default=0)
    deadCount = models.IntegerField(_('deadCount'), default=0)
    dailyUrl = models.URLField(_('dailyUrl'), null=True, blank=True)
    currentUrl = models.URLField(_('currentUrl'), null=True, blank=True)
    dailyData = models.TextField(_('dailyData'), default='[]')
    createTime = models.DateTimeField(_('createTime'), auto_now_add=True, editable=False)
    modifyTime = models.DateTimeField(_('modifyTime'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Province')


class City(models.Model):

    countryCode = models.CharField(_('countryCode'), max_length=20)
    provinceCode = models.CharField(_('provinceCode'), max_length=20)
    provinceName = models.CharField(_('provinceName'), max_length=50)
    cityName = models.CharField(_('cityName'), max_length=50)
    currentConfirmedCount = models.IntegerField(_('currentConfirmedCount'), default=0)
    confirmedCount = models.IntegerField(_('confirmedCount'), default=0)
    suspectedCount = models.IntegerField(_('suspectedCount'), default=0)
    curedCount = models.IntegerField(_('curedCount'), default=0)
    deadCount = models.IntegerField(_('deadCount'), default=0)
    createTime = models.DateTimeField(_('createTime'), auto_now_add=True, editable=False)
    modifyTime = models.DateTimeField(_('modifyTime'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('City')


class CountryCode(models.Model):

    numericCode = models.IntegerField(_('numericCode'))
    countryCode = models.CharField(_('countryCode'), max_length=20)
    shortCountryCode = models.CharField(_('shortCountryCode'), max_length=5)
    countryName = models.CharField(_('countryName'), max_length=50)
    englishCountryName = models.CharField(_('englishCountryName'), max_length=50)
    englishCountryFullName = models.CharField(_('englishCountryFullName'), max_length=100)
    comment = models.CharField(_('comment'), max_length=200, null=True)

    class Meta:
        verbose_name = _('CountryCode')
        verbose_name_plural = _('CountryCode')