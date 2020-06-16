<div align="center">

# 新冠肺炎实时接口 :id=intro {docsify-ignore}

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

由于现在疫情高发地已从国内转向国外，所以本项目也会逐渐增加*数据源*以便提供关于*国外某国某州（某省）*的疫情数据接口。

现已新增美国各州最新疫情以及各州每日疫情统计接口。

# 快速开始 :id=quick-start

请按照以下步骤完成项目的初始化和启动。

## 代码仓库 :id=repo

项目开源，需要源代码可以前往仓库自行获取。

前往获取源码 [https://github.com/leafcoder/django-covid19](https://github.com/leafcoder/django-covid19)。

## 线上示例 :id=demo

使用本项目的接口开发了一个数据大屏的示例页面，代码在项目根目录的 `demo/` 文件夹中。

前往在线示例 [新冠肺炎实时数据大屏](http://ncov.leafcoder.cn/demo)

[![在线数据大屏](https://raw.githubusercontent.com/leafcoder/django-covid19/master/docs/images/dashboard.png)](http://111.231.75.86/dashboard)

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

### 数据库 :id=database

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

### 缓存 :id=cache

> 如果使用*内存*等无法跨进程访问的方式作为缓存后端，会导致爬虫更新数据后，缓存并不会自动删除。
> 建议使用 `Redis` 等可跨进程访问的缓存后端。

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


### 数据库初始化 :id=migrate

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
        # 每分钟抓取丁香园数据一次
        ('*/1 * * * *', 'django.core.management.call_command', ['crawl', 'dxy']),

        # 每天下午4-6点间每10分钟抓取 covidtracking 数据一次（covidtracking 每天下午4-5点间更新数据）
        # 抓取美国各州疫情数据
        ('*/10 16-18 * * *', 'django.core.management.call_command', ['crawl', 'covidtracking'])

    )

要创建自动抓取丁香园、covidtracking 新冠数据任务需要运行如下命令，创建定时任务；

    $ ./manage.py crontab add

如果想要立即爬取数据，可通过项目自定义命令获取；如果数据未发生变更，爬虫并不会爬取数据。

    $ ./manage.py crawl dxy
    $ ./manage.py crawl covidtracking

## 项目启动 :id=start

正式环境的部署建议使用 `nginx + uwsgi + django` 方案完成项目部署；简单运行查看接口情况，运行如下命令即可；

    $ ./manage.py runserver

运行成功后，通过浏览器访问 [`http://localhost:8000/api/statistics/`](http://localhost:8000/api/statistics/) 即可看到统计数据。

# 示例项目 :id=demo-project

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

## 各国疫情 :id=country

### 所有国家日统计 :id=country-list-daily

获取全球所有国家的每日统计数据，返回结果会根据国家编码（从小到大）、日期（从小到大）排列。

接口地址：/api/countries/daily/

请求方法：GET

请求参数：

参数                 | 描述
------------------- | -------
countryCodes   | 国家英文缩写，如：美国的英文缩写为 USA；以逗号分割多个值；
countryNames        | 国家中文名，如：美国、中国；以逗号分割多个值；


示例链接：

http://111.231.75.86:8000/api/countries/daily/

http://111.231.75.86:8000/api/countries/daily/?countryCodes=USA,CHN,AFG

http://111.231.75.86:8000/api/countries/daily/?countryNames=美国

返回结果：

```
[
    // 阿富汗
    {
        "confirmedCount": 1,
        "confirmedIncr": 1,
        "curedCount": 0,
        "curedIncr": 0,
        "currentConfirmedCount": 1,
        "currentConfirmedIncr": 1,
        "dateId": 20200225,
        "deadCount": 0,
        "deadIncr": 0,
        "suspectedCount": 0,
        "suspectedCountIncr": 0,
        "countryCode": "AFG",
        "countryName": "阿富汗"
    },
    ...
    //中国
    {
        "confirmedCount": 217,
        "confirmedIncr": 217,
        "curedCount": 25,
        "curedIncr": 25,
        "currentConfirmedCount": 188,
        "currentConfirmedIncr": 188,
        "dateId": 20200119,
        "deadCount": 4,
        "deadIncr": 4,
        "suspectedCount": 0,
        "suspectedCountIncr": 0,
        "countryCode": "CHN",
        "countryName": "中国"
    },
    ...
    // 美国
    {
        "confirmedCount": 1,
        "confirmedIncr": 1,
        "curedCount": 0,
        "curedIncr": 0,
        "currentConfirmedCount": 1,
        "currentConfirmedIncr": 1,
        "dateId": 20200123,
        "deadCount": 0,
        "deadIncr": 0,
        "suspectedCount": 0,
        "suspectedCountIncr": 0,
        "countryCode": "USA",
        "countryName": "美国"
    },
    ...
    // 其他国家
    ...
]
```

### 某国日统计 :id=country-daily

根据[国家代码](#/?id=国家代码)获取某个国家的疫情从 2020-01-19 到目前的疫情列表数据；

接口地址：/api/countries/\<COUNTRY_CODE\>/daily/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/countries/USA/daily/

http://111.231.75.86:8000/api/countries/BRA/daily/

返回结果：

```
[
    {
        "confirmedCount": 1,
        "confirmedIncr": 1,
        "curedCount": 0,
        "curedIncr": 0,
        "currentConfirmedCount": 1,
        "currentConfirmedIncr": 1,
        "dateId": 20200123,
        "deadCount": 0,
        "deadIncr": 0,
        "suspectedCount": 0,
        "suspectedCountIncr": 0,
        "countryCode": "USA",
        "countryName": "美国"
    },
    {
        "confirmedCount": 1,
        "confirmedIncr": 0,
        "curedCount": 0,
        "curedIncr": 0,
        "currentConfirmedCount": 1,
        "currentConfirmedIncr": 0,
        "dateId": 20200124,
        "deadCount": 0,
        "deadIncr": 0,
        "suspectedCount": 0,
        "suspectedCountIncr": 0,
        "countryCode": "USA",
        "countryName": "美国"
    },
    ...
]
```

### 所有国家最新疫情 :id=country-list

获取各个国家的疫情统计数据；

接口地址：/api/countries/

请求方法：GET

请求参数：

参数                 | 描述
------------------- | -------
continents          | 所属大洲，可选值为（北美洲，南美洲，非洲，欧洲，亚洲，大洋洲，南极洲）；以逗号分割多个值；
countryCodes        | 国家英文缩写，如：美国的英文缩写为 USA；以逗号分割多个值；
countryNames        | 国家中文名，如：美国、中国；以逗号分割多个值；

示例链接：

http://111.231.75.86:8000/api/countries/?continents=南美洲,北美洲&countryNames=美国,巴西

返回结果：

```
[
    {
        "continents": "北美洲",
        "countryCode": "USA",
        "countryName": "美国",
        "currentConfirmedCount": 1263787,
        "confirmedCount": 1850144,
        "suspectedCount": 0,
        "curedCount": 479258,
        "deadCount": 107099,
        "incrVo": {
            "currentConfirmedIncr": 2105,
            "confirmedIncr": 18414,
            "curedIncr": 15390,
            "deadIncr": 919
        }
    },
    ...
]
```

### 某国最新疫情 :id=country-detail

根据[国家代码](#/?id=国家代码)获取某个国家的疫情统计数据；

接口地址：/api/countries/\<COUNTRY_CODE\>/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/countries/USA/

http://111.231.75.86:8000/api/countries/BRA/

返回结果：

```
{
    "continents": "北美洲",
    "countryCode": "USA",
    "countryName": "美国",
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

## 中国各省、美国各州 :id=province

!> 现阶段暂时仅支持获取 `中国各省`、`美国各州` 最新数据和每日数据；

* 中国各省数据来源：丁香园；
* 美国各州数据来源：[https://covidtracking.com/](https://covidtracking.com/)，该站每日 *下午 4-5 点* 更新数据；

!> 各国疫情统计数据中，美国整体疫情数据依旧来源于 [`丁香园`](http://ncov.dxy.cn/ncovh5/view/pneumonia)，
仅美国各州疫情数据来源于 [https://covidtracking.com/](https://covidtracking.com)；

美国各州原始数据获取方式请自行参考 [https://covidtracking.com/api](https://covidtracking.com/api);

特此感谢 [ccjhpu](https://github.com/ccjhpu) 在 [issues-8](https://github.com/leafcoder/django-covid19/issues/8) 中提出的需求以及数据来源。

### 某国所有省份日统计

!> 现阶段暂时仅支持获取 `中国各省`、`美国各州` 最新数据和每日数据；

接口地址：/api/provinces/\<COUNTRY_CODE\>/daily/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/provinces/CHN/daily/

http://111.231.75.86:8000/api/provinces/USA/daily/

返回结果：

```
[
    {
        "dateId": 20200306,
        "provinceCode": "AK",
        "provinceName": "Alaska",
        "countryCode": "USA",
        "confirmedCount": 0,
        "currentConfirmedCount": 0,
        "suspectedCount": 1,
        "curedCount": null,
        "deadCount": 0,
        "currentConfirmedIncr": 0,
        "confirmedIncr": 0,
        "suspectedIncr": 0,
        "curedIncr": null,
        "deadIncr": 0
    },
    {
        "dateId": 20200307,
        "provinceCode": "AK",
        "provinceName": "Alaska",
        "countryCode": "USA",
        "confirmedCount": 0,
        "currentConfirmedCount": 0,
        "suspectedCount": 2,
        "curedCount": null,
        "deadCount": 0,
        "currentConfirmedIncr": 0,
        "confirmedIncr": 0,
        "suspectedIncr": 4,
        "curedIncr": null,
        "deadIncr": 0
    },
    ...
]
```

### 某国某省日统计 :id=province-daily

!> 现阶段暂时仅支持获取 `中国各省`、`美国各州` 最新数据和每日数据；

* [国家代码](#/?id=国家代码)
* [省、州编码](#/?id=省、州编码)

接口地址：/api/provinces/\<COUNTRY_CODE\>/\<PROVINCE_CODE\>/daily/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/provinces/CHN/TW/daily/

http://111.231.75.86:8000/api/provinces/CHN/XG/daily/

http://111.231.75.86:8000/api/provinces/CHN/AM/daily/


http://111.231.75.86:8000/api/provinces/USA/Alaska/daily/

http://111.231.75.86:8000/api/provinces/USA/AK/daily/

http://111.231.75.86:8000/api/provinces/USA/Alabama/daily/

http://111.231.75.86:8000/api/provinces/USA/AL/daily/

返回结果：

```
[
    {
        "dateId": 20200306,
        "provinceCode": "AK",
        "provinceName": "Alaska",
        "countryCode": "USA",
        "confirmedCount": 0,
        "currentConfirmedCount": 0,
        "suspectedCount": 1,
        "curedCount": null,
        "deadCount": 0,
        "currentConfirmedIncr": 0,
        "confirmedIncr": 0,
        "suspectedIncr": 0,
        "curedIncr": null,
        "deadIncr": 0
    },
    {
        "dateId": 20200307,
        "provinceCode": "AK",
        "provinceName": "Alaska",
        "countryCode": "USA",
        "confirmedCount": 0,
        "currentConfirmedCount": 0,
        "suspectedCount": 2,
        "curedCount": null,
        "deadCount": 0,
        "currentConfirmedIncr": 0,
        "confirmedIncr": 0,
        "suspectedIncr": 4,
        "curedIncr": null,
        "deadIncr": 0
    },
]
```

### 某国所有省份最新疫情 :id=province-list

!> 现阶段暂时仅支持获取 `中国各省`、`美国各州` 最新数据和每日数据；

获取某省/自治区/直辖市/州的疫情统计数据；

* [国家代码](#/?id=国家代码)

接口地址：/api/provinces/\<COUNTRY_CODE\>/

请求方法：GET

请求参数：

参数                 | 描述
------------------- | -------
provinceNames       | 省份名（自治区、直辖市），如：黑龙江、四川、香港；以逗号分割多个值；
provinceCodes       | 省份编码，如：黑龙江的编码是 HLJ；以逗号分割多个值；


示例链接：

http://111.231.75.86:8000/api/provinces/CHN/

http://111.231.75.86:8000/api/provinces/CHN/?provinceNames=四川,香港

http://111.231.75.86:8000/api/provinces/CHN/?provinceCodes=SC,XG

http://111.231.75.86:8000/api/provinces/CHN/?provinceNames=Alaska,Alabama

http://111.231.75.86:8000/api/provinces/USA/?provinceCodes=AL,AK

返回结果：

```
[
    {
        "provinceName": "Alaska",
        "provinceCode": "AK",
        "currentConfirmedCount": 0,
        "confirmedCount": 0,
        "suspectedCount": 0,
        "curedCount": 0,
        "deadCount": 0,
        "countryCode": "USA",
        "dailyUrl": "https://covidtracking.com/api/v1/states/AK/daily.json",
        "currentUrl": "https://covidtracking.com/api/v1/states/AK/current.json"
    },
    {
        "provinceName": "Alabama",
        "provinceCode": "AL",
        "currentConfirmedCount": 0,
        "confirmedCount": 0,
        "suspectedCount": 0,
        "curedCount": 0,
        "deadCount": 0,
        "countryCode": "USA",
        "dailyUrl": "https://covidtracking.com/api/v1/states/AL/daily.json",
        "currentUrl": "https://covidtracking.com/api/v1/states/AL/current.json"
    }
]
```

### 某国某省最新疫情 :id=province-detail

!> 现阶段暂时仅支持获取 `中国各省`、`美国各州` 最新数据和每日数据；

通过[省、州编码](#/?id=省、州编码)获取某省份（自治区、直辖市）的疫情统计数据；

* [国家代码](#/?id=国家代码)
* [省、州编码](#/?id=省、州编码)

接口地址：/api/provinces/\<COUNTRY_CODE\>/\<PROVINCE_CODE\>/

请求方法：GET

示例链接：


http://111.231.75.86:8000/api/provinces/CHN/TW/

http://111.231.75.86:8000/api/provinces/CHN/XG/

http://111.231.75.86:8000/api/provinces/CHN/AM/

http://111.231.75.86:8000/api/provinces/USA/Alaska/

http://111.231.75.86:8000/api/provinces/USA/AL/

返回结果：

```
{
    "provinceName": "Alabama",
    "provinceCode": "AL",
    "currentConfirmedCount": 0,
    "confirmedCount": 0,
    "suspectedCount": 0,
    "curedCount": 0,
    "deadCount": 0,
    "countryCode": "USA",
    "dailyUrl": "https://covidtracking.com/api/v1/states/AL/daily.json",
    "currentUrl": "https://covidtracking.com/api/v1/states/AL/current.json"
}
```

## 城市或直辖市某区 :id=city

!> 目前仅支持获取中国国内城市数据。

### 所有城市最新疫情 :id=city-list

获取中国各个城市或直辖市某个区的疫情数据。

接口地址：/api/cities/\<COUNTRY_CODE\>/

请求方法：GET

请求参数：

参数                 | 描述
------------------- | -------
provinceNames       | 省份名，如：黑龙江、四川；以逗号分割多个值；
cityNames           | 城市名，如：大庆、万州区

示例链接：

http://111.231.75.86:8000/api/cities/CHN/?cityNames=大庆,万州区

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

### 某城市最新疫情 :id=city-detail


接口地址：/api/cities/\<COUNTRY_CODE\>/\<CITY_NAME\>/

请求方法：GET

示例链接：

http://111.231.75.86:8000/api/cities/CHN/大庆/

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

# 附录

## 国家代码

大洲 | 国家代码 | 中文名 | 英文名
----|-----|-------|-------
亚洲 | [AFG](http://111.231.75.86:8000/api/countries/AFG/) | 阿富汗 | Afghanistan
亚洲 | [ARE](http://111.231.75.86:8000/api/countries/ARE/) | 阿联酋 | United Arab Emirates
亚洲 | [ARM](http://111.231.75.86:8000/api/countries/ARM/) | 亚美尼亚 | Armenia
亚洲 | [AZE](http://111.231.75.86:8000/api/countries/AZE/) | 阿塞拜疆 | Azerbaijan
亚洲 | [BGD](http://111.231.75.86:8000/api/countries/BGD/) | 孟加拉国 | Bangladesh
亚洲 | [BHR](http://111.231.75.86:8000/api/countries/BHR/) | 巴林 | Bahrain
亚洲 | [BRN](http://111.231.75.86:8000/api/countries/BRN/) | 文莱 | Brunei Darussalam
亚洲 | [BTN](http://111.231.75.86:8000/api/countries/BTN/) | 不丹 | Bhutan
亚洲 | [CHN](http://111.231.75.86:8000/api/countries/CHN/) | 中国 | China
亚洲 | [CYP](http://111.231.75.86:8000/api/countries/CYP/) | 塞浦路斯 | Cyprus
亚洲 | [GEO](http://111.231.75.86:8000/api/countries/GEO/) | 格鲁吉亚 | Georgia
亚洲 | [IDN](http://111.231.75.86:8000/api/countries/IDN/) | 印度尼西亚 | Indonesia
亚洲 | [IND](http://111.231.75.86:8000/api/countries/IND/) | 印度 | India
亚洲 | [IRN](http://111.231.75.86:8000/api/countries/IRN/) | 伊朗 | Iran (Islamic Republic of)
亚洲 | [IRQ](http://111.231.75.86:8000/api/countries/IRQ/) | 伊拉克 | Iraq
亚洲 | [ISR](http://111.231.75.86:8000/api/countries/ISR/) | 以色列 | Israel
亚洲 | [JOR](http://111.231.75.86:8000/api/countries/JOR/) | 约旦 | Jordan
亚洲 | [JPN](http://111.231.75.86:8000/api/countries/JPN/) | 日本 | Japan
亚洲 | [KAZ](http://111.231.75.86:8000/api/countries/KAZ/) | 哈萨克斯坦 | Kazakhstan
亚洲 | [KGZ](http://111.231.75.86:8000/api/countries/KGZ/) | 吉尔吉斯斯坦 | Kyrgyzstan
亚洲 | [KHM](http://111.231.75.86:8000/api/countries/KHM/) | 柬埔寨 | Cambodia
亚洲 | [KOR](http://111.231.75.86:8000/api/countries/KOR/) | 韩国 | Republic of Korea
亚洲 | [KWT](http://111.231.75.86:8000/api/countries/KWT/) | 科威特 | Kuwait
亚洲 | [LAO](http://111.231.75.86:8000/api/countries/LAO/) | 老挝 | Laos
亚洲 | [LBN](http://111.231.75.86:8000/api/countries/LBN/) | 黎巴嫩 | Lebanon
亚洲 | [LKA](http://111.231.75.86:8000/api/countries/LKA/) | 斯里兰卡 | Sri Lanka
亚洲 | [MDV](http://111.231.75.86:8000/api/countries/MDV/) | 马尔代夫 | Maldives
亚洲 | [MMR](http://111.231.75.86:8000/api/countries/MMR/) | 缅甸 | Myanmar
亚洲 | [MNG](http://111.231.75.86:8000/api/countries/MNG/) | 蒙古 | Mongolia
亚洲 | [MYS](http://111.231.75.86:8000/api/countries/MYS/) | 马来西亚 | Malaysia
亚洲 | [NPL](http://111.231.75.86:8000/api/countries/NPL/) | 尼泊尔 | Nepal
亚洲 | [OMN](http://111.231.75.86:8000/api/countries/OMN/) | 阿曼 | Oman
亚洲 | [PAK](http://111.231.75.86:8000/api/countries/PAK/) | 巴基斯坦 | Pakistan
亚洲 | [PHL](http://111.231.75.86:8000/api/countries/PHL/) | 菲律宾 | Philippines
亚洲 | [PSE](http://111.231.75.86:8000/api/countries/PSE/) | 巴勒斯坦 | occupied Palestinian territory
亚洲 | [QAT](http://111.231.75.86:8000/api/countries/QAT/) | 卡塔尔 | Qatar
亚洲 | [SAU](http://111.231.75.86:8000/api/countries/SAU/) | 沙特阿拉伯 | Saudi Arabia
亚洲 | [SGP](http://111.231.75.86:8000/api/countries/SGP/) | 新加坡 | Singapore
亚洲 | [SYR](http://111.231.75.86:8000/api/countries/SYR/) | 叙利亚 | Syrian ArabRepublic
亚洲 | [THA](http://111.231.75.86:8000/api/countries/THA/) | 泰国 | Thailand
亚洲 | [TJK](http://111.231.75.86:8000/api/countries/TJK/) | 塔吉克斯坦 | Tajikistan
亚洲 | [TLS](http://111.231.75.86:8000/api/countries/TLS/) | 东帝汶 | Tinor-Leste
亚洲 | [TUR](http://111.231.75.86:8000/api/countries/TUR/) | 土耳其 | Turkey
亚洲 | [UZB](http://111.231.75.86:8000/api/countries/UZB/) | 乌兹别克斯坦 | Uzbekstan
亚洲 | [VNM](http://111.231.75.86:8000/api/countries/VNM/) | 越南 | Vietnam
亚洲 | [YEM](http://111.231.75.86:8000/api/countries/YEM/) | 也门共和国 | The Republic of Yemen
其他 | [PRINCESS](http://111.231.75.86:8000/api/countries/PRINCESS/) | 钻石公主号邮轮 | International conveyance (Diamond Princess)
北美洲 | [ABW](http://111.231.75.86:8000/api/countries/ABW/) | 阿鲁巴 | Aruba
北美洲 | [AI](http://111.231.75.86:8000/api/countries/AI/) | 安圭拉 | Anguilla
北美洲 | [ATG](http://111.231.75.86:8000/api/countries/ATG/) | 安提瓜和巴布达 | Antigua & Barbuda
北美洲 | [BHS](http://111.231.75.86:8000/api/countries/BHS/) | 巴哈马 | Bahamas
北美洲 | [BL](http://111.231.75.86:8000/api/countries/BL/) | 圣巴泰勒米岛 | Saint Barthelemy
北美洲 | [BLZ](http://111.231.75.86:8000/api/countries/BLZ/) | 伯利兹 | Belize
北美洲 | [BMU](http://111.231.75.86:8000/api/countries/BMU/) | 百慕大 | Bermuda
北美洲 | [BRB](http://111.231.75.86:8000/api/countries/BRB/) | 巴巴多斯 | Barbados
北美洲 | [CAN](http://111.231.75.86:8000/api/countries/CAN/) | 加拿大 | Canada
北美洲 | [CRI](http://111.231.75.86:8000/api/countries/CRI/) | 哥斯达黎加 | Costa Rica
北美洲 | [CUB](http://111.231.75.86:8000/api/countries/CUB/) | 古巴 | Cuba
北美洲 | [CW](http://111.231.75.86:8000/api/countries/CW/) | 库拉索岛 | Curaçao
北美洲 | [CYM](http://111.231.75.86:8000/api/countries/CYM/) | 开曼群岛 | Cayman Islands
北美洲 | [DMA](http://111.231.75.86:8000/api/countries/DMA/) | 多米尼克 | Dominica
北美洲 | [DOM](http://111.231.75.86:8000/api/countries/DOM/) | 多米尼加 | Dominican Republic
北美洲 | [GLP](http://111.231.75.86:8000/api/countries/GLP/) | 瓜德罗普岛 | Guadeloupe
北美洲 | [GRD](http://111.231.75.86:8000/api/countries/GRD/) | 格林那达 | Grenada
北美洲 | [GRL](http://111.231.75.86:8000/api/countries/GRL/) | 格陵兰 | Greenland
北美洲 | [GTM](http://111.231.75.86:8000/api/countries/GTM/) | 危地马拉 | Guatemala
北美洲 | [HND](http://111.231.75.86:8000/api/countries/HND/) | 洪都拉斯 | Honduras
北美洲 | [HTI](http://111.231.75.86:8000/api/countries/HTI/) | 海地 | The Republic of Haiti
北美洲 | [JAM](http://111.231.75.86:8000/api/countries/JAM/) | 牙买加 | Jamaica
北美洲 | [KNA](http://111.231.75.86:8000/api/countries/KNA/) | 圣其茨和尼维斯 | Saint Kitts and Nevis
北美洲 | [LCA](http://111.231.75.86:8000/api/countries/LCA/) | 圣卢西亚 | Saint Lucia
北美洲 | [MEX](http://111.231.75.86:8000/api/countries/MEX/) | 墨西哥 | Mexico
北美洲 | [MS](http://111.231.75.86:8000/api/countries/MS/) | 蒙特塞拉特 | Montserrat
北美洲 | [MTQ](http://111.231.75.86:8000/api/countries/MTQ/) | 马提尼克 | Martinique
北美洲 | [NIC](http://111.231.75.86:8000/api/countries/NIC/) | 尼加拉瓜 | Nicaragua
北美洲 | [PAN](http://111.231.75.86:8000/api/countries/PAN/) | 巴拿马 | Panama
北美洲 | [PRI](http://111.231.75.86:8000/api/countries/PRI/) | 波多黎各 | Puerto Rico
北美洲 | [SLV](http://111.231.75.86:8000/api/countries/SLV/) | 萨尔瓦多 | The Republic of El Salvador
北美洲 | [SPM](http://111.231.75.86:8000/api/countries/SPM/) | 圣皮埃尔和密克隆群岛 | Saint Pierre and Miquelon
北美洲 | [MAF](http://111.231.75.86:8000/api/countries/MAF/) | 圣马丁岛 | Saint Martin
北美洲 | [SXM](http://111.231.75.86:8000/api/countries/SXM/) | 荷属圣马丁 | Sint Maarten
北美洲 | [TCA](http://111.231.75.86:8000/api/countries/TCA/) | 特克斯和凯科斯群岛 | Turks & Caicos Islands
北美洲 | [TTO](http://111.231.75.86:8000/api/countries/TTO/) | 特立尼达和多巴哥 | Trinidad & Tobago
北美洲 | [USA](http://111.231.75.86:8000/api/countries/USA/) | 美国 | United States of America
北美洲 | [USVI](http://111.231.75.86:8000/api/countries/USVI/) | 美属维尔京群岛 | United States Virgin Islands
北美洲 | [VCT](http://111.231.75.86:8000/api/countries/VCT/) | 圣文森特和格林纳丁斯 | Saint Vincent and the Grenadines
北美洲 | [VG](http://111.231.75.86:8000/api/countries/VG/) | 英属维尔京群岛 | VirginIslands,British
南美洲 | [ARG](http://111.231.75.86:8000/api/countries/ARG/) | 阿根廷 | Argentina
南美洲 | [BES](http://111.231.75.86:8000/api/countries/BES/) | 荷兰加勒比地区 | Bonaire, Sint Eustatius and Saba
南美洲 | [BOL](http://111.231.75.86:8000/api/countries/BOL/) | 玻利维亚 | Bolivia (Plurinational State of)
南美洲 | [BRA](http://111.231.75.86:8000/api/countries/BRA/) | 巴西 | Brazil
南美洲 | [CHL](http://111.231.75.86:8000/api/countries/CHL/) | 智利 | Chile
南美洲 | [COL](http://111.231.75.86:8000/api/countries/COL/) | 哥伦比亚 | Colombia
南美洲 | [ECU](http://111.231.75.86:8000/api/countries/ECU/) | 厄瓜多尔 | Ecuador
南美洲 | [FLK](http://111.231.75.86:8000/api/countries/FLK/) | 福克兰群岛 | Falkland Islands
南美洲 | [GUF](http://111.231.75.86:8000/api/countries/GUF/) | 法属圭亚那 | French Guiana
南美洲 | [GUY](http://111.231.75.86:8000/api/countries/GUY/) | 圭亚那 | Guyana
南美洲 | [PER](http://111.231.75.86:8000/api/countries/PER/) | 秘鲁 | Peru
南美洲 | [PRY](http://111.231.75.86:8000/api/countries/PRY/) | 巴拉圭 | Paraguay
南美洲 | [SUR](http://111.231.75.86:8000/api/countries/SUR/) | 苏里南 | Suriname
南美洲 | [URY](http://111.231.75.86:8000/api/countries/URY/) | 乌拉圭 | Uruguay
南美洲 | [VEN](http://111.231.75.86:8000/api/countries/VEN/) | 委内瑞拉 | Venezuela
大洋洲 | [AUS](http://111.231.75.86:8000/api/countries/AUS/) | 澳大利亚 | Australia
大洋洲 | [CNMI](http://111.231.75.86:8000/api/countries/CNMI/) | 北马里亚纳群岛联邦 | Northern Mariana Islands (Commonwealth of the)
大洋洲 | [FJI](http://111.231.75.86:8000/api/countries/FJI/) | 斐济 | The Republic of Fiji
大洋洲 | [GU](http://111.231.75.86:8000/api/countries/GU/) | 关岛 | Guam
大洋洲 | [NCL](http://111.231.75.86:8000/api/countries/NCL/) | 新喀里多尼亚 | New Caledonia
大洋洲 | [NZL](http://111.231.75.86:8000/api/countries/NZL/) | 新西兰 | New Zealand
大洋洲 | [PNG](http://111.231.75.86:8000/api/countries/PNG/) | 巴布亚新几内亚 | Papua New Guinea
大洋洲 | [PYF](http://111.231.75.86:8000/api/countries/PYF/) | 法属波利尼西亚 | French Polynesia
欧洲 | [ALB](http://111.231.75.86:8000/api/countries/ALB/) | 阿尔巴尼亚 | Albania
欧洲 | [AND](http://111.231.75.86:8000/api/countries/AND/) | 安道尔 | Andorra
欧洲 | [AUT](http://111.231.75.86:8000/api/countries/AUT/) | 奥地利 | Austria
欧洲 | [BEL](http://111.231.75.86:8000/api/countries/BEL/) | 比利时 | Belgium
欧洲 | [BGR](http://111.231.75.86:8000/api/countries/BGR/) | 保加利亚 | Bulgaria
欧洲 | [BIH](http://111.231.75.86:8000/api/countries/BIH/) | 波黑 | Bosnia and Herzegovina
欧洲 | [BLR](http://111.231.75.86:8000/api/countries/BLR/) | 白俄罗斯 | Belarus
欧洲 | [CHE](http://111.231.75.86:8000/api/countries/CHE/) | 瑞士 | Switzerland
欧洲 | [CIB](http://111.231.75.86:8000/api/countries/CIB/) | 直布罗陀 | Gibraltar
欧洲 | [CZE](http://111.231.75.86:8000/api/countries/CZE/) | 捷克 | Czechia
欧洲 | [DEU](http://111.231.75.86:8000/api/countries/DEU/) | 德国 | Germany
欧洲 | [DNK](http://111.231.75.86:8000/api/countries/DNK/) | 丹麦 | Denmark
欧洲 | [ESP](http://111.231.75.86:8000/api/countries/ESP/) | 西班牙 | Spain
欧洲 | [EST](http://111.231.75.86:8000/api/countries/EST/) | 爱沙尼亚 | Estonia
欧洲 | [FIN](http://111.231.75.86:8000/api/countries/FIN/) | 芬兰 | Finland
欧洲 | [FO](http://111.231.75.86:8000/api/countries/FO/) | 法罗群岛 | Faroe Islands
欧洲 | [FRA](http://111.231.75.86:8000/api/countries/FRA/) | 法国 | France
欧洲 | [GBR](http://111.231.75.86:8000/api/countries/GBR/) | 英国 | The United Kingdom
欧洲 | [GG](http://111.231.75.86:8000/api/countries/GG/) | 根西岛 | Guernsey
欧洲 | [GRC](http://111.231.75.86:8000/api/countries/GRC/) | 希腊 | Greece
欧洲 | [HRV](http://111.231.75.86:8000/api/countries/HRV/) | 克罗地亚 | Croatia
欧洲 | [HUN](http://111.231.75.86:8000/api/countries/HUN/) | 匈牙利 | Hungary
欧洲 | [IRL](http://111.231.75.86:8000/api/countries/IRL/) | 爱尔兰 | Ireland
欧洲 | [ISL](http://111.231.75.86:8000/api/countries/ISL/) | 冰岛 | Iceland
欧洲 | [ITA](http://111.231.75.86:8000/api/countries/ITA/) | 意大利 | Italy
欧洲 | [JE](http://111.231.75.86:8000/api/countries/JE/) | 泽西岛 | Jersey
欧洲 | [LIE](http://111.231.75.86:8000/api/countries/LIE/) | 列支敦士登 | Liechtenstein
欧洲 | [LTU](http://111.231.75.86:8000/api/countries/LTU/) | 立陶宛 | Lithuania
欧洲 | [LUX](http://111.231.75.86:8000/api/countries/LUX/) | 卢森堡 | Luxembourg
欧洲 | [LVA](http://111.231.75.86:8000/api/countries/LVA/) | 拉脱维亚 | Latvia
欧洲 | [MCO](http://111.231.75.86:8000/api/countries/MCO/) | 摩纳哥 | Monaco
欧洲 | [MDA](http://111.231.75.86:8000/api/countries/MDA/) | 摩尔多瓦 | Republic of Moldova
欧洲 | [MKD](http://111.231.75.86:8000/api/countries/MKD/) | 北马其顿 | North Macedonia
欧洲 | [MLT](http://111.231.75.86:8000/api/countries/MLT/) | 马耳他 | Malta
欧洲 | [MNE](http://111.231.75.86:8000/api/countries/MNE/) | 黑山 | Montenegro
欧洲 | [Mann](http://111.231.75.86:8000/api/countries/Mann/) | 马恩岛 | Isle of Man
欧洲 | [NLD](http://111.231.75.86:8000/api/countries/NLD/) | 荷兰 | Netherlands
欧洲 | [NOR](http://111.231.75.86:8000/api/countries/NOR/) | 挪威 | Norway
欧洲 | [POL](http://111.231.75.86:8000/api/countries/POL/) | 波兰 | Poland
欧洲 | [PRT](http://111.231.75.86:8000/api/countries/PRT/) | 葡萄牙 | Portugal
欧洲 | [ROU](http://111.231.75.86:8000/api/countries/ROU/) | 罗马尼亚 | Romania
欧洲 | [RUS](http://111.231.75.86:8000/api/countries/RUS/) | 俄罗斯 | Russian Federation
欧洲 | [SMR](http://111.231.75.86:8000/api/countries/SMR/) | 圣马力诺 | San Marino
欧洲 | [SRB](http://111.231.75.86:8000/api/countries/SRB/) | 塞尔维亚 | Serbia
欧洲 | [SVK](http://111.231.75.86:8000/api/countries/SVK/) | 斯洛伐克 | Slovakia
欧洲 | [SVN](http://111.231.75.86:8000/api/countries/SVN/) | 斯洛文尼亚 | Slovenia
欧洲 | [SWE](http://111.231.75.86:8000/api/countries/SWE/) | 瑞典 | Sweden
欧洲 | [UKR](http://111.231.75.86:8000/api/countries/UKR/) | 乌克兰 | Ukraine
欧洲 | [VAT](http://111.231.75.86:8000/api/countries/VAT/) | 梵蒂冈 | Holy See
非洲 | [AGO](http://111.231.75.86:8000/api/countries/AGO/) | 安哥拉 | Angola
非洲 | [BDI](http://111.231.75.86:8000/api/countries/BDI/) | 布隆迪共和国 | The Republic of Burundi
非洲 | [BEN](http://111.231.75.86:8000/api/countries/BEN/) | 贝宁 | Benin
非洲 | [BFA](http://111.231.75.86:8000/api/countries/BFA/) | 布基纳法索 | Burkina Faso
非洲 | [BWA](http://111.231.75.86:8000/api/countries/BWA/) | 博茨瓦纳 | Botswana
非洲 | [CAF](http://111.231.75.86:8000/api/countries/CAF/) | 中非共和国 | Central African Republic
非洲 | [CIV](http://111.231.75.86:8000/api/countries/CIV/) | 科特迪瓦 | Cote d Ivoire
非洲 | [CMR](http://111.231.75.86:8000/api/countries/CMR/) | 喀麦隆 | Cameroon
非洲 | [COD](http://111.231.75.86:8000/api/countries/COD/) | 刚果（金） | Democratic Republic of the Congo
非洲 | [COG](http://111.231.75.86:8000/api/countries/COG/) | 刚果（布） | Congo
非洲 | [COM](http://111.231.75.86:8000/api/countries/COM/) | 科摩罗 | Union des Comores
非洲 | [CPV](http://111.231.75.86:8000/api/countries/CPV/) | 佛得角 | Cabo Verde
非洲 | [DJI](http://111.231.75.86:8000/api/countries/DJI/) | 吉布提 | The Republic of Djibouti
非洲 | [DZA](http://111.231.75.86:8000/api/countries/DZA/) | 阿尔及利亚 | Algeria
非洲 | [EGY](http://111.231.75.86:8000/api/countries/EGY/) | 埃及 | Egypt
非洲 | [ERI](http://111.231.75.86:8000/api/countries/ERI/) | 厄立特里亚 | Eritrea
非洲 | [ETH](http://111.231.75.86:8000/api/countries/ETH/) | 埃塞俄比亚 | Ethiopia
非洲 | [GAB](http://111.231.75.86:8000/api/countries/GAB/) | 加蓬 | Gabon
非洲 | [GBN](http://111.231.75.86:8000/api/countries/GBN/) | 几内亚比绍 | Guinea-Bissau
非洲 | [GHA](http://111.231.75.86:8000/api/countries/GHA/) | 加纳 | Ghana
非洲 | [GIN](http://111.231.75.86:8000/api/countries/GIN/) | 几内亚 | Guinea
非洲 | [GMB](http://111.231.75.86:8000/api/countries/GMB/) | 冈比亚 | Gambia
非洲 | [GNQ](http://111.231.75.86:8000/api/countries/GNQ/) | 赤道几内亚 | Eq.Guinea
非洲 | [KEN](http://111.231.75.86:8000/api/countries/KEN/) | 肯尼亚 | Kenya
非洲 | [LBR](http://111.231.75.86:8000/api/countries/LBR/) | 利比里亚 | Liberia
非洲 | [LBY](http://111.231.75.86:8000/api/countries/LBY/) | 利比亚 | Libya
非洲 | [LSO](http://111.231.75.86:8000/api/countries/LSO/) | 莱索托 | Lesotho
非洲 | [MAR](http://111.231.75.86:8000/api/countries/MAR/) | 摩洛哥 | Morocco
非洲 | [MDG](http://111.231.75.86:8000/api/countries/MDG/) | 马达加斯加 | Madagascar
非洲 | [MLI](http://111.231.75.86:8000/api/countries/MLI/) | 马里 | Mali
非洲 | [MOZ](http://111.231.75.86:8000/api/countries/MOZ/) | 莫桑比克 | Mozambique
非洲 | [MRT](http://111.231.75.86:8000/api/countries/MRT/) | 毛里塔尼亚 | Mauritania
非洲 | [MUS](http://111.231.75.86:8000/api/countries/MUS/) | 毛里求斯 | Mauritius
非洲 | [MWI](http://111.231.75.86:8000/api/countries/MWI/) | 马拉维 | Malawi
非洲 | [MYT](http://111.231.75.86:8000/api/countries/MYT/) | 马约特 | Mayotte
非洲 | [NAM](http://111.231.75.86:8000/api/countries/NAM/) | 纳米比亚 | Namibia
非洲 | [NER](http://111.231.75.86:8000/api/countries/NER/) | 尼日尔 | Niger
非洲 | [NGA](http://111.231.75.86:8000/api/countries/NGA/) | 尼日利亚 | Nigeria
非洲 | [REU](http://111.231.75.86:8000/api/countries/REU/) | 留尼旺 | Réunion
非洲 | [RWA](http://111.231.75.86:8000/api/countries/RWA/) | 卢旺达 | Rwanda
非洲 | [SDN](http://111.231.75.86:8000/api/countries/SDN/) | 苏丹 | Sudan
非洲 | [SEN](http://111.231.75.86:8000/api/countries/SEN/) | 塞内加尔 | Senegal
非洲 | [SLE](http://111.231.75.86:8000/api/countries/SLE/) | 塞拉利昂 | Sierra Leone
非洲 | [SOM](http://111.231.75.86:8000/api/countries/SOM/) | 索马里 | Somalia
非洲 | [SSD](http://111.231.75.86:8000/api/countries/SSD/) | 南苏丹 | South Sudan
非洲 | [STP](http://111.231.75.86:8000/api/countries/STP/) | 圣多美和普林西比 | São Tomé and Príncipe
非洲 | [SWZ](http://111.231.75.86:8000/api/countries/SWZ/) | 斯威士兰 | Swaziland
非洲 | [SYC](http://111.231.75.86:8000/api/countries/SYC/) | 塞舌尔 | Seychelles
非洲 | [TCD](http://111.231.75.86:8000/api/countries/TCD/) | 乍得 | Chad
非洲 | [TGO](http://111.231.75.86:8000/api/countries/TGO/) | 多哥 | Togo
非洲 | [TUN](http://111.231.75.86:8000/api/countries/TUN/) | 突尼斯 | Tunisia
非洲 | [TZA](http://111.231.75.86:8000/api/countries/TZA/) | 坦桑尼亚 | Tanzania
非洲 | [UGA](http://111.231.75.86:8000/api/countries/UGA/) | 乌干达 | Uganda
非洲 | [ZAF](http://111.231.75.86:8000/api/countries/ZAF/) | 南非 | South Africa
非洲 | [ZMB](http://111.231.75.86:8000/api/countries/ZMB/) | 赞比亚共和国 | The Republic of Zambia
非洲 | [ZWE](http://111.231.75.86:8000/api/countries/ZWE/) | 津巴布韦 | Zimbabwe

## 省、州编码


国家代码 | 省代码 | 省名、州名
-------|-------|-------
CHN | [AH](http://111.231.75.86:8000/api/provinces/CHN/AH/) | 安徽
CHN | [AM](http://111.231.75.86:8000/api/provinces/CHN/AM/) | 澳门
CHN | [BJ](http://111.231.75.86:8000/api/provinces/CHN/BJ/) | 北京
CHN | [CQ](http://111.231.75.86:8000/api/provinces/CHN/CQ/) | 重庆
CHN | [FJ](http://111.231.75.86:8000/api/provinces/CHN/FJ/) | 福建
CHN | [GD](http://111.231.75.86:8000/api/provinces/CHN/GD/) | 广东
CHN | [GS](http://111.231.75.86:8000/api/provinces/CHN/GS/) | 甘肃
CHN | [GX](http://111.231.75.86:8000/api/provinces/CHN/GX/) | 广西
CHN | [GZ](http://111.231.75.86:8000/api/provinces/CHN/GZ/) | 贵州
CHN | [HB](http://111.231.75.86:8000/api/provinces/CHN/HB/) | 湖北
CHN | [HB-1](http://111.231.75.86:8000/api/provinces/CHN/HB-1/) | 河北
CHN | [HLJ](http://111.231.75.86:8000/api/provinces/CHN/HLJ/) | 黑龙江
CHN | [HN](http://111.231.75.86:8000/api/provinces/CHN/HN/) | 湖南
CHN | [HN-1](http://111.231.75.86:8000/api/provinces/CHN/HN-1/) | 河南
CHN | [HN-2](http://111.231.75.86:8000/api/provinces/CHN/HN-2/) | 海南
CHN | [JL](http://111.231.75.86:8000/api/provinces/CHN/JL/) | 吉林
CHN | [JS](http://111.231.75.86:8000/api/provinces/CHN/JS/) | 江苏
CHN | [JX](http://111.231.75.86:8000/api/provinces/CHN/JX/) | 江西
CHN | [LN](http://111.231.75.86:8000/api/provinces/CHN/LN/) | 辽宁
CHN | [NMG](http://111.231.75.86:8000/api/provinces/CHN/NMG/) | 内蒙古
CHN | [NX](http://111.231.75.86:8000/api/provinces/CHN/NX/) | 宁夏
CHN | [QH](http://111.231.75.86:8000/api/provinces/CHN/QH/) | 青海
CHN | [SC](http://111.231.75.86:8000/api/provinces/CHN/SC/) | 四川
CHN | [SD](http://111.231.75.86:8000/api/provinces/CHN/SD/) | 山东
CHN | [SH](http://111.231.75.86:8000/api/provinces/CHN/SH/) | 上海
CHN | [SX](http://111.231.75.86:8000/api/provinces/CHN/SX/) | 陕西
CHN | [SX-1](http://111.231.75.86:8000/api/provinces/CHN/SX-1/) | 山西
CHN | [TJ](http://111.231.75.86:8000/api/provinces/CHN/TJ/) | 天津
CHN | [TW](http://111.231.75.86:8000/api/provinces/CHN/TW/) | 台湾
CHN | [XG](http://111.231.75.86:8000/api/provinces/CHN/XG/) | 香港
CHN | [XJ](http://111.231.75.86:8000/api/provinces/CHN/XJ/) | 新疆
CHN | [XZ](http://111.231.75.86:8000/api/provinces/CHN/XZ/) | 西藏
CHN | [YN](http://111.231.75.86:8000/api/provinces/CHN/YN/) | 云南
CHN | [ZJ](http://111.231.75.86:8000/api/provinces/CHN/ZJ/) | 浙江
USA | [AK](http://111.231.75.86:8000/api/provinces/USA/AK/) | Alaska
USA | [AL](http://111.231.75.86:8000/api/provinces/USA/AL/) | Alabama
USA | [AR](http://111.231.75.86:8000/api/provinces/USA/AR/) | Arkansas
USA | [AS](http://111.231.75.86:8000/api/provinces/USA/AS/) | AmericanSamoa
USA | [AZ](http://111.231.75.86:8000/api/provinces/USA/AZ/) | Arizona
USA | [CA](http://111.231.75.86:8000/api/provinces/USA/CA/) | California
USA | [CO](http://111.231.75.86:8000/api/provinces/USA/CO/) | Colorado
USA | [CT](http://111.231.75.86:8000/api/provinces/USA/CT/) | Connecticut
USA | [DC](http://111.231.75.86:8000/api/provinces/USA/DC/) | DistrictOfColumbia
USA | [DE](http://111.231.75.86:8000/api/provinces/USA/DE/) | Delaware
USA | [FL](http://111.231.75.86:8000/api/provinces/USA/FL/) | Florida
USA | [GA](http://111.231.75.86:8000/api/provinces/USA/GA/) | Georgia
USA | [GU](http://111.231.75.86:8000/api/provinces/USA/GU/) | Guam
USA | [HI](http://111.231.75.86:8000/api/provinces/USA/HI/) | Hawaii
USA | [IA](http://111.231.75.86:8000/api/provinces/USA/IA/) | Iowa
USA | [ID](http://111.231.75.86:8000/api/provinces/USA/ID/) | Idaho
USA | [IL](http://111.231.75.86:8000/api/provinces/USA/IL/) | Illinois
USA | [IN](http://111.231.75.86:8000/api/provinces/USA/IN/) | Indiana
USA | [KS](http://111.231.75.86:8000/api/provinces/USA/KS/) | Kansas
USA | [KY](http://111.231.75.86:8000/api/provinces/USA/KY/) | Kentucky
USA | [LA](http://111.231.75.86:8000/api/provinces/USA/LA/) | Louisiana
USA | [MA](http://111.231.75.86:8000/api/provinces/USA/MA/) | Massachusetts
USA | [MD](http://111.231.75.86:8000/api/provinces/USA/MD/) | Maryland
USA | [ME](http://111.231.75.86:8000/api/provinces/USA/ME/) | Maine
USA | [MI](http://111.231.75.86:8000/api/provinces/USA/MI/) | Michigan
USA | [MN](http://111.231.75.86:8000/api/provinces/USA/MN/) | Minnesota
USA | [MO](http://111.231.75.86:8000/api/provinces/USA/MO/) | Missouri
USA | [MP](http://111.231.75.86:8000/api/provinces/USA/MP/) | NorthernMarianaIslands
USA | [MS](http://111.231.75.86:8000/api/provinces/USA/MS/) | Mississippi
USA | [MT](http://111.231.75.86:8000/api/provinces/USA/MT/) | Montana
USA | [NC](http://111.231.75.86:8000/api/provinces/USA/NC/) | NorthCarolina
USA | [ND](http://111.231.75.86:8000/api/provinces/USA/ND/) | NorthDakota
USA | [NE](http://111.231.75.86:8000/api/provinces/USA/NE/) | Nebraska
USA | [NH](http://111.231.75.86:8000/api/provinces/USA/NH/) | NewHampshire
USA | [NJ](http://111.231.75.86:8000/api/provinces/USA/NJ/) | NewJersey
USA | [NM](http://111.231.75.86:8000/api/provinces/USA/NM/) | NewMexico
USA | [NV](http://111.231.75.86:8000/api/provinces/USA/NV/) | Nevada
USA | [NY](http://111.231.75.86:8000/api/provinces/USA/NY/) | NewYork
USA | [OH](http://111.231.75.86:8000/api/provinces/USA/OH/) | Ohio
USA | [OK](http://111.231.75.86:8000/api/provinces/USA/OK/) | Oklahoma
USA | [OR](http://111.231.75.86:8000/api/provinces/USA/OR/) | Oregon
USA | [PA](http://111.231.75.86:8000/api/provinces/USA/PA/) | Pennsylvania
USA | [PR](http://111.231.75.86:8000/api/provinces/USA/PR/) | PuertoRico
USA | [RI](http://111.231.75.86:8000/api/provinces/USA/RI/) | RhodeIsland
USA | [SC](http://111.231.75.86:8000/api/provinces/USA/SC/) | SouthCarolina
USA | [SD](http://111.231.75.86:8000/api/provinces/USA/SD/) | SouthDakota
USA | [TN](http://111.231.75.86:8000/api/provinces/USA/TN/) | Tennessee
USA | [TX](http://111.231.75.86:8000/api/provinces/USA/TX/) | Texas
USA | [UT](http://111.231.75.86:8000/api/provinces/USA/UT/) | Utah
USA | [VA](http://111.231.75.86:8000/api/provinces/USA/VA/) | Virginia
USA | [VI](http://111.231.75.86:8000/api/provinces/USA/VI/) | USVirginIslands
USA | [VT](http://111.231.75.86:8000/api/provinces/USA/VT/) | Vermont
USA | [WA](http://111.231.75.86:8000/api/provinces/USA/WA/) | Washington
USA | [WI](http://111.231.75.86:8000/api/provinces/USA/WI/) | Wisconsin
USA | [WV](http://111.231.75.86:8000/api/provinces/USA/WV/) | WestVirginia
USA | [WY](http://111.231.75.86:8000/api/provinces/USA/WY/) | Wyoming