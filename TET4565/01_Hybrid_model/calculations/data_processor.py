import pandas as pd
import numpy as np

#Reading PV panel specifications:
def read_excel_data(file_path):
    pv_panel = pd.read_excel(file_path, header=[2])
    return pv_panel
    
#Reading irradiance data from JRC:
def read_csv_data(file_path):  
    irr_data = pd.read_csv(file_path, parse_dates=['time'], index_col='time', dtype=float)  
    irr_data.index = irr_data.index.str[:-5]
    irr_data.index = pd.to_datetime(irr_data.index, format='%Y%m%d')
    irr_data['hours'] = irr_data.groupby(irr_data.index.date).cumcount()
    irr_data.index = irr_data.index + pd.to_timedelta(irr_data['hours'], unit='h')
    irr_data.drop(columns='hours', inplace=True)
    return irr_data


def perform_calculation(pv_panel, irr_data):  #implement tilt and azimuth as inputs as well in order to more accurately calculate PV power production (use book from home)
    # Extract specific values from pv_data (assumed to be a DataFrame)
    P =  pv_panel.loc[0,'P_max']
    V_oc =  pv_panel.loc[0, 'V_oc']
    V_mp =  pv_panel.loc[0, 'V_mp']
    I_sc =  pv_panel.loc[0, 'I_sc']
    I_mp =  pv_panel.loc[0, 'I_mp']
    n_eff = pv_panel.loc[0, 'n_eff']
    no_panels = pv_panel.loc[0, 'no_panels']
    length =  pv_panel.loc[0, 'length']
    width =  pv_panel.loc[0, 'width']
    alfa =  pv_panel.loc[0, 'alfa']

    #STC values for PV panels
    T_ref = 25

    # Extract specific values from irr_data (assumed to be a DataFrame)
    irr_ref = irr_data['G(i)'].values
    T = irr_data['T2m'].values

    # Effective irradiance (NEED SOURCE)
    irr_eff = irr_ref*(1+alfa*(T-T_ref))

    # Panel Power Output
    time_index = irr_data.index
    PV_power = np.round(P*irr_eff/irr_ref)  # (NEED SOURCE FOR THIS EQUATION)
    PV_power = np.nan_to_num(PV_power, nan=0)
    pv_power_df = pd.DataFrame({'PV_power': PV_power}, index=time_index)
    
    return pv_power_df
    


#calculated_value = np.round((P * n_eff)/(length*width),2)


    