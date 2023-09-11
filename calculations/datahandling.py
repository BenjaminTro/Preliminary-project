# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 13:47:40 2023

@author: oscar
"""
import pandas as pd
import numpy as np

def read_csv_data(file_path):
    csv_data = pd.read_csv(file_path, parse_dates=[0], dtype=float)
    csv_data.set_index(csv_data.columns[0], inplace=True)
    return csv_data

def read_irr_data(file_path):  
    irr_data = pd.read_csv(file_path, parse_dates=['time'], index_col='time', dtype=float)  
    irr_data.index = irr_data.index.str[:-5]
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

def convert_to_dict(dataframe, date_1, date_2, timeresolution):
    date_1 = pd.to_datetime(date_1)
    date_2 = pd.to_datetime(date_2)
    df_2 = dataframe[date_1:date_2]

    # Resample the DataFrame based on the selected time resolution and apply sum aggregation
    if timeresolution == 'H':
        resampled_df = df_2
    elif timeresolution == 'D':
        resampled_df = df_2.resample('D').sum()
    elif timeresolution == 'M':
        resampled_df = df_2.resample('M').sum()
    elif timeresolution == 'Y':
        resampled_df = df_2.resample('Y').sum()
    else:
        raise ValueError("Unsupported time resolution. Supported values are 'H' (hours), 'D' (days), 'M' (months), and 'Y' (years).")

    # Convert the resampled DataFrame to float
    resampled_df = resampled_df.astype(float)

    result_dict = {}

    # Iterate through the DataFrame and assign values to keys ranging from 1 to the number of rows
    for i, (_, row) in enumerate(resampled_df.iterrows(), start=1):
        result_dict[i] = row[0]  # Convert the row to a list

    # Return the resulting dictionary
    return result_dict

def average_value(dictionary):
    if not dictionary:
        return 0.0
    total_sum=sum(dictionary.values())
    avg=total_sum/len(dictionary)
    return avg
    


