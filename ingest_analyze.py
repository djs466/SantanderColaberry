import os
import pandas as pd 
import datetime as dt
from api.models import *
import json
import numpy as np


def read_files(root_directory: str) -> None:
    """
    Fruitless function that adds new raw weather_data objects into the database from the files present in the root_directory provided.

    If a weather station's raw data is already present in the database then ingestion is skipped to prevent duplication. 
    Run-time and total records ingested is stored in the file './logs/ingestion_log.txt'
    
    Args:
        root_directory: a string that provides the path to the folder where all the whether data is present. Default is: '../wx_data/'
    """
    start_time = dt.datetime.now()
    no_of_records = 0
    weather_stations_in_db = raw_weather_data.objects.all().values_list('weather_station_name', flat='True')
    filenames = os.listdir(root_directory)
    for file in filenames:
        station_name = file[:-4]
        #1.) Check to see if there is already data for the weather station in the database.
        if station_name in weather_stations_in_db:
            pass
        else:
            #2.) If the data for this station does not exist in the database then read it from the txt file.
            daily_data = pd.read_csv(root_directory + file, delimiter = '\t', header = None)
            daily_data['year'] = daily_data[0].map(str).str[:4] # converts data values to string so that the year can be spliced.
            daily_data_years_list = [groups for df, groups in daily_data.groupby('year')] #Breaks up dataframe into seperate dataframes based on year.
            #It is significantly faster to not break up the dataframe by year and exclude the field from the raw_weather_data model, 
            #but this allows for filtering by year in the API.

            #3.) Load the dataframes to JSON objects and create new raw data objects in the database for it.
            for daily_data_df in daily_data_years_list:
                year = int(daily_data_df['year'].unique()[0])
                weather_data_json = json.loads(daily_data_df[[0,1,2,3]].to_json(orient='values'))

                new_raw_data_obj = raw_weather_data()
                new_raw_data_obj.weather_station_name = station_name
                new_raw_data_obj.year = year
                new_raw_data_obj.daily_weather_data = weather_data_json
                new_raw_data_obj.save()
            no_of_records += daily_data.shape[0]
    time_delta = dt.datetime.now() - start_time
    new_log_data = f'Method of ingestion: slow, Datetime: {start_time}, Number of records processed: {no_of_records}, Amount of time taken: {time_delta}\n'
    log_file = open('./logs/ingestion_log.txt', 'a')
    log_file.write(new_log_data)
    log_file.close()


def analysis() -> None:
    """
    Fruitless function that refreshes all of the analyzed_weather_data objects in the database by calculating
    their annual average maximum & minimum temperature (*C) and total yearly precipitation (cm).
    """
    weather_stations = raw_weather_data.objects.all() #Pulls all raw data seperated by name and year
    existing_stations = analyzed_weather_data.objects.all().delete() #Clear out existing data in the database, so it can rerun with creating duplicates
    
    for station in weather_stations:
        station_name = station.weather_station_name
        current_year = station.year
        #Pulls the raw data for a specific weather station and year from the database and loads it into a pandas DataFrame. 
        annual_data = pd.DataFrame(station.daily_weather_data, columns = ['Date','Max','Min','Precipitation'])
        annual_data.replace(-9999, None, inplace = True)
        
        #loop through all of the years present in the raw data, and calculate annual avg. temperatures and total precipitation.
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


if __name__ == '__main__':
    read_files('./wx_data')
    analysis()