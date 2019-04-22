# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Station

class StationDetailTests(APITestCase):
    fixtures = ['StationDetailTests/stations']

    def test_get_station_detail(self):
        response = self.client.get('/apis/stations/3/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "station_id": 3,
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
    
    def test_get_station_detail_region(self):
        response = self.client.get('/apis/stations/67/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["region"], "Cambridge")
    

    def test_get_station_detail_not_found(self):
        response = self.client.get('/stations/100/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_station_detail_with_fields_filter(self):
        response = self.client.get('/apis/stations/3/', {'fields': 'station_id'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { "station_id": 3 })


    def test_get_station_detail_with_multiple_fields_filter(self):
        response = self.client.get('/apis/stations/3/', {'fields': 'station_id,short_name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { 
            "station_id": 3,
            "short_name": "B32006"
        })


    def test_get_station_detail_with_omit_filter(self):
        response = self.client.get('/apis/stations/3/', {'omit': 'station_id,short_name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { 
            "name": "Colleges of the Fenway - Fenway at Avenue Louis Pasteur",
            "lat": 42.34011512249236,
            "lon": -71.10061883926392,
            "region": 'Boston',
            "capacity": 15,
            "electric_bike_surcharge_waiver": False,
            "eightd_has_key_dispenser": True,
            "has_kiosk": True,
        })

    
    # if one field is specified by 'fields' and 'omit', then it should be excluded
    def test_get_station_detail_with_both_omit_and_fields_filter(self):
        response = self.client.get('/apis/stations/3/', {'fields': 'station_id,short_name', 'omit': 'station_id'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { 
            "short_name": "B32006"
        })


    # empty string of fields_filter returns empty object
    def test_get_station_detail_with_empty_fields_filter(self):
        response = self.client.get('/apis/stations/3/', {'fields': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})


    # wrong fields of fields_filter are ignored (specifying only wrong fields filter is equal to specifying empty string)
    def test_get_station_detail_with_wrong_fields_filter(self):
        response = self.client.get('/apis/stations/3/', {'fields': 'wrong_field'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})


class StationListTests(APITestCase):
    fixtures = ['StationListTests/stations']

    IDS_AT_FIRST_PAGE = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    IDS_AT_SECOND_PAGE = [13, 14, 15, 16, 17, 19, 20, 21, 22, 23]

    def test_get_stations(self):
        response = self.client.get('/apis/stations/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 21)
        self.assertEqual(response.data['next'], 'http://testserver/apis/stations/?page=2')
        self.assertIsNone(response.data['previous'])

        results = response.data['results']
        self.assertEqual(len(results), 10)

        # check all fields for only first element
        self.assertEqual(results[0], {
            "station_id": 3,
            "short_name": "B32006",
            "name": "Colleges of the Fenway - Fenway at Avenue Louis Pasteur",
            "lat": 42.34011512249236,
            "lon": -71.10061883926392,
            "region": 'Boston',
            "capacity": 15,
            "electric_bike_surcharge_waiver": False,
            "eightd_has_key_dispenser": True,
            "has_kiosk": True
        })

        # check only ids for all elements
        self.assertEqual([s['station_id'] for s in results], self.IDS_AT_FIRST_PAGE)


    def test_get_stations_next_page(self):
        response = self.client.get('/apis/stations/?page=2', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 21)
        self.assertEqual(response.data['next'], 'http://testserver/apis/stations/?page=3')
        self.assertEqual(response.data['previous'], 'http://testserver/apis/stations/')

        results = response.data['results']
        self.assertEqual(len(results), 10)

        # check all fields for only first element
        self.assertEqual(results[0], {
            "station_id": 13,
            "short_name": "C32002",
            "name": "Boston Medical Center - E Concord St at Harrison Ave",
            "lat": 42.33671641210506,
            "lon": -71.06880776602338,
            "region": 'Boston',
            "capacity": 15,
            "electric_bike_surcharge_waiver": False,
            "eightd_has_key_dispenser": False,
            "has_kiosk": True
        })

        # check only ids for all elements
        self.assertEqual([s['station_id'] for s in results], self.IDS_AT_SECOND_PAGE)


    def test_get_stations_last_page(self):
        response = self.client.get('/apis/stations/?page=3', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 21)
        self.assertIsNone(response.data['next'])
        self.assertEqual(response.data['previous'], 'http://testserver/apis/stations/?page=2')

        results = response.data['results']
        self.assertEqual(len(results), 1)

        # check all fields for only first element
        self.assertEqual(results[0], {
            "station_id": 24,
            "short_name": "B32007",
            "name": "Seaport Square - Seaport Blvd at Northern Ave",
            "lat": 42.35148193460858,
            "lon": -71.04436084628105,
            "region": 'Boston',
            "capacity": 19,
            "electric_bike_surcharge_waiver": False,
            "eightd_has_key_dispenser": False,
            "has_kiosk": True
        })


    def test_get_stations_with_fields_filter(self):
        response = self.client.get('/apis/stations/', {'fields': 'station_id'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i], { "station_id": self.IDS_AT_FIRST_PAGE[i] })


    def test_get_stations_with_multiple_fields_filter(self):
        response = self.client.get('/apis/stations/', {'fields': 'station_id,short_name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i].keys(), ['station_id', 'short_name'])
    

    def test_get_stations_with_omit_filter(self):
        response = self.client.get('/apis/stations/', {'omit': 'station_id,short_name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i].keys(), ['name', 'lat', 'lon', 'region', 'capacity', 'electric_bike_surcharge_waiver', 'eightd_has_key_dispenser', 'has_kiosk'])

    
    # if one field is specified by 'fields' and 'omit', then it should be excluded
    def test_get_station_s_with_both_omit_and_fields_filter(self):
        response = self.client.get('/apis/stations/', {'fields': 'station_id,short_name', 'omit': 'station_id'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i].keys(), ['short_name'])            


    # empty string of fields_filter returns empty object
    def test_get_stations_with_empty_fields_filter(self):
        response = self.client.get('/apis/stations/', {'fields': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i], {})


    # wrong fields of fields_filter are ignored (specifying only wrong fields filter is equal to specifying empty string)
    def test_get_stations_with_wrong_fields_filter(self):
        response = self.client.get('/apis/stations/', {'fields': 'wrong_field'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i], {})


    def test_get_stations_simple_filter(self):
        response = self.client.get('/apis/stations/', {'eightd_has_key_dispenser': 'false'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 14)
        self.assertEqual(response.data['next'], 'http://testserver/apis/stations/?eightd_has_key_dispenser=false&page=2')
        self.assertIsNone(response.data['previous'])

        results = response.data['results']
        self.assertEqual(len(results), 10)

        # check all fields for only first element
        self.assertEqual(results[0], {
            "station_id": 4,
            "short_name": "C32000",
            "name": "Tremont St at E Berkeley St",
            "lat": 42.345392,
            "lon": -71.069616,
            "region": 'Boston',
            "capacity": 19,
            "electric_bike_surcharge_waiver": False,
            "eightd_has_key_dispenser": False,
            "has_kiosk": True
        })


    def test_get_stations_capacity_filter(self):
        response = self.client.get('/apis/stations/', {'capacity': 18}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)


    def test_get_stations_capacity_gt_filter(self):
        response = self.client.get('/apis/stations/', {'capacity_gt': 18}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 8)


    def test_get_stations_capacity_lt_filter(self):
        response = self.client.get('/apis/stations/', {'capacity_lt': 18}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
    

    def test_get_stations_filter_not_found(self):
        response = self.client.get('/apis/stations/', {'station_id': 0}, format='json') # not existing station id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])


    def test_get_stations_multiple_filters(self):
        response = self.client.get('/apis/stations/', {'capacity_gt': 15, 'eightd_has_key_dispenser': 'true'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

        results = response.data['results']
        self.assertEqual(len(results), 6)