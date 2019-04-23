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

class TripSummarySerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        """
        Initialize TripSummarySerializer. 
        Generate fields depending on the request parameters 'agg' and 'field' so that the field names have both agg and field like 'max_duration'.
        """

        # Instantiate the superclass normally
        super(TripSummarySerializer, self).__init__(*args, **kwargs)

        if 'request' not in self.context:
            return

        query_params = self.context['request'].query_params
        group_by = str(query_params.get('group_by'))
        field = str(query_params.get('field'))
    
        aggs = query_params.get('agg', 'count').split(','); # multiple aggs can be specified by connecting comma (,)

        for key in self.fields.keys():
            if key != group_by:
                self.fields.pop(key) # remove all fields except group_by field
            
        for agg in aggs:
            name = agg
            if agg != 'count':
                name += '_' + field # concat aggregation function name and field to summarize

            self.fields[name] = serializers.IntegerField() # add aggregation field

    class Meta:
        fields = '__all__'

