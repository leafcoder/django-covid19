import csv
import django_covid19
import os
import posixpath
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from django_covid19.models import CountryCode

app_dir = os.path.dirname(django_covid19.__file__)


class Command(BaseCommand):

    help = _('Import country codes.')

    def handle(self, *args, **options):
        path = posixpath.join(app_dir, 'data', 'CountryCodes.csv')
        reader = csv.DictReader(open(path))
        for r in reader:
            countryCode = r['countryCode']
            CountryCode.objects.update_or_create(
                countryCode=countryCode, defaults={
                    "countryCode": countryCode,
                    "numericCode": r['numericCode'],
                    "shortCountryCode": r['shortCountryCode'],
                    "countryName": r['countryName'],
                    "englishCountryName": r['englishCountryName'],
                    "englishCountryFullName": r['englishCountryFullName'],
                    "comment": r['comment']
                })
