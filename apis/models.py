# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Region(models.Model):
    region_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class RentalMethod(models.Model):
    method = models.CharField(max_length=10)

    def __str__(self):
        return self.method

class Station(models.Model):
    """
    The class for station

    Attributes
    ----------
    station_id : int
        the unique identified of the station
    short_name : str
        the short name of the station
    name : str
        the name of the station
    lat : double
        the latitude of the location of the station
    lon : double
        the longitude of the location of the station
    region: Region
        the region of the station
    capacity : int
        the capacity of bikes at the station
    electric_bike_surcharge_waiver:  boolean
        whether the electric bike surcharge can be waivered
    eightd_has_key_dispenser: boolean
        whether the station has key dispenser
    has_kiosk: boolean
        whether there is a kiosk at the station
    """

    station_id = models.IntegerField(primary_key=True)
    short_name = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    region =  models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)
    capacity = models.IntegerField()
    electric_bike_surcharge_waiver = models.BooleanField()
    eightd_has_key_dispenser = models.BooleanField()
    has_kiosk = models.BooleanField()
    rental_methods = models.ManyToManyField(RentalMethod)

    def __str__(self):
        return self.name


class Trip(models.Model):
    """
    The class for trip

    Attributes
    ----------
    duration : int
        the duration of the trip
    start_time : ISODatetime
        the date time to start the trip
    stop_time : ISODatetime
        the date time to stop the trip
    start_time : ISODate
        the date to start the trip
    stop_time : ISODate
        the date to stop the trip
    start_station: Station
        the station to start the trip
    stop_station: Station
        the station to stop the trip
    bike_id : int
        the unique identifer of the bike used for the trip
    is_subscriber:  boolean
        whether the user has subscriber or not
    birth_year: int
        the user's birth year
    gender: int
        the user's gender (0 = unknown, 1 = man, 2 = woman)
    """
    
    duration = models.IntegerField()
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    start_date = models.DateField()
    stop_date = models.DateField()
    start_station = models.ForeignKey(Station, on_delete=models.DO_NOTHING, related_name='start_station_id')
    stop_station = models.ForeignKey(Station, on_delete=models.DO_NOTHING, related_name='stop_station_id')
    bike_id = models.IntegerField()
    is_subscriber = models.BooleanField()
    birth_year = models.IntegerField(null=True)
    gender = models.IntegerField()

    def save(self, *args, **kwargs):
        """
            Create a trip. Calcurate date from datetime fields
        """
        self.start_date = self.start_time.date()
        self.stop_date = self.stop_time.date()
        return super(Trip, self).save(*args, **kwargs)

    