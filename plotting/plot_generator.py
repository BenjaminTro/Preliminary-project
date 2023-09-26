#import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.pyplot as plt

def plot_irr(data, time_resolution, line_color):
    data = data.resample(time_resolution).sum()

    fig = px.line(data, x=data.index, y='G(i)', title='Irradiance Data')
    fig.update_xaxes(title='Time')
    fig.update_yaxes(title='Irradiance (W/m^2)')
 
    if line_color:
        fig.update_traces(line=dict(color=line_color))

    fig.show()


def plot_PV(data, time_resolution, line_color):
    data = data.resample(time_resolution).sum()

    fig = px.line(data, x=data.index, y='P', title='PV power production')
    fig.update_xaxes(title='Time')
    fig.update_yaxes(title='Power production (MW)')
 
    if line_color:
        fig.update_traces(line=dict(color=line_color))

    fig.show()


def plot_PVcalc(data, time_resolution, line_color):
    data = data.resample(time_resolution).sum()

    fig = px.line(data, x=data.index, y='PV_power', title='PV Power Production')
    fig.update_xaxes(title='Time')
    fig.update_yaxes(title='Power production (MW)')

    if line_color:
        fig.update_traces(line=dict(color=line_color))

    fig.show()




# ----------------- SPECIFIC PLOTS FOR RESERVOIR TOPOLOGY ---------------- #

#Volume plot
def plot_vol(model):
    volume_hydro1 = []
    volume_hydro2 = []

    for period in model.periods:
        volume_hydro1.append(model.v['Hydro1', period].value)
        volume_hydro2.append(model.v['Hydro2', period].value)

    plt.figure(figsize=(10, 6))
    plt.plot(model.periods, volume_hydro1, label='Hydro1 Volume', linestyle='-')
    plt.plot(model.periods, volume_hydro2, label='Hydro2 Volume', linestyle='-')
    plt.xlabel('Periods [h]')
    plt.ylabel('Volume [MM3]')
    plt.title('Volume of reservoirs changing over time')
    plt.legend()
    plt.grid(True)
    plt.show()

#Discharge plot
def plot_disc(model):
    discharge_hydro1 = []
    discharge_hydro2 = []

    for period in model.periods:
        discharge_hydro1.append(model.q['Hydro1', period].value)
        discharge_hydro2.append(model.q['Hydro2', period].value)

    plt.figure(figsize=(10, 6))
    plt.plot(model.periods, discharge_hydro1, label='Hydro1 Discharge', linestyle='-')
    plt.plot(model.periods, discharge_hydro2, label='Hydro2 Discharge', linestyle='-')
    plt.xlabel('Periods [h]')
    plt.ylabel('Discharge [m^3/s]')
    plt.title('Discharge from Reservoirs (Hydro1 and Hydro2) vs. Time')
    plt.legend()
    plt.grid(True)
    plt.show()

#inflow plot
def plot_inflow(model):
    inflow_hydro1 = []
    inflow_hydro2 = []

    for period in model.periods:
        inflow_hydro1.append(model.inflow1[period])
        inflow_hydro2.append(model.inflow2[period])  

    plt.figure(figsize=(10, 6))
    plt.plot(model.periods, inflow_hydro1, label='Hydro1 Inflow', linestyle='-')
    plt.plot(model.periods, inflow_hydro2, label='Hydro2 Inflow', linestyle='-')
    plt.xlabel('Periods [h]')
    plt.ylabel('Inflow [$m^3/s$]')  # Update the label if the units are different
    plt.title('Inflow to Reservoirs (Hydro1 and Hydro2) vs. Time')
    plt.legend()
    plt.grid(True)
    plt.show()

#cumulative discharge plot
def plot_cumq(model):
    cumulative_q_hydro1 = []
    cumulative_q_hydro2 = []

    for j in model.periods:
        cumulative_q_hydro1.append(model.cumulative_q['Hydro1', j].value)
        cumulative_q_hydro2.append(model.cumulative_q['Hydro2', j].value)

    plt.figure(figsize=(10, 6))
    plt.plot(model.periods, cumulative_q_hydro1, label='Cumulative Discharge Hydro1', linestyle='-')
    plt.plot(model.periods, cumulative_q_hydro2, label='Cumulative Discharge Hydro2', linestyle='-')

    plt.xlabel('Periods [h]')
    plt.ylabel('Cumulative Discharge [MM3]')
    plt.legend()
    plt.grid(True)
    plt.title('Cumulative Discharge for Hydro1 and Hydro2')
    plt.show()

#cumulative inflow plot
def plot_cumin(model):
    cumulative_inflow_hydro1 = []
    cumulative_inflow_hydro2 = []

    for period in model.periods:
        cumulative_inflow_hydro1.append(model.cumulative_inflow['Hydro1', period].value)
        cumulative_inflow_hydro2.append(model.cumulative_inflow['Hydro2', period].value)

    plt.figure(figsize=(10, 6))
    plt.plot(model.periods, cumulative_inflow_hydro1, label='Hydro1 Cumulative Inflow', linestyle='-')
    plt.plot(model.periods, cumulative_inflow_hydro2, label='Hydro2 Cumulative Inflow', linestyle='-')
    plt.xlabel('Periods [h]')
    plt.ylabel('Cumulative Inflow [M3/s]')
    plt.title('Cumulative Inflow of Reservoirs changing over time')
    plt.legend()
    plt.grid(True)
    plt.show()

#head plot
def plot_head(model):
    head_hydro1_values = []
    head_hydro2_values = []

    for j in model.periods:
        head_hydro1_values.append(model.h['Hydro1', j].value)
        head_hydro2_values.append(model.h['Hydro2', j].value)

    plt.figure(figsize=(10, 6))
    plt.plot(model.periods, head_hydro1_values, label='Head Hydro1', linestyle='-')
    plt.plot(model.periods, head_hydro2_values, label='Head Hydro2', linestyle='-')
    plt.xlabel('Periods [h]')
    plt.ylabel('Head [m]')
    plt.legend()
    plt.grid(True)
    plt.title('Changing Head for Hydro1 and Hydro2')
    plt.show()

#pump plot
def plot_pump(model):
    cumulative_pump_hydro2 = []

    for period in model.periods:
        cumulative_pump_hydro2.append(model.cumulative_pump['Hydro2', period].value)

    plt.figure(figsize=(10, 6))
    plt.plot(model.periods, cumulative_pump_hydro2, label='Hydro2 Cumulative Pump', linestyle='-')
    plt.xlabel('Periods [h]')
    plt.ylabel('Cumulative Pump [M3/s]')
    plt.title('Cumulative pumping from lower reservoir to upper reservoir over time')
    plt.legend()
    plt.grid(True)
    plt.show()