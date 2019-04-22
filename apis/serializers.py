from rest_framework import serializers
from .models import Station, Trip

class FieldsFilterMixin(object):

    @property
    def fields(self):
        existing_fields = super(FieldsFilterMixin, self).fields

        if 'request' not in self.context:
            return existing_fields

        query_params = self.context['request'].query_params

        fields = query_params.get('fields')
        includes = set(existing_fields.keys()) if not fields else set(fields.split(','))
            
        excludes = query_params.get('fields_exclude')
        if excludes:
            includes -= set(excludes.split(','))
        
        for field_name in set(existing_fields.keys()) - includes:
            del existing_fields[field_name]

        return existing_fields


class StationSerializer(FieldsFilterMixin, serializers.ModelSerializer):
    region = serializers.StringRelatedField(many=False)

    class Meta:
        model = Station
        fields = ('station_id', 'short_name', 'name', 'lat', 'lon', 'region', 'capacity', 'electric_bike_surcharge_waiver', 'eightd_has_key_dispenser', 'has_kiosk')


class TripSerializer(FieldsFilterMixin, serializers.ModelSerializer):
    start_station = StationSerializer(many=False)
    stop_station = StationSerializer(many=False)

    class Meta:
        model = Trip
        fields = '__all__' 

class TripSummarySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    max = serializers.IntegerField()
    min = serializers.IntegerField()
    avg = serializers.IntegerField()
    sum = serializers.IntegerField()

    @property
    def fields(self):
        existing_fields = super(TripSummarySerializer, self).fields

        if 'request' not in self.context:
            return existing_fields

        query_params = self.context['request'].query_params
        group_by = str(query_params.get('group_by'))

        aggs = query_params.get('agg', 'count').split(',');

        fields = {agg: existing_fields[agg] for agg in aggs}
                    
        fields['group_by'] = existing_fields[group_by]

        return fields

    # def to_representation(self, obj):
    #     return { key: 10 if key == 'count' else obj[key] for key in self.fields }

    class Meta:
        model = Trip
        fields = '__all__'

