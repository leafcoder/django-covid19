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


class Province(models.Model):

    locationId = models.IntegerField(_('locationId'))
    provinceName = models.CharField(_('provinceName'), max_length=50)
    provinceShortName = models.CharField(_('provinceShortName'), max_length=20)
    currentConfirmedCount = models.IntegerField(_('currentConfirmedCount'), default=0)
    confirmedCount = models.IntegerField(_('confirmedCount'), default=0)
    suspectedCount = models.IntegerField(_('suspectedCount'), default=0)
    curedCount = models.IntegerField(_('curedCount'), default=0)
    deadCount = models.IntegerField(_('deadCount'), default=0)
    comment = models.CharField(_('comment'), max_length=200)
    statisticsData = models.CharField(_('statisticsData'), max_length=500)
    dailyData = models.TextField(_('dailyData'))
    createTime = models.DateTimeField(_('createTime'), auto_now_add=True, editable=False)
    modifyTime = models.DateTimeField(_('modifyTime'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Province')


class City(models.Model):

    locationId = models.IntegerField(_('locationId'))
    cityName = models.CharField(_('cityName'), max_length=50)
    currentConfirmedCount = models.IntegerField(_('currentConfirmedCount'), default=0)
    confirmedCount = models.IntegerField(_('confirmedCount'), default=0)
    suspectedCount = models.IntegerField(_('suspectedCount'), default=0)
    curedCount = models.IntegerField(_('curedCount'), default=0)
    deadCount = models.IntegerField(_('deadCount'), default=0)
    createTime = models.DateTimeField(_('createTime'), auto_now_add=True, editable=False)
    modifyTime = models.DateTimeField(_('modifyTime'), auto_now=True, editable=False)
    province = models.ForeignKey(
        "Province", verbose_name=_('province'), on_delete=models.CASCADE,
        related_name="cities", db_column="provinceId"
    )

    @property
    def provinceName(self):
        return self.province.provinceName

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('City')


class Country(models.Model):

    locationId = models.IntegerField()
    continents = models.CharField(max_length=50)
    countryShortCode = models.CharField(max_length=20)
    countryName = models.CharField(max_length=50)
    countryFullName = models.CharField(max_length=50)
    currentConfirmedCount = models.IntegerField(default=0)
    confirmedCount = models.IntegerField(default=0)
    suspectedCount = models.IntegerField(default=0)
    curedCount = models.IntegerField(default=0)
    deadCount = models.IntegerField(default=0)

    showRank = models.BooleanField(null=True)
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


class State(models.Model):

    countryShortCode = models.CharField(max_length=20)
    stateName = models.CharField(max_length=50, null=False)
    currentUrl = models.URLField(max_length=200, null=True, blank=True)
    dailyUrl = models.URLField(max_length=200, null=True, blank=True)
    dailyData = models.TextField(default='[]')  # save daily data here

    # fields in covidtracking api
    state = models.CharField(max_length=10, null=False)
    positive = models.IntegerField(null=True, blank=True)
    negative = models.IntegerField(null=True, blank=True)
    positiveScore = models.IntegerField(null=True, blank=True)
    negativeScore = models.IntegerField(null=True, blank=True)
    negativeRegularScore = models.IntegerField(null=True, blank=True)
    commercialScore = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    dataQualityGrade = models.CharField(max_length=20, null=True, blank=True)
    pending = models.IntegerField(null=True, blank=True)
    hospitalizedCurrently = models.IntegerField(null=True, blank=True)
    hospitalizedCumulative = models.IntegerField(null=True, blank=True)
    inIcuCurrently = models.IntegerField(null=True, blank=True)
    inIcuCumulative = models.IntegerField(null=True, blank=True)
    onVentilatorCurrently = models.IntegerField(null=True, blank=True)
    onVentilatorCumulative = models.IntegerField(null=True, blank=True)
    recovered = models.IntegerField(null=True, blank=True)
    lastUpdateEt = models.CharField(max_length=20, null=True, blank=True)
    checkTimeEt = models.CharField(max_length=20, null=True, blank=True)
    death = models.IntegerField(null=True, blank=True)
    hospitalized = models.IntegerField(null=True, blank=True)
    totalTestResults = models.IntegerField(null=True, blank=True)
    posNeg = models.IntegerField(null=True, blank=True)
    fips = models.CharField(max_length=20, null=True, blank=True)
    dateModified = models.CharField(max_length=50, null=True, blank=True)
    dateChecked = models.CharField(max_length=50, null=True, blank=True)
    hash = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('State')