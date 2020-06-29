import os
import sys
import django_covid19

app_dir = os.path.dirname(django_covid19.__file__)
sys.path.insert(0, os.path.join(app_dir, 'spider'))

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
from nCoV.spiders.covidtracking import CovidTrackingSpider
from nCoV.spiders.dxy import DXYSpider
from nCoV.spiders.c1p3a import C1P3ASpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Scraper:
    def __init__(self):
        settings_file_path = 'nCoV.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.dxy_spider = DXYSpider
        self.covidtracking_spider = CovidTrackingSpider
        self.c1p3a_spider = C1P3ASpider

    def run_spiders(self, spider):
        spider_class = getattr(self, '%s_spider' % spider)
        self.process.crawl(spider_class)
        self.process.start()

class Command(BaseCommand):

    help = _('Crawl data from DingXiangYuan.')

    def add_arguments(self, parser):
        parser.add_argument(
            'spider', type=str, choices=['dxy', 'covidtracking', 'c1p3a'],
            help='spider name')

    def handle(self, *args, **options):
        spider = options['spider']
        scraper = Scraper()
        scraper.run_spiders(spider)
