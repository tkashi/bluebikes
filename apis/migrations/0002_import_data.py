# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

import sys, urllib, json

from django.db import migrations, models
import django.db.models.deletion


def encode_utf8(data, ignore_dicts = False):
    if isinstance(data, unicode):
        return data.encode('utf-8')

    if isinstance(data, list):
        return [ encode_utf8(item, ignore_dicts=True) for item in data ]

    if isinstance(data, dict) and not ignore_dicts:
        return {
            key.encode('utf-8'): encode_utf8(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }

    return data

def import_data(*args):
    from apis.models import Station, Region

    # regions
    print('-- importing region data --')
    response = urllib.urlopen('https://gbfs.bluebikes.com/gbfs/en/system_regions.json')
    data = json.loads(response.read(), object_hook=encode_utf8)
    for r in data['data']['regions']:
        Region(**r).save()

    if 'test' not in sys.argv:    
        print('-- importing station data --')
        # stations
        response = urllib.urlopen('https://gbfs.bluebikes.com/gbfs/en/station_information.json')
        data = json.loads(response.read(), object_hook=encode_utf8)

        for s in data['data']['stations']:
            station = Station(station_id=s['station_id'], short_name=s['short_name'], name=s['name'], lat=s['lat'], lon=s['lon'], capacity=s['capacity'], electric_bike_surcharge_waiver=s['electric_bike_surcharge_waiver'], eightd_has_key_dispenser=s['eightd_has_key_dispenser'], has_kiosk=s['has_kiosk'])

            if 'region_id' in s:
                station.region_id = s['region_id']

            station.save()

class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_data),
    ]