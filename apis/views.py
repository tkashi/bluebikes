# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import FilterSet, NumberFilter, DateTimeFilter, DjangoFilterBackend
from .models import Station, Trip
from .serializers import StationSerializer, TripSerializer

# Create your views here.
class StationFilter(FilterSet):
    capacity_gt = NumberFilter(name='capacity', lookup_expr='gt')
    capacity_lt = NumberFilter(name='capacity', lookup_expr='lt')

    class Meta:
        model = Station
        fields = '__all__'

class StationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend,)
    filter_class = StationFilter
    ordering_fields = '__all__'
    search_fields = ('name')


class TripFilter(FilterSet):
    start_time_gt = DateTimeFilter(field_name='start_time', lookup_expr='gt')
    start_time_lt = DateTimeFilter(field_name='start_time', lookup_expr='lt')
    stop_time_gt = DateTimeFilter(field_name='stop_time', lookup_expr='gt')
    stop_time_lt = DateTimeFilter(field_name='stop_time', lookup_expr='lt')
    birth_year_gt = NumberFilter(name='birth_year', lookup_expr='gt')
    birth_year_lt = NumberFilter(name='birth_year', lookup_expr='lt')

    class Meta:
        model = Trip
        fields = '__all__'

class TripViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filter_class = TripFilter
