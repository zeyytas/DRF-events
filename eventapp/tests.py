import json

from rest_framework.test import APITestCase
from django.core import serializers
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from eventapp.models import Event


class DatasetFilterTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('dataset-list')
        queries = [{'country': 'US', 'date': '2017-05-27', 'checkin_count': 5406, 'session_count': 56767,
                    'revenue': 322554},
                   {'country': 'US', 'name': 'Facebook', 'date': '2018-09-17', 'checkin_count': 3444,
                    'session_count': 5767, 'revenue': 3467674},
                   {'country': 'US', 'name': 'Google', 'date': '2017-06-29', 'checkin_count': 333, 'revenue': 66665},
                   {'country': 'CA', 'date': '2018-06-23', 'installs': 399, 'checkin_count': 4654, 'session_count': 12,
                    'revenue': 546564}]

        for query in queries:
            Event.objects.create(**query)

    def test_params1(self):
        params = {'country': 'US', 'date_to': '2019-05-27'}
        response = json.loads(json.dumps(self.client.get(self.url, params, format='json').data.get('results')))[0]

        for key in ['tp', 'id']:
            response.pop(key)

        queryset = json.loads(serializers.serialize(
            queryset=Event.objects.filter(country='US',  date__lte='2019-05-27'),
            format='json'))[0]['fields']

        self.assertDictEqual(response, queryset )