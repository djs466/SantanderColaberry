import os
import pandas as pd 
import datetime as dt
from api.models import *
import json
import numpy as np

"""
This is the fastest way to ingest and analyze the data. Though the gain in speed is related to the fact that all the daily weather data is stored as 
one JSON without being broken up by year. This means raw weather data in the API can not be filtered by year, but ingestion speed and analysis are drastically reduced.
"""


def read_files(root_directory: str) -> None:
    """
    Fruitless function that adds new raw raw_weather_data_fastest objects into the database from the files present in the root_directory provided.

    If a weather station's raw data is already present in the database then ingestion is skipped to prevent duplication. 
    Run-time and total records ingested is stored in the file './logs/ingestion_log.txt'
    
    Args:
        root_directory: a string that provides the path to the folder where all the whether data is present. Default is: '../wx_data/'
    """
    start_time = dt.datetime.now()
    no_of_records = 0
    weather_stations_in_db = raw_weather_data_simplified.objects.all().values_list('weather_station_name', flat='True')
    filenames = os.listdir(root_directory)
    for file in filenames:
        station_name = file[:-4]
        #1.) Check to see if there is already data for the weather station in the database.
        if station_name in weather_stations_in_db:
            pass
        else:
            #2.) If the data for this station does not exist in the database then read it from the txt file.
            daily_data = pd.read_csv(root_directory + file, delimiter = '\t')
            #3.) Load the dataframe to a JSON object and create a new object in the database for it.
            weather_data_json = json.loads(daily_data.to_json(orient='values'))
            
            new_weather_station = raw_weather_data_simplified()
            new_weather_station.weather_station_name = station_name
            new_weather_station.daily_weather_data = weather_data_json
            new_weather_station.save()
            
            no_of_records += daily_data.shape[0]
    time_delta = dt.datetime.now() - start_time
    new_log_data = f'Method of ingestion: fast, Datetime: {start_time}, Number of records processed: {no_of_records}, Amount of time taken: {time_delta}\n'
    log_file = open('./logs/ingestion_log.txt', 'a')
    log_file.write(new_log_data)
    log_file.close()


def analysis() -> None:
    """
    Fruitless function that refreshes all of the analyzed_weather_data objects in the database by calculating
    their annual average maximum & minimum temperature (*C) and total yearly precipitation (cm).
    """
    weather_stations = raw_weather_data_simplified.objects.all() #Pulls all raw data and station names
    existing_stations = analyzed_weather_data.objects.all().delete() #Clear out existing data in the database, so it can rerun with creating duplicates
    
    analysis_output = {}
    for station in weather_stations:
        station_name = station.weather_station_name
        
        #Pulls the raw data for a specific weather station from the database and loads it into a pandas DataFrame. 
        df = pd.DataFrame(station.daily_weather_data, columns = ['Date','Max','Min','Precipitation'])
        df['Date'] = pd.to_datetime(df['Date'], format = '%Y%m%d')
        df.replace(-9999, None, inplace = True)
        
        #loop through all of the years present in the raw data, and calculate annual avg. temperatures and total precipitation.
        years_present = df['Date'].dt.year.unique()
        single_trial_output = {}
        for current_year in years_present:
            annual_data = df[df['Date'].dt.year == current_year]
            avg_max_temp_C = annual_data['Max'].mean() / 10 #Divide by 10 to put temperature in standard celsius units
            avg_min_temp_C = annual_data['Min'].mean() / 10 #Skip NA values is default behavior
            annual_precipitation = annual_data['Precipitation'].sum() / 100 #Divide by 100 to change units from tenths of mm to cm

            #Create new object in database with analyzed data
            new_analyzed_data = analyzed_weather_data(weather_station_name = station_name,
                                                      year = current_year,
                                                      avg_max_temp = round(avg_max_temp_C, 2),
                                                      avg_min_temp = round(avg_min_temp_C, 2),
                                                      precipitation = annual_precipitation,
            )
            new_analyzed_data.save()
        