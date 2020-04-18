# 新冠肺炎疫情数据接口（数据来源：丁香园）

请按照以下步骤完成项目的初始化和启动。

> 注意：请先修改 covid19/settings.py 中 `SCRAPY_CMD`，设置为 scrapy 命令完整路径。

## 启动服务前，请先安装项目依赖包。

    $ pip install -r requirement.txt

## 初始化

    $ ./manage.py makemigrations ncovapi
    $ ./manage.py migrate

## 创建自动抓取丁香园新冠数据任务

    $ ./manage.py crontab add

## 启动

    $ ./manage.py runserver

## 接口文档

详情见查看项目目录 [`docs`](https://github.com/leafcoder/django-covid19/docs)。