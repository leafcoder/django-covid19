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

    continents = models.CharField(max_length=50)
    countryCode = models.CharField(max_length=20)
    countryName = models.CharField(max_length=50)
    countryFullName = models.CharField(max_length=50)
    currentConfirmedCount = models.IntegerField(default=0)
    confirmedCount = models.IntegerField(default=0)
    suspectedCount = models.IntegerField(default=0)
    curedCount = models.IntegerField(default=0)
    deadCount = models.IntegerField(default=0)

    showRank = models.BooleanField(default=False)
    deadRateRank = models.IntegerField(null=True)
    deadCountRank = models.IntegerField(null=True)
    confirmedCountRank = models.FloatField(null=True)
    deadRate = models.FloatField(null=True)
    tags = models.CharField(max_length=200, null=True)
    statisticsData = models.CharField(max_length=500, null=True)
    comment = models.CharField(max_length=200, null=True)
    incrVo = models.TextField(null=True)
    sort = models.IntegerField(null=True)
    operator = models.CharField(max_length=50, null=True)
    dailyData = models.TextField()
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