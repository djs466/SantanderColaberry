from django.db import models

class raw_weather_data(models.Model):
    """
    This model stores objects that contain the raw data from the .txt files.

    JSON objects were used to store the year, max & min temp, & precipitation rather than individual model fields,
    because it was faster and required the creation of fewer objects.
    
    Attributes:
        weather_station_name: (str) The station name/id that is its unique identifier. i.e. USC00110072
        year: (int) the year of data collection. These values range from [1985-2014]
        daily_weather_data: (json) All of the data ingested from a single .txt file. 
            Organized as a nested list, as such: [[...],[date, max_temp, min_temp, precipitation],[...]]
    """
    weather_station_name = models.CharField(max_length=15, blank=False, unique=False, default=None)
    year = models.IntegerField()
    daily_weather_data = models.JSONField(default=None)


class analyzed_weather_data(models.Model):
    """
    This model stores the analyzed data produced for each weather station. Representing the calculated annual
    average max temp, min temp, and total precipitation

    Attributes:
        weather_station_name: (str) The station name/id that is its unique identifier. i.e. USC00110072
        year: (int) the year of data collection. These values range from [1985-2014]
        avg_max_temp: (float) The average annual maximum temperature in degrees Celsius.
        avg_min_temp: (float) The average annual minimum temperature in degrees Celsius.
        precipitation: (float) The total annual precipitation in cm.
    """
    weather_station_name = models.CharField(max_length=15, blank=False, unique=False, default=None)
    year = models.IntegerField()
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    precipitation = models.FloatField(null=True)

    def __str__(self):
        return self.weather_station_name
    

class raw_weather_data_simplified(models.Model):
    """
    This model stores objects that contain the raw data from the .txt files. It is the simpliest way to store the raw weather data
    by omitting the year field. Though the speed gained in ingestion, causes the API to work slower, as the JSON's are bigger, and 
    does not allow for filtering by year.

    JSON objects were used to store the year, max & min temp, & precipitation rather than individual model fields,
    because it was faster and required the creation of fewer objects.
    
    Attributes:
        weather_station_name: (str) The station name/id that is its unique identifier. i.e. USC00110072
        year: (int) the year of data collection. These values range from [1985-2014]
        daily_weather_data: (json) All of the data ingested from a single .txt file. 
            Organized as a nested list, as such: [[...],[date, max_temp, min_temp, precipitation],[...]]
    """
    weather_station_name = models.CharField(max_length=15, blank=False, unique=False, default=None)
    daily_weather_data = models.JSONField(default=None)
