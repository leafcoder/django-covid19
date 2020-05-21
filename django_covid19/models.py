from django.db import models
from django.utils import timezone
from django_mysql.models import JSONField


class Statistics(models.Model):


    JSON_FIELDS = (
        'globalStatistics', 'domesticStatistics', 'internationalStatistics',
        'remarks', 'notes', 'WHOArticle', 'recommends', 'timelines',
        'wikis', 'goodsGuides', 'rumors'
    )

    globalStatistics = models.TextField(default='{}')
    domesticStatistics = models.TextField(default='{}')
    internationalStatistics = models.TextField(default='{}')
    remarks = models.TextField(default='[]')
    notes = models.TextField(default='[]')
    generalRemark = models.TextField(default='')
    WHOArticle = models.TextField(verbose_name='WHO 文章', default='{}')
    recommends = models.TextField(verbose_name='防护知识', default='[]')
    timelines = models.TextField(verbose_name='时间线事件', default='[]')
    wikis = models.TextField(verbose_name='Wiki', default='[]')
    goodsGuides = models.TextField(verbose_name='购物指南', default='[]')
    rumors = models.TextField(verbose_name='辟谣与防护', default='[]')
    modifyTime = models.DateTimeField(null=True)
    createTime = models.DateTimeField(null=True)
    crawlTime = models.DateTimeField(
        "抓取时间", default=timezone.now, editable=False)

    class Meta:
        verbose_name = '统计数据'
        verbose_name_plural = '统计数据'


class Province(models.Model):

    locationId = models.IntegerField()
    provinceName = models.CharField(max_length=50)
    provinceShortName = models.CharField(max_length=20)
    currentConfirmedCount = models.IntegerField(default=0)
    confirmedCount = models.IntegerField(default=0)
    suspectedCount = models.IntegerField(default=0)
    curedCount = models.IntegerField(default=0)
    deadCount = models.IntegerField(default=0)
    comment = models.CharField(max_length=200)
    statisticsData = models.CharField(max_length=500)
    dailyData = models.TextField()
    created = models.DateTimeField(
        '创建时间', auto_now_add=True, editable=False)
    updated = models.DateTimeField(
        '更新时间', auto_now=True, editable=False)

    class Meta:
        verbose_name = '国内省份'
        verbose_name_plural = '国内省份'


class City(models.Model):

    locationId = models.IntegerField()
    cityName = models.CharField(max_length=50)
    currentConfirmedCount = models.IntegerField(default=0)
    confirmedCount = models.IntegerField(default=0)
    suspectedCount = models.IntegerField(default=0)
    curedCount = models.IntegerField(default=0)
    deadCount = models.IntegerField(default=0)
    created = models.DateTimeField(
        '创建时间', auto_now_add=True, editable=False)
    updated = models.DateTimeField(
        '更新时间', auto_now=True, editable=False)
    province = models.ForeignKey(
        "Province", on_delete=models.CASCADE, related_name="cities",
        db_column="provinceId"
    )

    @property
    def provinceName(self):
        return self.province.provinceName

    class Meta:
        verbose_name = "国内城市"
        verbose_name_plural = "国内城市"


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
    created = models.DateTimeField(
        '创建时间', auto_now_add=True, editable=False)
    updated = models.DateTimeField(
        '更新时间', auto_now=True, editable=False)

    class Meta:
        verbose_name = "国家地区"
        verbose_name_plural = "国家地区"
