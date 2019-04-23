# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Count, Max, Min, Sum, Avg

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import APIException
from django_filters.rest_framework import FilterSet, NumberFilter, DateFilter, DateTimeFilter, DjangoFilterBackend
from .models import Station, Trip
from .serializers import StationSerializer, TripSerializer, TripSummarySerializer

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
    start_date_gt = DateFilter(field_name='start_date', lookup_expr='gt')
    start_date_lt = DateFilter(field_name='start_date', lookup_expr='lt')
    stop_date_gt = DateFilter(field_name='stop_date', lookup_expr='gt')
    stop_date_lt = DateFilter(field_name='stop_date', lookup_expr='lt')
    birth_year_gt = NumberFilter(name='birth_year', lookup_expr='gt')
    birth_year_lt = NumberFilter(name='birth_year', lookup_expr='lt')
    duration_gt = NumberFilter(name='duration', lookup_expr='gt')
    duration_lt = NumberFilter(name='duration', lookup_expr='lt')

    class Meta:
        model = Trip
        fields = '__all__'

class TripViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filter_class = TripFilter

ANNODATIONS_DEFS = {
    'max' : Max,
    'min' : Min,
    'avg' : Avg,
    'sum' : Sum,
}

class TripSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    filter_class = TripFilter
    queryset = Trip.objects.all()
    serializer_class = TripSummarySerializer
    pagination_class=None

    def _raiseException(self, field):
        e = APIException("The request parameter '{}' is required.".format(field))
        e.status_code = 400
        raise e

    def get_queryset(self):
        query_params = self.request.query_params
        group_by = query_params.get('group_by')

        if group_by is None:
            self._raiseException('group_by')

        field = query_params.get('field')
        aggs = query_params.get('agg', 'count')
        
        annotations = {}

        for agg in aggs.split(','):
            if agg == 'count':
                annotations[agg] = Count('pk')
            else:
                if field is None:
                    self._raiseException('field')
                
                annotations[agg + '_' + str(field)] = ANNODATIONS_DEFS[agg](field)
        
        return self.queryset.values(str(group_by)).annotate(**annotations)