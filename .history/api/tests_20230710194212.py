from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Provider, ServiceArea

class ServiceAreaTests(APITestCase):
    def test_get_polygons(self):
        provider = Provider.objects.create(name='Provider1', email='provider1@example.com',
                                           phone_number='1234567890', language='English', currency='USD')
        service_area1 = ServiceArea.objects.create(name='Area1', price='10.00',
                                                   geojson={'type': 'Polygon', 'coordinates': [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]},
                                                   provider=provider)
        service_area2 = ServiceArea.objects.create(name='Area2', price='20.00',
                                                   geojson={'type': 'Polygon', 'coordinates': [[[1, 1], [1, 2], [2, 2], [2, 1], [1, 1]]]},
                                                   provider=provider)

        url = reverse('get-polygons')
        response = self.client.get(url, {'lat': 0.5, 'lng': 0.5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Area1')

        response = self.client.get(url, {'lat': 1.5, 'lng': 1.5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        names = set(item['name'] for item in response.data)
        self.assertSetEqual(names, {'Area1', 'Area2'})

