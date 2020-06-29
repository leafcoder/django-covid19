import json
import scrapy
import logging
from scrapy.selector import Selector

from .. import items

from django.core.cache import cache
from django.utils.timezone import datetime, make_aware

logger = logging.getLogger()

import re

find_standby = re.compile(r'JSON\.parse\(').findall

class C1P3ASpider(scrapy.Spider):

    """中美除外其他国家、地区最新疫情和疫情日统计"""

    name = "C1P3A"
    allowed_domains = ["coronavirus.1point3acres.com"]
    start_urls = [
        "https://coronavirus.1point3acres.com/zh/world",
    ]

    base_url = 'https://coronavirus.1point3acres.com'

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath(
            '//link[@rel="preload"][@as="script"]').xpath('@href').getall()
        for link in links:
            if 'chunks' not in link:
                continue
            full_url = ''.join((self.base_url, link))
            request = scrapy.Request(full_url, callback=self.parse_chunk)
            yield request

    def parse_chunk(self, response):
        result = find_standby(response.text)
        if not result:
            logger.info('ignore %s', response.url)
            return
        countries = Selector(response).re(
            r'e\.exports\s*\=\s*JSON\.parse\(\'([^\=]*\})\'\)(?:\,)?')
        if not countries:
            logger.info('ignore %s', response.url)
            return
