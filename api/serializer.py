from rest_framework import serializers
from .models import analyzed_weather_data, raw_weather_data, raw_weather_data_simplified


class RawDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = raw_weather_data
        fields = ['weather_station_name', 'year', 'daily_weather_data']
        

class WeatherDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = analyzed_weather_data
        fields = ['weather_station_name', 'year', 'avg_max_temp', 'avg_min_temp', 'precipitation']


class RawDataSimplifiedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = raw_weather_data_simplified
        fields = ['weather_station_name', 'daily_weather_data']