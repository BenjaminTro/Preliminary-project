# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 13:47:40 2023

@author: oscar
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_csv_data(file_path):
    csv_data = pd.read_csv(file_path, parse_dates=[0], dtype=float)
    csv_data.set_index(csv_data.columns[0], inplace=True)
    return csv_data

def read_irr_data(file_path):  
    irr_data = pd.read_csv(file_path, parse_dates=['time'], index_col='time', dtype=float)  
    #irr_data.index = irr_data.index.str[:-5]
    irr_data.index = pd.to_datetime(irr_data.index, format='%Y%m%d')
    irr_data['hours'] = irr_data.groupby(irr_data.index.date).cumcount()
    irr_data.index = irr_data.index + pd.to_timedelta(irr_data['hours'], unit='h')
    irr_data.drop(columns='hours', inplace=True)
    return irr_data

def read_excel_data(filename):
    df=pd.read_excel(filename, header=[2])
    return df

def read_specific_dates(filename, date_1, date_2):
    df=read_csv_data(filename)
    df=df[date_1 : date_2]
    return df

def dataframe_to_dict(df):
    result = [df[col_name].to_dict() for col_name in df.columns]
    return result

def convert_to_dict(dataframe, date_1, date_2, timeresolution, value_columns=None):
    date_1 = pd.to_datetime(date_1)
    date_2 = pd.to_datetime(date_2)
    df_2 = dataframe[date_1:date_2]

    # Resample the DataFrame based on the selected time resolution and apply sum aggregation
    if timeresolution == 'H':
        resampled_df = df_2
    elif timeresolution == 'D':
        resampled_df = df_2.resample('D').sum()
    elif timeresolution == 'W':
        resampled_df = df_2.resample('W').sum()
    elif timeresolution == 'M':
        resampled_df = df_2.resample('M').sum()
    elif timeresolution == 'Y':
        resampled_df = df_2.resample('Y').sum()
    else:
        raise ValueError("Unsupported time resolution. Supported values are 'H' (hours), 'D' (days), 'M' (months), and 'Y' (years).")

    # Convert the resampled DataFrame to float
    resampled_df = resampled_df.astype(float)

    result_dict = {}
    
    if value_columns is not None:
        for column in value_columns:
            value_dict = {}
            for i, (_, row) in enumerate(resampled_df.iterrows(), start=1):
                value_dict[i] = row[column]
            result_dict[column] = value_dict
    else:
        for column in resampled_df.columns:
            value_dict = {}
            for i, (_, row) in enumerate(resampled_df.iterrows(), start=1):
                value_dict[i] = row[column]
            result_dict[column] = value_dict

    # If only one column is selected, return the inner dictionary directly
    if len(result_dict) == 1:
        return result_dict[value_columns[0]] if value_columns else result_dict[resampled_df.columns[0]]
    
    # Convert the DataFrame to the desired format when value_columns is not None
    if value_columns is not None:
        result_dict = dataframe_to_dict(pd.DataFrame(result_dict))

    return result_dict

def average_value(dictionary):
    if not dictionary:
        return 0.0
    total_sum=sum(dictionary.values())
    avg=total_sum/len(dictionary)
    return avg

def scale_dict(dictionary, constant):
    scaled={}
    for key in dictionary:
        scaled[key]=dictionary[key]*constant
    return scaled 

def calculate_time_difference(start, end, timeres):
    # Create datetime objects
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)

    # Calculate hours_difference based on time resolution
    if timeres == 'H':
        time_difference = int((end_dt - start_dt).total_seconds() / 3600) + 1
    elif timeres == 'D':
        days_difference = (end_dt - start_dt).days
        time_difference = (days_difference + 1) 
    elif timeres == 'W':
        weeks_difference = (end_dt - start_dt).days // 7
        time_difference = (weeks_difference + 1)
    elif timeres == 'M':
        months_difference = (end_dt.year - start_dt.year) * 12 + end_dt.month - start_dt.month
        time_difference = months_difference   # Assuming 30 days per month
    else:
        raise ValueError("Unsupported time resolution: {}".format(timeres))

    return time_difference

def scale_value(time_resolution):
    # Define scaling factors for different time resolutions
    scaling_factors = {
        'H': 1,
        'D': 24,
        'W': 24 * 7,
    }
        # Check if the provided time resolution is valid
    if time_resolution not in scaling_factors:
        raise ValueError("Invalid time resolution. Choose from 'hour', 'day', 'week', or 'month'.")

    # Scale the value based on the chosen time resolution
    scaled_value = scaling_factors[time_resolution]

    return scaled_value

import pandas as pd

def split_data(csv_file):
    # Read CSV file with the first column as datetime index
    df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)

    # Create dictionaries for each reservoir
    reservoir1_data = {}
    reservoir2_data = {}
    solar_dict={}

    # Iterate through each year in the DataFrame
    for year in df.index.year.unique():
        # Create dictionaries for each reservoir for the current year
        reservoir1_data[year] = {}
        reservoir2_data[year] = {}
        solar_dict[year]={}
        # Iterate through each hour (1 to 8760)
        for hour in range(1, 8761):
            # Get the datetime for the current year and hour
            current_datetime = pd.Timestamp(f'{year}-01-01') + pd.DateOffset(hours=hour - 1)

            # Check if the datetime exists in the DataFrame
            if current_datetime in df.index:
                # Extract inflow values
                inflow_reservoir1 = df.loc[current_datetime, 'Ormsetvatn']
                inflow_reservoir2 = df.loc[current_datetime, 'Buavatn']
                solar_data=df.loc[current_datetime, 'Solar']
            else:
                # If the datetime is missing, set inflow values to zero
                inflow_reservoir1 = 0.0
                inflow_reservoir2 = 0.0
                solar_data=0

            # Update dictionaries
            reservoir1_data[year][hour] = inflow_reservoir1
            reservoir2_data[year][hour] = inflow_reservoir2
            solar_dict[year][hour]=solar_data

    return reservoir1_data, reservoir2_data, solar_dict


def split_data2(csv_file):
    # Read CSV file with the first column as datetime index
    df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)

    # Create dictionaries for each reservoir
    reservoir1_data = {}

    # Iterate through each year in the DataFrame
    for year in df.index.year.unique():
        # Create dictionaries for each reservoir for the current year
        reservoir1_data[year] = {}
      
        # Iterate through each hour (1 to 8760)
        for hour in range(1, 8761):
            # Get the datetime for the current year and hour
            current_datetime = pd.Timestamp(f'{year}-01-01') + pd.DateOffset(hours=hour - 1)

            # Check if the datetime exists in the DataFrame
            if current_datetime in df.index:
                # Extract inflow values
                inflow_reservoir1 = df.loc[current_datetime, 'Hourly Inflow']
                
            else:
                # If the datetime is missing, set inflow values to zero
                inflow_reservoir1 = 0.0
             

            # Update dictionaries
            reservoir1_data[year][hour] = inflow_reservoir1
        

    return reservoir1_data