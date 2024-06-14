from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializer import WeatherDataSerializer, RawDataSerializer, RawDataSimplifiedSerializer 
from .models import *
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Raw Data': '/weather/',
        'Analyzed Weather Data':'/weather/stat/',
        'Swagger Schema': '/schema/',
        'Swagger UI': '/schema/swagger-ui/',
        'Swagger Redoc': '/schema/redoc/',
        'Raw Data Slow UI/Fast Ingestion': '/weather/slow/'
    }
    return Response(api_urls)


class weatherRawData(viewsets.ModelViewSet):
    """
    Viewset for viewing, retrieving, and filtering the daily raw weather data. Faster UI with filtering for year and weather station name

    Daily weather data is organized as a nested list, as such: [[...],[date, max_temp, min_temp, precipitation],[...]]
    Temperature units are in .1 *C and total precipitation units are in .1 mm 
    """
    queryset = raw_weather_data.objects.all().order_by('weather_station_name')
    serializer_class = RawDataSerializer
    
    #Pagination handler. Page size of 1 was chosen so all of the raw data for a station could be seen on 1 page.
    pagination_class = PageNumberPagination
    pagination_class.page_size = 1
    
    #Filtering for raw data. There is only an option to filter one the weather station name
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'weather_station_name': ["exact"],
        'year': ['exact'],
    }


class weatherStats(viewsets.ModelViewSet):
    """
    Viewset for viewing, retrieving, and filtering the analyzed annual weather data.

    Temperature units are in *C and total precipitation units are in cm
    """
    queryset = analyzed_weather_data.objects.all()
    serializer_class = WeatherDataSerializer
    
    #Pagination handler. Page size of 30 was chosen so you could see each year of data for a station on 1 page.
    pagination_class_stats = PageNumberPagination
    pagination_class_stats.page_size = 30
    
    #Filtering fields
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'weather_station_name': ["exact"],
        'year': ["exact"]
    }


class weatherRawDataSimplified(viewsets.ModelViewSet):
    """
    Viewset for viewing, retrieving, and filtering the daily raw weather data. Ingestion is faster but UI is slower.

    Daily weather data is organized as a nested list, as such: [[...],[date, max_temp, min_temp, precipitation],[...]]
    Temperature units are in .1 *C and total precipitation units are in .1 mm 
    """
    queryset = raw_weather_data_simplified.objects.all().order_by('weather_station_name')
    serializer_class = RawDataSimplifiedSerializer 
    
    #Pagination handler. Page size of 1 was chosen so all of the raw data for a station could be seen on 1 page.
    pagination_class = PageNumberPagination
    
    #Filtering for raw data. There is only an option to filter one the weather station name
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'weather_station_name': ["exact"],
    }