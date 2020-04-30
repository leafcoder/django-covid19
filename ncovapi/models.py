from django.db import models
from django.utils import timezone
from django_mysql.models import ListCharField


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
    COUNTRY_TYPES = (
        (GLOBAL, '全球'),
        (DOMESTIC, '国内'),
        (INTERNATIONAL, '国外')
    )

    countryType = models.IntegerField(choices=COUNTRY_TYPES)
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


class Notice(models.Model):

    remarks = ListCharField(
        models.CharField(max_length=100), size=10, max_length=100*11)
    notes = ListCharField(
        models.CharField(max_length=100), size=10, max_length=100*11)
    generalRemark = models.TextField(null=True)
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="notices",
        db_column="crawlerId"
    )

    class Meta:
        verbose_name = '注意信息'
        verbose_name_plural = '注意信息'


class WHOArticle(models.Model):

    title = models.CharField(max_length=100)
    linkUrl = models.URLField(max_length=200)
    imgUrl = models.URLField(max_length=200)
    crawler = models.OneToOneField(
        "Crawler", on_delete=models.CASCADE, related_name="WHO_article",
        db_column="crawlerId"
    )

    class Meta:
        verbose_name = 'WHO 文章'
        verbose_name_plural = 'WHO 文章'


class Recommend(models.Model):

    CONTENT_TYPES = [
        (1, '我要出行'),
        (2, '家有小孩'),
        (3, '未知'),
        (4, '我宅在家'),
        (5, '未知'),
        (6, '未知'),
        (7, '未知')
    ]
    GLOBAL = 0
    DOMESTIC = 1
    INTERNATIONAL = 2
    COUNTRY_TYPES = (
        (GLOBAL, '全球'),
        (DOMESTIC, '国内'),
        (INTERNATIONAL, '国外')
    )

    title = models.CharField(max_length=100)
    linkUrl = models.URLField(max_length=200)
    imgUrl = models.URLField(max_length=200)
    contentType = models.IntegerField(choices=CONTENT_TYPES)
    recordStatus = models.IntegerField()
    countryType = models.IntegerField(choices=COUNTRY_TYPES)
    sort = models.IntegerField()
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="recommends",
        db_column="crawlerId"
    )

    class Meta:
        verbose_name = '防护知识'
        verbose_name_plural = '防护知识'


class Timeline(models.Model):

    pubDate = models.IntegerField()
    pubDateStr = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    summary = models.TextField()
    infoSource = models.CharField(max_length=50)
    sourceUrl = models.URLField(max_length=200)
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="timelines",
        db_column="crawlerId"
    )

    class Meta:
        verbose_name = '时间线事件'
        verbose_name_plural = '时间线事件'


class Wiki(models.Model):

    title = models.CharField(max_length=100)
    linkUrl = models.URLField(max_length=200)
    imgUrl = models.URLField(max_length=200)
    description = models.TextField()
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="wikis",
        db_column="crawlerId"
    )

    class Meta:
        verbose_name = 'Wiki'
        verbose_name_plural = 'Wiki'


class GoodsGuide(models.Model):

    title = models.CharField(max_length=100)
    categoryName = models.CharField(max_length=50)
    recordStatus = models.IntegerField()
    contentImgUrls = ListCharField(
        models.CharField(max_length=100), size=10, max_length=100*11)
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="goods_guides",
        db_column="crawlerId"
    )

    class Meta:
        verbose_name = '购物指南'
        verbose_name_plural = '购物指南'


class Rumor(models.Model):

    title = models.CharField(max_length=100)
    mainSummary = models.TextField()
    summary = models.TextField()
    body = models.TextField()
    sourceUrl = models.URLField(max_length=200)
    score = models.IntegerField()
    rumorType = models.IntegerField()
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="rumors",
        db_column="crawlerId"
    )

    class Meta:
        verbose_name = '辟谣与防护'
        verbose_name_plural = '辟谣与防护'


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
    created = models.DateTimeField(
        '创建时间', auto_now_add=True, editable=False)
    updated = models.DateTimeField(
        '更新时间', auto_now=True, editable=False)
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
    crawler = models.ForeignKey(
        "Crawler", on_delete=models.CASCADE, related_name="countries",
        db_column="countryId"
    )

    class Meta:
        verbose_name = "国家地区"
        verbose_name_plural = "国家地区"
