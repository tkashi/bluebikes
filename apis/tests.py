# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Station

class StationTests(APITestCase):
    fixtures = ['StationTests/stations']


    def test_get_stations(self):
        response = self.client.get('/stations/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 2)


    def test_get_station_detail(self):
        response = self.client.get('/stations/3/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "short_name": "B32006",
            "name": "Colleges of the Fenway - Fenway at Avenue Louis Pasteur",
            "lat": 42.34011512249236,
            "lon": -71.10061883926392,
            "region": 'Boston',
            "capacity": 15,
            "electric_bike_surcharge_waiver": False,
            "eightd_has_key_dispenser": True,
            "has_kiosk": True,
        })   
    

    def test_get_station_detail_not_found(self):
        response = self.client.get('/stations/100/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

