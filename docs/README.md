<div align="center">

# 新冠肺炎实时接口 {docsify-ignore}

<p>
    <!-- Place this tag where you want the button to render. -->
    <a class="github-button" href="https://github.com/leafcoder/django-covid19/subscription" data-color-scheme="no-preference: light; light: light; dark: dark;" data-show-count="true" aria-label="Watch leafcoder/django-covid19 on GitHub">
        <img alt="GitHub forks" src="https://img.shields.io/github/watchers/leafcoder/django-covid19?style=social">
    </a>
    <a class="github-button" href="https://github.com/leafcoder/django-covid19" data-color-scheme="no-preference: light; light: light; dark: dark;" data-show-count="true" aria-label="Star leafcoder/django-covid19 on GitHub">
        <img alt="GitHub forks" src="https://img.shields.io/github/stars/leafcoder/django-covid19?style=social">
    </a>
    <a class="github-button" href="https://github.com/leafcoder/django-covid19/fork" data-color-scheme="no-preference: light; light: light; dark: dark;" data-show-count="true" aria-label="Fork leafcoder/django-covid19 on GitHub">
        <img alt="GitHub forks" src="https://img.shields.io/github/forks/leafcoder/django-covid19?style=social">
    </a>
</p>

<p>
    <img src="https://img.shields.io/github/v/release/leafcoder/django-covid19" data-origin="https://img.shields.io/github/v/release/leafcoder/django-covid19" alt="GitHub release (latest by date)">
    <img src="https://img.shields.io/github/languages/top/leafcoder/django-covid19" data-origin="https://img.shields.io/github/languages/top/leafcoder/django-covid19" alt="GitHub top language">
    <img src="https://img.shields.io/github/languages/code-size/leafcoder/django-covid19" data-origin="https://img.shields.io/github/languages/code-size/leafcoder/django-covid19" alt="GitHub code size in bytes">
    <img src="https://img.shields.io/github/commit-activity/w/leafcoder/django-covid19" data-origin="https://img.shields.io/github/commit-activity/w/leafcoder/django-covid19" alt="GitHub commit activity">
    <img src="https://img.shields.io/pypi/dm/django_covid19" data-origin="https://img.shields.io/pypi/dm/django_covid19" alt="PyPI - Downloads">
</p>

</div>

