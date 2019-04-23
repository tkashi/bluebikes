# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

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


class TripDetailTests(APITestCase):
    fixtures = ['TripDetailTests/stations', 'TripDetailTests/trips']

    def test_get_trip_detail(self):
        response = self.client.get('/apis/trips/314/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": 314,
            "start_station": {
                "station_id": 3,
                "short_name": "B32006",
                "name": "Colleges of the Fenway - Fenway at Avenue Louis Pasteur",
                "lat": 42.34011512249236,
                "lon": -71.10061883926392,
                "region": "Boston",
                "capacity": 15,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": True,
                "has_kiosk": True
            },
            "stop_station": {
                "station_id": 14,
                "short_name": "B32003",
                "name": "HMS/HSPH - Avenue Louis Pasteur at Longwood Ave",
                "lat": 42.3374174845973,
                "lon": -71.10286116600037,
                "region": "Boston",
                "capacity": 21,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": False,
                "has_kiosk": True
            },
            "duration": 93,
            "start_time": "2019-03-01T07:58:21.278000-05:00",
            "stop_time": "2019-03-01T07:59:54.886000-05:00",
            "start_date": "2019-03-01",
            "stop_date": "2019-03-01",
            "bike_id": 2885,
            "is_subscriber": True,
            "birth_year": 1986,
            "gender": 1
        })
    

    def test_get_station_detail_region(self):
        response = self.client.get('/apis/trips/182/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["start_station"], {
                "station_id": 4,
                "short_name": "C32000",
                "name": "Tremont St at E Berkeley St",
                "lat": 42.345392,
                "lon": -71.069616,
                "region": "Boston",
                "capacity": 19,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": False,
                "has_kiosk": True
            })
        self.assertEqual(response.data["stop_station"], {
                "station_id": 6,
                "short_name": "D32000",
                "name": "Cambridge St at Joy St",
                "lat": 42.36121165307985,
                "lon": -71.06530619789737,
                "region": "Boston",
                "capacity": 15,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": False,
                "has_kiosk": True
            })
    

    def test_get_trip_detail_not_found(self):
        response = self.client.get('/trips/100/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_trip_detail_with_fields_filter(self):
        response = self.client.get('/apis/trips/182/', {'fields': 'id'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { "id": 182 })


    def test_get_trip_detail_with_station_fields_filter(self):
        response = self.client.get('/apis/trips/182/', {'fields': 'start_station'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'start_station': {
                "station_id": 4,
                "short_name": "C32000",
                "name": "Tremont St at E Berkeley St",
                "lat": 42.345392,
                "lon": -71.069616,
                "region": "Boston",
                "capacity": 19,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": False,
                "has_kiosk": True
            }
        })


    def test_get_trip_detail_with_multiple_fields_filter(self):
        response = self.client.get('/apis/trips/182/', {'fields': 'id,duration'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { "id": 182, 'duration': 996 })


    def test_get_trip_detail_with_omit_filter(self):
        response = self.client.get('/apis/trips/314/', {'omit': 'id,duration'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "start_station": {
                "station_id": 3,
                "short_name": "B32006",
                "name": "Colleges of the Fenway - Fenway at Avenue Louis Pasteur",
                "lat": 42.34011512249236,
                "lon": -71.10061883926392,
                "region": "Boston",
                "capacity": 15,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": True,
                "has_kiosk": True
            },
            "stop_station": {
                "station_id": 14,
                "short_name": "B32003",
                "name": "HMS/HSPH - Avenue Louis Pasteur at Longwood Ave",
                "lat": 42.3374174845973,
                "lon": -71.10286116600037,
                "region": "Boston",
                "capacity": 21,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": False,
                "has_kiosk": True
            },
            "start_time": "2019-03-01T07:58:21.278000-05:00",
            "stop_time": "2019-03-01T07:59:54.886000-05:00",
            "start_date": "2019-03-01",
            "stop_date": "2019-03-01",
            "bike_id": 2885,
            "is_subscriber": True,
            "birth_year": 1986,
            "gender": 1
        })

    
    # if one field is specified by 'fields' and 'omit', then it should be excluded
    def test_get_trip_detail_with_both_omit_and_fields_filter(self):
        response = self.client.get('/apis/trips/314/', {'fields': 'id,duration', 'omit': 'id'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, { 
            'duration': 93
        })


    # empty string of fields_filter returns empty object
    def test_get_trip_detail_with_empty_fields_filter(self):
        response = self.client.get('/apis/trips/314/', {'fields': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})


    # wrong fields of fields_filter are ignored (specifying only wrong fields filter is equal to specifying empty string)
    def test_get_trip_detail_with_wrong_fields_filter(self):
        response = self.client.get('/apis/trips/314/', {'fields': 'wrong_field'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})


class TripListTests(APITestCase):
    fixtures = ['TripListTests/stations', 'TripListTests/trips']

    IDS_AT_FIRST_PAGE = [175, 522, 575, 787, 931, 1582, 1602, 1950, 2186, 3255]
    IDS_AT_SECOND_PAGE = [3940, 4377, 4378, 4688, 4690, 5303, 5304, 6938, 7394, 7770]

    def test_get_trips(self):
        response = self.client.get('/apis/trips/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 21)
        self.assertEqual(response.data['next'], 'http://testserver/apis/trips/?page=2')
        self.assertIsNone(response.data['previous'])

        results = response.data['results']
        self.assertEqual(len(results), 10)

        # check all fields for only first element
        self.assertEqual(results[0], {
            "id": 175,
			"start_station": {
                "station_id": 190,
                "short_name": "A32025",
                "name": "Nashua Street at Red Auerbach Way",
                "lat": 42.365673,
                "lon": -71.064263,
                "region": 'Boston',
                "capacity": 37,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": True,
                "has_kiosk": True
            },
			"stop_station": {
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
            },
			"duration": 1171,
			"start_time": "2019-03-01T07:22:57.543000-05:00",
			"stop_time": "2019-03-01T07:42:29.141000-05:00",
			"start_date": "2019-03-01",
			"stop_date": "2019-03-01",
			"bike_id": 3571,
			"is_subscriber": True,
			"birth_year": 1984,
			"gender": 1
        })

        # check only ids for all elements
        self.assertEqual([t['id'] for t in results], self.IDS_AT_FIRST_PAGE)


    def test_get_trips_next_page(self):
        response = self.client.get('/apis/trips/?page=2', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 21)
        self.assertEqual(response.data['next'], 'http://testserver/apis/trips/?page=3')
        self.assertEqual(response.data['previous'], 'http://testserver/apis/trips/')

        results = response.data['results']
        self.assertEqual(len(results), 10)

        # check all fields for only first element
        self.assertEqual(results[0], {
            "id": 3940,
			"start_station": {
                "station_id": 14,
                "short_name": "B32003",
                "name": "HMS/HSPH - Avenue Louis Pasteur at Longwood Ave",
                "lat": 42.3374174845973,
                "lon": -71.10286116600037,
                "region": 'Boston',
                "capacity": 21,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": False,
                "has_kiosk": True
            },
			"stop_station": {
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
            },
			"duration": 105,
			"start_time": "2019-03-02T21:30:19.229000-05:00",
			"stop_time": "2019-03-02T21:32:04.951000-05:00",
			"start_date": "2019-03-02",
			"stop_date": "2019-03-02",
			"bike_id": 2644,
			"is_subscriber": True,
			"birth_year": 1986,
			"gender": 1
        })

        # check only ids for all elements
        self.assertEqual([t['id'] for t in results], self.IDS_AT_SECOND_PAGE)


    def test_get_trips_last_page(self):
        response = self.client.get('/apis/trips/?page=3', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 21)
        self.assertIsNone(response.data['next'])
        self.assertEqual(response.data['previous'], 'http://testserver/apis/trips/?page=2')

        results = response.data['results']
        self.assertEqual(len(results), 1)

        # check all fields for only first element
        self.assertEqual(results[0], {
            "id": 7983,
			"start_station": {
			    "station_id": 12,
                "short_name": "B32002",
                "name": "Ruggles T Stop - Columbus Ave at Melnea Cass Blvd",
                "lat": 42.33624444796878,
                "lon": -71.08798563480377,
                "region": 'Boston',
                "capacity": 18,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": True,
                "has_kiosk": True
            },
			"stop_station": {
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
            },
			"duration": 348,
			"start_time": "2019-03-05T10:18:50.611000-05:00",
			"stop_time": "2019-03-05T10:24:39.046000-05:00",
			"start_date": "2019-03-05",
			"stop_date": "2019-03-05",
			"bike_id": 2678,
			"is_subscriber": True,
			"birth_year": 1993,
			"gender": 1
        })


    def test_get_trips_with_fields_filter(self):
        response = self.client.get('/apis/trips/', {'fields': 'id'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i], { "id": self.IDS_AT_FIRST_PAGE[i] })


    def test_get_trips_with_multiple_fields_filter(self):
        response = self.client.get('/apis/trips/', {'fields': 'id,duration'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i].keys(), ['id', 'duration'])
    

    def test_get_trips_with_omit_filter(self):
        response = self.client.get('/apis/trips/', {'omit': 'id,duration'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i].keys(), ['start_station', 'stop_station', 'start_time', 'stop_time', 'start_date', 'stop_date', 'bike_id', 'is_subscriber', 'birth_year', 'gender'])

    
    # if one field is specified by 'fields' and 'omit', then it should be excluded
    def test_get_station_s_with_both_omit_and_fields_filter(self):
        response = self.client.get('/apis/trips/', {'fields': 'id,duration', 'omit': 'id'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i].keys(), ['duration'])            


    # empty string of fields_filter returns empty object
    def test_get_trips_with_empty_fields_filter(self):
        response = self.client.get('/apis/trips/', {'fields': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i], {})


    # wrong fields of fields_filter are ignored (specifying only wrong fields filter is equal to specifying empty string)
    def test_get_trips_with_wrong_fields_filter(self):
        response = self.client.get('/apis/trips/', {'fields': 'wrong_field'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        for i in range(len(results)):
            self.assertEqual(results[i], {})


    def test_get_trips_simple_filter(self):
        response = self.client.get('/apis/trips/', {'is_subscriber': 'true'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 15)
        self.assertEqual(response.data['next'], 'http://testserver/apis/trips/?is_subscriber=true&page=2')
        self.assertIsNone(response.data['previous'])

        results = response.data['results']
        self.assertEqual(len(results), 10)

        # check all fields for only first element
        self.assertEqual(results[0], {
            "id": 175,
			"start_station": {
                "station_id": 190,
                "short_name": "A32025",
                "name": "Nashua Street at Red Auerbach Way",
                "lat": 42.365673,
                "lon": -71.064263,
                "region": 'Boston',
                "capacity": 37,
                "electric_bike_surcharge_waiver": False,
                "eightd_has_key_dispenser": True,
                "has_kiosk": True
            },
			"stop_station": {
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
            },
			"duration": 1171,
			"start_time": "2019-03-01T07:22:57.543000-05:00",
			"stop_time": "2019-03-01T07:42:29.141000-05:00",
			"start_date": "2019-03-01",
			"stop_date": "2019-03-01",
			"bike_id": 3571,
			"is_subscriber": True,
			"birth_year": 1984,
			"gender": 1
        })


    def test_get_trips_start_date_filter(self):
        response = self.client.get('/apis/trips/', {'start_date': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


    # gt doesn't include strict same date
    def test_get_trips_start_date_gt_filter(self):
        response = self.client.get('/apis/trips/', {'start_date_gt': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    # lt doesn't include strict same date
    def test_get_trips_start_date_lt_filter(self):
        response = self.client.get('/apis/trips/', {'start_date_lt': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 17)
    

    def test_get_trips_stop_date_filter(self):
        response = self.client.get('/apis/trips/', {'stop_date': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


    # gt doesn't include strict same date
    def test_get_trips_stop_date_gt_filter(self):
        response = self.client.get('/apis/trips/', {'stop_date_gt': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    # lt doesn't include strict same date
    def test_get_trips_stop_date_lt_filter(self):
        response = self.client.get('/apis/trips/', {'stop_date_lt': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 17)
      

    def test_get_trips_birth_year_filter(self):
        response = self.client.get('/apis/trips/', {'birth_year': 1990}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)


    # gt doesn't include strict same year
    def test_get_trips_birth_year_gt_filter(self):
        response = self.client.get('/apis/trips/', {'birth_year_gt': 1990}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 12)

    # lt doesn't include strict same year
    def test_get_trips_birth_year_lt_filter(self):
        response = self.client.get('/apis/trips/', {'birth_year_lt': 1990}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 7)
    

    def test_get_trips_duration_filter(self):
        response = self.client.get('/apis/trips/', {'duration': 449}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


    # gt doesn't include strict same date
    def test_get_trips_duration_gt_filter(self):
        response = self.client.get('/apis/trips/', {'duration_gt': 449}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 17)

    # lt doesn't include strict same date
    def test_get_trips_duration_lt_filter(self):
        response = self.client.get('/apis/trips/', {'duration_lt': 449}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)


    def test_get_trips_start_time_gt_filter(self):
        response = self.client.get('/apis/trips/', {'start_time_gt': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)


    def test_get_trips_start_time_lt_filter(self):
        response = self.client.get('/apis/trips/', {'start_time_lt': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 17)
    

    def test_get_trips_stop_time_gt_filter(self):
        response = self.client.get('/apis/trips/', {'stop_time_gt': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)


    def test_get_trips_stop_time_lt_filter(self):
        response = self.client.get('/apis/trips/', {'stop_time_lt': '2019-03-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 17)


    def test_get_trips_filter_not_found(self):
        response = self.client.get('/apis/trips/', {'duration': 0}, format='json') # not existing station id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)


    def test_get_trips_multiple_filters(self):
        response = self.client.get('/apis/trips/', {'start_date_gt': '2019-03-04', 'birth_year_gt': 1990}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)


class TripSummaryTests(APITestCase):
    fixtures = ['TripSummaryTests/stations', 'TripSummaryTests/trips']

    def test_get_trip_summary_count(self):
        response = self.client.get('/apis/trips/summary/', {'group_by': 'start_date', 'agg': 'count'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'start_date': datetime.date(2019, 3, 1),
            'count': 9
        }, {
            'start_date': datetime.date(2019, 3, 2),
            'count': 2
        }, {
            'start_date': datetime.date(2019, 3, 3),
            'count': 6
        }, {
            'start_date': datetime.date(2019, 3, 4),
            'count': 1
        }, {
            'start_date': datetime.date(2019, 3, 5),
            'count': 3
        }])


    # agg's default is count
    def test_get_trip_summary_not_specify_agg(self):
        response = self.client.get('/apis/trips/summary/', {'group_by': 'start_date'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'start_date': datetime.date(2019, 3, 1),
            'count': 9
        }, {
            'start_date': datetime.date(2019, 3, 2),
            'count': 2
        }, {
            'start_date': datetime.date(2019, 3, 3),
            'count': 6
        }, {
            'start_date': datetime.date(2019, 3, 4),
            'count': 1
        }, {
            'start_date': datetime.date(2019, 3, 5),
            'count': 3
        }])
    
    def test_get_trip_summary_max(self):
        response = self.client.get('/apis/trips/summary/', {
            'group_by': 'start_date', 
            'agg': 'max', 
            'field': 'duration'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'start_date': datetime.date(2019, 3, 1),
            'max_duration': 1674
        }, {
            'start_date': datetime.date(2019, 3, 2),
            'max_duration': 316
        }, {
            'start_date': datetime.date(2019, 3, 3),
            'max_duration': 4151
        }, {
            'start_date': datetime.date(2019, 3, 4),
            'max_duration': 1092
        }, {
            'start_date': datetime.date(2019, 3, 5),
            'max_duration': 1381
        }])


    def test_get_trip_summary_ave(self):
        response = self.client.get('/apis/trips/summary/', {
            'group_by': 'start_date', 
            'agg': 'avg', 
            'field': 'duration'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'start_date': datetime.date(2019, 3, 1),
            'avg_duration': 1086.4444444444443,
        }, {
            'start_date': datetime.date(2019, 3, 2),
            'avg_duration': 210.5
        }, {
            'start_date': datetime.date(2019, 3, 3),
            'avg_duration': 2004.1666666666667
        }, {
            'start_date': datetime.date(2019, 3, 4),
            'avg_duration': 1092
        }, {
            'start_date': datetime.date(2019, 3, 5),
            'avg_duration': 784
        }])


    def test_get_trip_summary_min(self):
        response = self.client.get('/apis/trips/summary/', {
            'group_by': 'start_date', 
            'agg': 'min', 
            'field': 'duration'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'start_date': datetime.date(2019, 3, 1),
            'min_duration': 639
        }, {
            'start_date': datetime.date(2019, 3, 2),
            'min_duration': 105
        }, {
            'start_date': datetime.date(2019, 3, 3),
            'min_duration': 449
        }, {
            'start_date': datetime.date(2019, 3, 4),
            'min_duration': 1092
        }, {
            'start_date': datetime.date(2019, 3, 5),
            'min_duration': 348
        }])

            
    def test_get_trip_summary_sum(self):
        response = self.client.get('/apis/trips/summary/', {
            'group_by': 'start_date', 
            'agg': 'sum', 
            'field': 'duration'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'start_date': datetime.date(2019, 3, 1),
            'sum_duration': 9778
        }, {
            'start_date': datetime.date(2019, 3, 2),
            'sum_duration': 421
        }, {
            'start_date': datetime.date(2019, 3, 3),
            'sum_duration': 12025
        }, {
            'start_date': datetime.date(2019, 3, 4),
            'sum_duration': 1092
        }, {
            'start_date': datetime.date(2019, 3, 5),
            'sum_duration': 2352
        }])
    

    def test_get_trip_summary_multiple_agg(self):
        response = self.client.get('/apis/trips/summary/', {
            'group_by': 'start_date', 
            'agg': 'sum,count', 
            'field': 'duration'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'start_date': datetime.date(2019, 3, 1),
            'sum_duration': 9778,
            'count': 9
        }, {
            'start_date': datetime.date(2019, 3, 2),
            'sum_duration': 421,
            'count': 2
        }, {
            'start_date': datetime.date(2019, 3, 3),
            'sum_duration': 12025,
            'count': 6
        }, {
            'start_date': datetime.date(2019, 3, 4),
            'sum_duration': 1092,
            'count': 1
        }, {
            'start_date': datetime.date(2019, 3, 5),
            'sum_duration': 2352,
            'count': 3
        }])

    
    def test_get_trip_summary_missing_group_by(self):
         response = self.client.get('/apis/trips/summary/', format='json')
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_trip_summary_missing_field(self):
         response = self.client.get('/apis/trips/summary/', {
             'group_by': 'start_date',
             'agg': 'max'
         }, format='json')
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)