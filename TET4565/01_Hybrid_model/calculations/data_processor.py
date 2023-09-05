import pandas as pd
import numpy as np

#Reading PV panel specifications:
def read_excel_data(file_path):
    pv_panel = pd.read_excel(file_path, header=[2])
    return pv_panel

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


    