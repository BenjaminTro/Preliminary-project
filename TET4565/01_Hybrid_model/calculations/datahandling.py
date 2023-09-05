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

def read_excel_file(filename):
    df=pd.read_excel(filename, header=[2])
    return df
<<<<<<< HEAD
=======

def read_csv_range(file_path, date_1, date_2):
    df = pd.read_csv(file_path, dtype=float)
    date_column = None
    for column in df.columns:
        try:
            df[column] = pd.to_datetime(df[column])
            if date_column is None:
                date_column = column
            else:
                df[column] = df[column].astype(float)  # Convert non-datetime columns to floats
        except ValueError:
            pass

    if date_column is None:
        raise ValueError("No date column found in the CSV file.")

    # Filter the DataFrame to include only rows within the specified date range
    filtered_df = df[(df[date_column] >= date_1) & (df[date_column] <= date_2)]

    # Sort the DataFrame by the date column
    sorted_df = filtered_df.sort_values(by=date_column)
    return sorted_df
    
def return_specific_date(file_path, date_x, date_y):
    df=pd.read_csv(file_path, parse_dates=['time'], index_col='time', dtype=float) 
    df.index = df.index.str[:-5]
    df.index = pd.to_datetime(df.index, format='%Y%m%d')
    df['time']= pd.to_datetime(df.index, format='%Y%m%d') 
    df['hours'] = df.groupby(df.index.date).cumcount()
    df.index = df.index + pd.to_timedelta(df['hours'], unit='h')
    df.drop(columns='hours', inplace=True)
    mask = df[(df['time'] >= date_x) & (df['time'] <= date_y)]
    return mask
>>>>>>> 7b7bcbd97b315cf7d1fa015dbbf50b032cfd9e27



