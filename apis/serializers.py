from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin
from .models import Station, Trip

class StationSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    region = serializers.StringRelatedField(many=False)

    class Meta:
        model = Station
        fields = ('station_id', 'short_name', 'name', 'lat', 'lon', 'region', 'capacity', 'electric_bike_surcharge_waiver', 'eightd_has_key_dispenser', 'has_kiosk')


class TripSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    start_station = StationSerializer(many=False)
    stop_station = StationSerializer(many=False)

    class Meta:
        model = Trip
        fields = '__all__' 

