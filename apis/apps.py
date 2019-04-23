# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import glob, csv, sys

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware


def make_aware_datetime(datetime):
    return make_aware(parse_datetime(datetime))

def import_data(sender, **kwargs):
    """
        Import trip history data from csv files.
    """

    from .models import Station, Trip

    print('-- importing Trip data --')

    files = glob.glob("./data/*.csv")
    count = 0
    for file in files:
        with open(file) as f:
            reader = csv.reader(f, doublequote=True, lineterminator='\r\n', quotechar=str('"'), skipinitialspace=True)
            header = next(reader)
            for row in reader:                
                # print(row)
                trip = Trip(duration=int(row[0]), start_time=make_aware_datetime(row[1]), stop_time=make_aware_datetime(row[2]), bike_id=row[11], is_subscriber=row[12]=='Subscriber', birth_year=int(row[13]), gender=int(row[14]))
                try:
                    trip.start_station=Station.objects.get(pk=row[3])
                except:
                    trip.start_station_id = int(row[3])
                try:
                    trip.stop_station=Station.objects.get(pk=row[7])
                except:
                    trip.stop_station_id = int(row[7])

                trip.save()

                count += 1

    print('Loaded {} trips'.format(count))

class ApisConfig(AppConfig):
    name = 'apis'

    def ready(self):
        # import trip data if it is not for a test
        if 'test' not in sys.argv:  
            post_migrate.connect(import_data, sender=self)
