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
    duration = models.IntegerField()
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    start_station = models.ForeignKey(Station, on_delete=models.DO_NOTHING, related_name='start_station_id')
    stop_station = models.ForeignKey(Station, on_delete=models.DO_NOTHING, related_name='stop_station_id')
    bike_id = models.IntegerField()
    is_subscriber = models.BooleanField()
    birth_year = models.IntegerField(null=True)
    gender = models.IntegerField()
    