from django.db import models
from django.utils import timezone

class Crawler(models.Model):

    createTime = models.DateTimeField(
        "抓取时间", default=timezone.now, editable=False)

    class Meta:
        verbose_name = "抓取版本"
        verbose_name_plural = "抓取版本"

class Province(models.Model):

    locationId = models.IntegerField()
    provinceName = models.CharField(max_length=50)
    provinceShortName = models.CharField(max_length=20)
    currentConfirmedCount = models.IntegerField()
    confirmedCount = models.IntegerField()
    suspectedCount = models.IntegerField()
    curedCount = models.IntegerField()
    deadCount = models.IntegerField()
    comment = models.CharField(max_length=200)
    statisticsData = models.CharField(max_length=500)
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="provinces",
        db_column="crawlerId"
    )

    class Meta:
        verbose_name = '省份'
        verbose_name_plural = '省份'

class City(models.Model):

    locationId = models.IntegerField()
    cityName = models.CharField(max_length=50)
    currentConfirmedCount = models.IntegerField()
    confirmedCount = models.IntegerField()
    suspectedCount = models.IntegerField()
    curedCount = models.IntegerField()
    deadCount = models.IntegerField()
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
        verbose_name = "城市"
        verbose_name_plural = "城市"

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
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="countries",
        db_column="countryId"
    )

    class Meta:
        verbose_name = "国家或地区"
        verbose_name_plural = "国家或地区"
