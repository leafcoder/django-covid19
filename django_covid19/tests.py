from django.test import TestCase
from django.test.client import Client as DjangoClient

from django.urls import reverse

# Create your tests here.

class StatisticsTestCase(TestCase):

    """Supporting Chinese cities only."""

    fixtures = ['statistics.json']

    def test_list_view_status_code(self):
        url = reverse('django_covid19:statistics-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_latest_view_status_code(self):
        url = reverse('django_covid19:statistics-latest')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class CountriesTestCase(TestCase):

    fixtures = ['country.json']
    countryCode = 'USA'

    def test_list_view_status_code(self):
        url = reverse('django_covid19:country-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        for item in response.json():
            self.assertEquals('countryCode' in item, True)
            self.assertEquals('countryName' in item, True)
            self.assertEquals('continents' in item, True)

    def test_list_daily_view_status_code(self):
        url = reverse('django_covid19:country-list-daily')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_view_status_code(self):
        kwargs = {'countryCode': self.countryCode}
        url = reverse('django_covid19:country-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_daily_view_status_code(self):
        kwargs = {'countryCode': self.countryCode}
        url = reverse('django_covid19:country-daily', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class ProvincesTestCase(TestCase):

    fixtures = ['province.json']

    countryCode = 'USA'
    provinceCode = 'AL'
    provinceName = 'Alabama'

    def test_list_view_status_code(self):
        kwargs = {'countryCode': self.countryCode}
        url = reverse('django_covid19:province-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_daily_view_status_code(self):
        kwargs = {'countryCode': self.countryCode}
        url = reverse('django_covid19:province-list-daily', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_daily_view_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'provinceCode': self.provinceCode
        }
        url = reverse('django_covid19:province-daily', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_daily_by_name_view_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'provinceName': self.provinceName
        }
        url = reverse('django_covid19:province-daily-by-name', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_view_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'provinceCode': self.provinceCode
        }
        url = reverse('django_covid19:province-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_by_nameview_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'provinceName': self.provinceName
        }
        url = reverse('django_covid19:province-detail-by-name', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class CitiesTestCase(TestCase):

    """Supporting Chinese cities only."""

    fixtures = ['city.json']

    countryCode = 'CHN'
    cityName = '深圳'

    def test_list_view_status_code(self):
        kwargs = {'countryCode': self.countryCode,}
        url = reverse('django_covid19:city-list', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_view_status_code(self):
        kwargs = {
            'countryCode': self.countryCode,
            'cityName': self.cityName
        }
        url = reverse('django_covid19:city-detail', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