本项目的数据来源为[`丁香园`](http://ncov.dxy.cn/ncovh5/view/pneumonia)，定时获取疫
情数据，保存疫情数据变更情况，以备跟踪研究和数据图表化展示。

# 快速开始 :id=quick-start

请按照以下步骤完成项目的初始化和启动。

## 代码仓库

项目开源，需要源代码可以前往仓库自行获取。

前往获取源码 [https://github.com/leafcoder/django-covid19](https://github.com/leafcoder/django-covid19)。

## 线上示例

使用本项目的接口开发了一个数据大屏的示例页面，代码在项目根目录的 `demo/` 文件夹中。

前往在线示例 [新冠肺炎实时数据大屏](http://ncov.leafcoder.cn/demo)

## 安装 :id=install

可以直接通过 `pip` 命令安装；

    pip install django_covid19

然后，将应用 `django_covid19` 和相关应用添加到你项目的 `INSTALLED_APPS`。

    INSTALLED_APPS = [
        ...
        # 以下为需要添加的部分
        'django_crontab',
        'rest_framework',
        'django_filters',
        'django_covid19'
    ]

## 初始化 :id=init

### 跨域

将应用 `corsheaders` 和相关应用添加到你项目配置文件的 `INSTALLED_APPS`。

    INSTALLED_APPS = [
        ...
        'corsheaders',
        ...
    ]


将 `corsheaders` 的 `middleware` 添加到你项目配置文件的 `MIDDLEWARE`。


    MIDDLEWARE = [
        ...
        'corsheaders.middleware.CorsMiddleware',  # 添加位置可查看应用 `corsheaders` 文档
        ...
    ]

需要加到 `settings.py` 中的跨域其他配置。

    # 跨域增加忽略
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_ALLOW_ALL = True

    CORS_ALLOW_METHODS = (
        'DELETE',
        'GET',
        'OPTIONS',
        'PATCH',
        'POST',
        'PUT',
        'VIEW',
    )

    CORS_ALLOW_HEADERS = (
        'XMLHttpRequest',
        'X_FILENAME',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
        'Pragma',
    )

### 数据库

项目示例中使用 `sqlite3` 作为数据库存储数据（推荐使用 `MySQL`）；


如果使用 `MySQL` 作为数据库，请先通过 `MySQL` 客户端创建好数据库，数据库编码推荐使用 `utf8mb4`；

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django_covid19',
            'USER': 'demo',
            'PASSWORD': 'demo',
            'HOST': 'localhost',
            'PORT': 3306,
            'OPTIONS': {
                'sql_mode': 'traditional',
                'charset': 'utf8mb4'
            }
        }
    }

### 缓存

项目缓存配置建议使用 `Redis` 作为缓存后端（项目也支持*文件*、*内存*等缓存方式）；

    CACHES = {
        'default': {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "TIMEOUT": 3600 * 24,
            "OPTIONS": {
                "MAX_ENTRIES": 200000
            }
        }
    }


### 数据库初始化

并运行以下命令完成项目数据库的初始化；

    $ ./manage.py makemigrations django_covid19
    $ ./manage.py migrate django_covid19
    $ ./manage.py migrate

### 项目后台 :id=admin

使用后台请先创建管理员账号；

    $ ./manage.py createsuperuser

在 `DEBUG = False` 的情况下，后台的静态文件将无法使用，必须运行以下命令将静态文件保存到对应目录才能正常使用项目后台；

    $ ./manage.py collectstatic

### 定时爬虫 :id=crontab

项目通过运行爬虫程序，将每一次数据的变更保存到数据库中；

请将以下配置添加到你项目配置文件 `<YOUR_PROJECT>/settings.py` 中。

    CRONTAB_LOCK_JOBS = True
    CRONJOBS = (
        # 每分钟抓取一次
        ('*/1 * * * *', 'django.core.management.call_command', ['crawl']),
    )


要创建自动抓取丁香园新冠数据任务需要运行如下命令，创建定时任务；

    $ ./manage.py crontab add

如果想要立即爬取数据，可通过项目自定义命令获取；如果丁香园数据未发生变更，爬虫并不会爬取数据。

    $ ./manage.py crawl

## 项目启动 :id=start

正式环境的部署建议使用 `nginx + uwsgi + django` 方案完成项目部署；简单运行查看接口情况，运行如下命令即可；

    $ ./manage.py runserver

运行成功后，通过浏览器访问 [`http://localhost:8000/api/statistics/`](http://localhost:8000/api/statistics/) 即可看到统计数据。

# 示例项目

通过 `pip` 安装好应 `django_covid19` 后，可以直接运行源码文件中的示例项目 `demo_proj` 查看效果。

    # 安装应用
    $ pip install django_covid19

    # 拉取源码
    $ git clone https://github.com/leafcoder/django-covid19.git

    # 初始化数据库
    $ cd django-covid19/demo_proj
    $ ./manage.py makemigrations django_covid19
    $ ./manage.py migrate

    # 运行定时爬虫
    $ ./manage.py crontab add

    # 启动项目
    $ ./manage.py runserver

# API 文档 :id=apidoc

本系统主要是将从`丁香园`获取的数据重新整合成接口返回出来。

## 全球疫情 :id=statistics

### 最新统计 :id=statistics-latest

获取最新获取到的全球整体疫情统计数据、相关文章、日常建议、推荐信息等；

接口地址：/api/statistics/latest

请求方法：GET

请求示例：

http://111.231.75.86:8000/api/statistics/latest

返回结果：

```
{
    "globalStatistics": {
        "confirmedCount": 2913206,
        "curedCount": 826309,
        "deadCount": 206245,
        "seriousCount": 0,
        "currentConfirmedCount": 1880652,
        "suspectedCount": 0
    },
    "domesticStatistics": {
        "confirmedCount": 84341,
        "curedCount": 78558,
        "deadCount": 4643,
        "seriousCount": 974,
        "currentConfirmedCount": 1140,
        "suspectedCount": 1636
    },
    "internationalStatistics": {
        "confirmedCount": 2828865,
        "curedCount": 747751,
        "deadCount": 201602,
        "seriousCount": 0,
        "currentConfirmedCount": 1879512,
        "suspectedCount": 4
    },
    "recommends": [
        {
            "contentType": 1,
            "countryType": 1,
            "title": "传染病全球大流行，历史早就告诉我们的 5 件事",
            "recordStatus": 1,
            "linkUrl": "https://mp.weixin.qq.com/s?__biz=MjA1ODMxMDQwMQ==&mid=2657278282&idx=1&sn=ec5a88bf6cead3079f2f48f68f64aa93&chksm=4906dd247e715432a91c3c99e4d92082ffd2eb8c6ddf4355b833f597d9464aa22ad048d84d0b&token=2114569265〈=zh_CN#rd",
            "imgUrl": "https://img1.dxycdn.com/2020/0325/826/3403983726425257144-135.jpg"
        }
    ],
    "remarks": [
        "易感人群：人群普遍易感。老年人及有基础疾病者感染后病情较重，儿童及婴幼儿也有发病",
        "潜伏期：一般为 3～7 天，最长不超过 14 天，潜伏期内可能存在传染性，其中无症状病例传染性非常罕见",
        "宿主：野生动物，可能为中华菊头蝠"
    ],
    "createTime": "2020-01-20T16:31:39Z",
    "generalRemark": "1. 3 月 12 日国家卫健委确诊补订遗漏 12 例确诊病例（非 12 日新增），暂无具体省份信息。 2. 浙江省 12 例外省治愈暂无具体省份信息。",
    "rumors": [
        {
            "body": "近日，有人在朋友圈兜售某公司生产的新冠病毒抗体检测试剂盒，单价 150 元，并宣称可以家庭自行使用。对此，北京市药监局提示，经批准注册的新冠病毒检测试剂盒，均需要具备 PCR 实验室及专用设备的医疗机构才能完成检测，普通市民家庭不可自行使用，市民不要轻信虚假宣传，出现相关症状应及时就医。",
            "mainSummary": "北京市药监局提示：普通市民家庭不可自行使用",
            "sourceUrl": "",
            "title": "可在家使用新冠病毒试剂盒自测？",
            "summary": "",
            "score": 1000,
            "rumorType": 0
        }
    ],
    "goodsGuides": [
        {
            "contentImgUrls": [
                "https://img1.dxycdn.com/2020/0215/220/3396780175063930893-135.png",
                "https://img1.dxycdn.com/2020/0215/637/3396780181506594738-135.png",
                "https://img1.dxycdn.com/2020/0215/372/3396780187949046019-135.png"
            ],
            "recordStatus": 1,
            "categoryName": "消毒剂",
            "title": "消毒剂指南"
        }
    ],
    "modifyTime": "2020-04-27T04:33:01Z",
    "timelines": [
        {
            "sourceUrl": "http://app.cctv.com/special/cportal/detail/arti/index.html?id=ArtiL3Kf65mSxf2yQjQ7WJpZ200427&isfromapp=1",
            "pubDate": 1587958979000,
            "title": "一季度全国社会物流总额56.0万亿元 同比下降7.5%",
            "summary": "中国物流与采购联合会今天（27日）公布一季度物流运行数据。受新冠肺炎疫情影响，一季度社会物流总需求出现负增长。一季度，全国社会物流总额为56.0万亿元，同比下降7.5%，与1-2月相比，降幅收窄4.3个百分点。 ",
            "pubDateStr": "9分钟前",
            "infoSource": "央视新闻app"
        }
    ],
    "wikis": [
        {
            "linkUrl": "https://ask.dxy.com/ama/index#/disease/24677/info/0",
            "description": "此次流行的冠状病毒为一种新发现的冠状病毒，国际病毒分类委员会命名为 SARS-Cov-2。因为人群缺少对新型病毒株的免疫力，所以人群普遍易感。",
            "imgUrl": "",
            "title": "什么是新型冠状病毒？"
        }
    ],
    "WHOArticle": {
        "linkUrl": "https://mp.weixin.qq.com/s/6q0qMFXzoKI7MMvY7zrXUw",
        "imgUrl": "https://img1.dxycdn.com/2020/0220/196/3397701576545475720-135.jpg",
        "title": "新冠病毒会变异？口罩不够怎么办？世界卫生组织的答疑来了！"
    },
    "notes": [
        "病毒：SARS-CoV-2，其导致疾病命名 COVID-19",
        "传染源：新冠肺炎的患者。无症状感染者也可能成为传染源。",
        "传播途径：经呼吸道飞沫、接触传播是主要的传播途径。气溶胶传播和消化道等传播途径尚待明确。"
    ]
}
```

### 统计列表 :id=statistics-list

获取项目从启动到当前获取到的全部疫情统计数据，分为全球、国内、国际三部分；

接口地址：/api/statistics/

请求方法：GET

请求示例：

http://111.231.75.86:8000/api/statistics/

返回结果：

```
[
    {
        "globalStatistics": {
            "confirmedCount": 2913206,
            "curedCount": 826309,
            "deadCount": 206245,
            "seriousCount": 0,
            "currentConfirmedCount": 1880652,
            "suspectedCount": 0
        },
        "domesticStatistics": {
            "confirmedCount": 84341,
            "curedCount": 78558,
            "deadCount": 4643,
            "seriousCount": 974,
            "currentConfirmedCount": 1140,
            "suspectedCount": 1636
        },
        "internationalStatistics": {
            "confirmedCount": 2828865,
            "curedCount": 747751,
            "deadCount": 201602,
            "seriousCount": 0,
            "currentConfirmedCount": 1879512,
            "suspectedCount": 4
        },
        "modifyTime": "2020-04-30T01:12:33Z",
        "createTime": "2020-01-20T16:31:39Z"
    }
]
```

## 国家疫情 :id=country

### 日统计 :id=country-daily

根据国家名称获取某个国家的疫情从 2020-01-19 到目前的疫情列表数据；

接口地址：/api/countries/\<COUNTRY_NAME\>/daily/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/countries/美国/daily/

http://111.231.75.86:8000/api/countries/巴西/daily/

返回结果：

```
[
    {
        "dateId": 20200119,
        "currentConfirmedCount": 188,
        "confirmedCount": 217,
        "suspectedCount": 0,
        "curedCount": 25,
        "deadCount": 4,
        "currentConfirmedIncr": 188,
        "confirmedIncr": 217,
        "suspectedCountIncr": 0,
        "curedIncr": 25,
        "deadIncr": 4
    },
    {
        "dateId": 20200120,
        "currentConfirmedCount": 188,
        "confirmedCount": 217,
        "suspectedCount": 0,
        "curedCount": 25,
        "deadCount": 4,
        "currentConfirmedIncr": 188,
        "confirmedIncr": 217,
        "suspectedCountIncr": 0,
        "curedIncr": 25,
        "deadIncr": 4
    },
    ...
]
```

### 所有国家 :id=country-list

获取各个国家的疫情统计数据；

接口地址：/api/countries/

请求方法：GET

请求参数：

参数                 | 描述
------------------- | -------
continents          | 所属大洲，可选值为（北美洲，南美洲，非洲，欧洲，亚洲，大洋洲，南极洲）；以逗号分割多个值；
countryShortCodes   | 国家英文缩写，如：美国的英文缩写为 USA；以逗号分割多个值；
countryNames        | 国家中文名，如：美国、中国；以逗号分割多个值；

示例链接：

http://111.231.75.86:8000/api/countries/?continents=南美洲,北美洲&countryNames=美国,巴西

返回结果：

```
[
    {
        "continents": "北美洲",
        "countryShortCode": "USA",
        "countryName": "美国",
        "countryFullName": "United States of America",
        "currentConfirmedCount": 803916,
        "confirmedCount": 965785,
        "suspectedCount": 0,
        "curedCount": 106988,
        "deadCount": 54881,
        "incrVo": {
            "confirmedIncr": 0,
            "currentConfirmedIncr": 0,
            "curedIncr": 0,
            "deadIncr": 0
        }
    }
]
```

### 国家详情 :id=country-detail

根据国家名称获取某个国家的疫情统计数据；

接口地址：/api/countries/\<COUNTRY_NAME\>/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/countries/美国/

http://111.231.75.86:8000/api/countries/巴西/

返回结果：

```
{
    "continents": "北美洲",
    "countryShortCode": "USA",
    "countryName": "美国",
    "countryFullName": "United States of America",
    "currentConfirmedCount": 803916,
    "confirmedCount": 965785,
    "suspectedCount": 0,
    "curedCount": 106988,
    "deadCount": 54881,
    "incrVo": {
        "confirmedIncr": 0,
        "currentConfirmedIncr": 0,
        "curedIncr": 0,
        "deadIncr": 0
    }
}
```

## 省/自治区/直辖市

### 日统计

通过`短省份名`获取某个中国省份（自治区、直辖市）的疫情从 2020-01-19 到目前的疫情列表数据；

接口地址：/api/provinces/\<PROVINCE_SHORT_NAME\>/daily/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/provinces/四川/daily/

http://111.231.75.86:8000/api/provinces/台湾/daily/

http://111.231.75.86:8000/api/provinces/香港/daily/

http://111.231.75.86:8000/api/provinces/澳门/daily/

返回结果：

```
[
    {
        "dateId": 20200119,
        "currentConfirmedCount": 188,
        "confirmedCount": 217,
        "suspectedCount": 0,
        "curedCount": 25,
        "deadCount": 4,
        "currentConfirmedIncr": 188,
        "confirmedIncr": 217,
        "suspectedCountIncr": 0,
        "curedIncr": 25,
        "deadIncr": 4
    },
    {
        "dateId": 20200120,
        "currentConfirmedCount": 188,
        "confirmedCount": 217,
        "suspectedCount": 0,
        "curedCount": 25,
        "deadCount": 4,
        "currentConfirmedIncr": 188,
        "confirmedIncr": 217,
        "suspectedCountIncr": 0,
        "curedIncr": 25,
        "deadIncr": 4
    },
    ...
]
```

### 省列表

获取中国各中国省/自治区/直辖市的疫情统计数据；

接口地址：/api/provinces/

请求方法：GET

请求参数：

参数                 | 描述
------------------- | -------
provinceNames       | 省份名（自治区、直辖市），如：黑龙江省、四川省、北京市；以逗号分割多个值；
provinceShortNames  | 短省份名（自治区、直辖市），如：黑龙江、四川、香港；以逗号分割多个值；


示例链接：

http://111.231.75.86:8000/api/provinces/?provinceShortNames=四川,香港

返回结果：

```
[
    {
        "provinceName": "黑龙江省",
        "provinceShortName": "黑龙江",
        "currentConfirmedCount": 367,
        "confirmedCount": 936,
        "suspectedCount": 384,
        "curedCount": 556,
        "deadCount": 13
    }
]
```

### 省详情

通过`短省份名`获取某个中国省份（自治区、直辖市）的疫情统计数据；

接口地址：/api/provinces/\<PROVINCE_SHORT_NAME\>/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/provinces/四川/

http://111.231.75.86:8000/api/provinces/台湾/

http://111.231.75.86:8000/api/provinces/香港/

http://111.231.75.86:8000/api/provinces/澳门/

返回结果：

```
{
    "provinceName": "黑龙江省",
    "provinceShortName": "黑龙江",
    "currentConfirmedCount": 367,
    "confirmedCount": 936,
    "suspectedCount": 384,
    "curedCount": 556,
    "deadCount": 13
}
```

## 城市或直辖市某区

### 城市列表

获取中国各个城市或直辖市某个区的疫情数据。

接口地址：/api/cities/

请求方法：GET

请求参数：

参数                 | 描述
------------------- | -------
provinceShortNames  | 短省份名，如：黑龙江、四川；以逗号分割多个值；
cityNames           | 城市名，如：大庆、万州区

示例链接：

http://111.231.75.86:8000/api/cities/?cityNames=大庆,万州区

返回结果：

```
[
    {
        "provinceName": "黑龙江省",
        "cityName": "境外输入",
        "currentConfirmedCount": 300,
        "confirmedCount": 386,
        "suspectedCount": 34,
        "curedCount": 86,
        "deadCount": 0
    }
]
```

### 城市详情


接口地址：/api/cities/\<CITY_NAME\>/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/cities/大庆/

返回结果：

```
{
    "provinceName": "黑龙江省",
    "cityName": "哈尔滨",
    "currentConfirmedCount": 61,
    "confirmedCount": 260,
    "suspectedCount": 8,
    "curedCount": 195,
    "deadCount": 4
}
```
