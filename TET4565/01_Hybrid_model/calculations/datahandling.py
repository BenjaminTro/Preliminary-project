# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 13:47:40 2023

@author: oscar
"""
import pandas as pd
import numpy as np

def read_csv_data(file_path):  
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


    
rad_data=read_csv_data('data/Data_solar_irr_NOR.csv')
PV_data=read_excel_file('data/PV_spec.xlsx')
spec=return_specific_date('data/Data_solar_irr_NOR.csv','2018-01-15','2018-02-09') 

print(rad_data)
print(PV_data, "\n")
print(spec)

