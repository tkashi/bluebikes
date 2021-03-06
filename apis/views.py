# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Count, Max, Min, Sum, Avg

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from django_filters.rest_framework import FilterSet, NumberFilter, DateFilter, DateTimeFilter, CharFilter, DjangoFilterBackend
from .models import Station, Trip
from .serializers import StationSerializer, TripSerializer

# Create your views here.
class StationFilter(FilterSet):
    """
    The filter class for stations

    Attributes
    ----------
    capacity_gt: int
        capacity filter to get stations whose capacity is greater than this value

    capacity_lt: int
        capacity filter to get stations whose capacity is less than this value

    """
    capacity_gt = NumberFilter(name='capacity', lookup_expr='gt')
    capacity_lt = NumberFilter(name='capacity', lookup_expr='lt')

    name = CharFilter(name='name', lookup_expr='contains')

    class Meta:
        model = Station
        fields = '__all__'

class StationViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    The viewset class for stations

    retrieve:
    Return the given station.

    list:
    Return a list of all the stations.

    update: 
    Update the station.

    create:
    Create a new station.

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

    region: int
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

    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filter_class = StationFilter
    ordering_fields = '__all__'


class TripFilter(FilterSet):
    """
    The filter class for trips

    """
    
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


ANNODATIONS_DEFS = {
    'max' : Max,
    'min' : Min,
    'avg' : Avg,
    'sum' : Sum,
}


class TripViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given trip.

    list:
    Return a list of all the trips.

    summary:
    Return summary information of trips
    """
    
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filter_class = TripFilter

    def _raiseException(self, field):
        """
        Raise 400 exceptions for invalid or missing parameters
        """
        e = APIException("The request parameter '{}' is required.".format(field))
        e.status_code = 400
        raise e
        

    @action(detail=False, methods=['get'])
    def summary(self, request, *args, **kwargs):
        """
        Return a summary of trip history using specified aggregate functions and field. The summaries are grouped by the field specified by 'group_by'.

        Query Parameters
        ----------
        group_by (required): str

            a field name of Trip to be grouped

        agg: str

            aggregation function names (count, max, min, avg or sum). Specify multiple names with comma (,). Default is 'coubt'

        field: str

            a field name of Trip to summarize

        Examples
        -----------
        http://127.0.0.1:8000/apis/trips/summary/?group_by=gender

            Get number of records grouped by gender field

        http://127.0.0.1:8000/apis/trips/summary/?group_by=gender&agg=max&field=duration

            Get maximum duration for each gender

        http://127.0.0.1:8000/apis/trips/summary/?group_by=gender&agg=max,min&field=duration

            Get maximum and minimum duration for each gender

        Returns
        ----------
        The fields of response depends on how you specify 'group_by', 'field', 'agg' request parameters.
        """
        
        query_params = request.query_params
        group_by = query_params.get('group_by')

        if group_by is None:
            self._raiseException('group_by') # group_by is required. So raise exception when not specified.

        field = query_params.get('field')
        aggs = query_params.get('agg', 'count') # default is count
        
        annotations = {}

        for agg in aggs.split(','):
            if agg == 'count':
                annotations[agg] = Count('pk')
            else:
                if field is None:
                    # field is required for max, min, ave, and sum
                    self._raiseException('field')
                
                annotations[agg + '_' + str(field)] = ANNODATIONS_DEFS[agg](field)
        
        queryset = self.filter_queryset(self.queryset)
        return Response([e for e in queryset.values(str(group_by)).annotate(**annotations).iterator()])
