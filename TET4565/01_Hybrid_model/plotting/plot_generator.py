#import matplotlib.pyplot as plt
import plotly.express as px

def plot_irr(data, time_resolution, line_color):
    data = data.resample(time_resolution).sum()

    fig = px.line(data, x=data.index, y='G(i)', title='Irradiance Data')
    fig.update_xaxes(title='Time')
    fig.update_yaxes(title='Irradiance (W/m^2)')
 
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

