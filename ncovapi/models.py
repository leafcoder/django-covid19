from django.db import models
from django.utils import timezone


class Crawler(models.Model):

    modifyTime = models.DateTimeField(null=True)
    createTime = models.DateTimeField(null=True)
    crawlTime = models.DateTimeField(
        "抓取时间", default=timezone.now, editable=False)

    class Meta:
        verbose_name = "抓取版本"
        verbose_name_plural = "抓取版本"


class Statistics(models.Model):

    GLOBAL = 0
    DOMESTIC = 1
    INTERNATIONAL = 2

    countryType = models.IntegerField(choices=(
        (GLOBAL, '全球'),
        (DOMESTIC, '国内'),
        (INTERNATIONAL, '国外')
    ))
    currentConfirmedCount = models.IntegerField(default=0)
    confirmedCount = models.IntegerField(default=0)
    suspectedCount = models.IntegerField(default=0)
    seriousCount = models.IntegerField('现存无症状', default=0)
    curedCount = models.IntegerField(default=0)
    deadCount = models.IntegerField(default=0)
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="statistics",
        db_column="crawlerId"
    )

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
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="provinces",
        db_column="crawlerId"
    )

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
    province = models.ForeignKey(
        "Province", on_delete=models.CASCADE, related_name="cities",
        db_column="provinceId"
    )
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, db_column="crawlerId"
    )

    @property
    def provinceName(self):
        return self.province.provinceName

    class Meta:
        verbose_name = "国内城市"
        verbose_name_plural = "国内城市"


class Country(models.Model):

    locationId = models.IntegerField()
    continents = models.CharField(max_length=50) # 
    countryShortCode = models.CharField(max_length=20) #
    countryType = models.CharField(max_length=20) # 
    countryName = models.CharField(max_length=50) #
    countryFullName = models.CharField(max_length=50) #
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
    modifyTime = models.IntegerField(null=True)
    createTime = models.IntegerField(null=True)
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="countries",
        db_column="countryId"
    )

    class Meta:
        verbose_name = "国家地区"
        verbose_name_plural = "国家地区"
