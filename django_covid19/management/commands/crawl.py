import os
import sys
import django_covid19

app_dir = os.path.dirname(django_covid19.__file__)
sys.path.insert(0, os.path.join(app_dir, 'spider'))

from nCoV.spiders.dxy import DXYSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

class Scraper:
    def __init__(self):
        settings_file_path = 'nCoV.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = DXYSpider

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start()

class Command(BaseCommand):

    help = _('Crawl data from DingXiangYuan.')

    def handle(self, *args, **options):
        scraper = Scraper()
        scraper.run_spiders()
