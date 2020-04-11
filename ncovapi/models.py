from django.db import models
from django.utils import timezone

class Province(models.Model):

    locationId = models.IntegerField(primary_key=True)
    provinceName = models.CharField(max_length=50)
    provinceShortName = models.CharField(max_length=20)
    currentConfirmedCount = models.IntegerField()
    confirmedCount = models.IntegerField()
    suspectedCount = models.IntegerField()
    curedCount = models.IntegerField()
    deadCount = models.IntegerField()
    comment = models.CharField(max_length=200)
    statisticsData = models.CharField(max_length=500)
    crawl_time = models.DateTimeField(
        '抓取时间', default=timezone.now, editable=False)

    class Meta:
        verbose_name = '省份'
        verbose_name_plural = '省份'

class City(models.Model):

    locationId = models.IntegerField()
    province = models.ForeignKey(
        'Province', on_delete=models.CASCADE, related_name="cities",
        db_column='provinceId'
    )
    cityName = models.CharField(max_length=50)
    currentConfirmedCount = models.IntegerField()
    confirmedCount = models.IntegerField()
    suspectedCount = models.IntegerField()
    curedCount = models.IntegerField()
    deadCount = models.IntegerField()
    crawl_time = models.DateTimeField(
        '抓取时间', default=timezone.now, editable=False)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = '城市'
        unique_together = ('province', 'cityName')

class Country(models.Model):

    locationId = models.IntegerField()
    continents = models.CharField(max_length=50) # 
    countryShortCode = models.CharField(max_length=20) #
    countryType = models.CharField(max_length=20) # 
    countryName = models.CharField(max_length=50) #
    countryFullName = models.CharField(max_length=50) #
    currentConfirmedCount = models.IntegerField()
    confirmedCount = models.IntegerField()
    suspectedCount = models.IntegerField()
    curedCount = models.IntegerField()
    deadCount = models.IntegerField()

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
    modifyTime = models.IntegerField(null=True)
    createTime = models.IntegerField(null=True)
    crawl_time = models.DateTimeField(
        '抓取时间', default=timezone.now, editable=False)


    class Meta:
        verbose_name = '国家或地区'
        verbose_name_plural = '国家或地区'
        unique_together = ('continents', 'countryShortCode')
