#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:04:54 2024

@author: alonso-pinar_a
"""

import dash
from dash import dcc, Input, Output
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import xarray as xr
import pandas as pd
import calendar
import numpy as np
import yaml 
from attrdictionary import AttrDict as attributedict

#############################################################
## Load configs parameter
#############################################################

# Import parameters values from config file by generating a dict.
# The lists will be imported as tuples.
with open("./../configs/main_alberto.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    
# Create a config dict from which we can access the keys with dot syntax
config = attributedict(config)
pathtofolder = config.dashboard.data.cams.folder
keptfiles = list(config.dashboard.data.cams.keptfiles) 


#############################################################
## Load files
#############################################################

ext = '.nc'

dust = pathtofolder + keptfiles[0] + ext
pm10 = pathtofolder + keptfiles[1] + ext 
pm25 = pathtofolder + keptfiles[2] + ext
pmwildfires = pathtofolder + keptfiles[3] + ext


with open( dust ) as f:
    dust_data = xr.open_dataset( dust )

with open( pm10 ) as f:
    pm10_data = xr.open_dataset( pm10 )

with open( pm25 ) as f:
    pm25_data = xr.open_dataset( pm25 )

with open( pmwildfires ) as f:
    pmwildfires_data = xr.open_dataset( pmwildfires )

#############################################################
## Dash app
#############################################################

available_data = ['Dust', 'PM10 particles', 'PM2.5 particles', 'PM wildfires']
datasets = {'Dust':dust_data, 'PM10 particles':pm10_data, 
            'PM2.5 particles':pm25_data, 'PM wildfires':pmwildfires_data }

data_options = [{'label':element, 'value': element} for element in available_data]

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout with dropdowns for month and day
app.layout = html.Div([
    html.H1("Air pollution levels over time"),
    html.Div([
        html.Label('Select Data:'),
        dcc.Dropdown(
            id='data-dropdown',
            options=data_options,
            value=available_data[0],
            clearable=False
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Select Month:'),
        dcc.Dropdown(
            id='month-dropdown',
            options=[],
            value=None
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Select Day:'),
        dcc.Dropdown(
            id='day-dropdown',
            options=[],
            value=None
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '5%'}),
    dcc.Graph(id='map')
])

# Callback to update the month options based on the selected dataset
@app.callback(
    Output('month-dropdown', 'options'),
    Output('month-dropdown', 'value'),
    Input('data-dropdown', 'value')
)

def update_month_options(selected_data):
    data = datasets[selected_data]
    times = pd.to_datetime(data.time.values)
    available_months = times.month.unique()
    available_months.sort_values()
    month_options = [{'label': calendar.month_name[month], 'value': month} for month in available_months]
    # Set the default day to the first available day
    default_month = available_months[0] if len(available_months) > 0 else None
    return month_options, default_month

# Callback to update the day options based on the selected month
@app.callback(
    Output('day-dropdown', 'options'),
    Output('day-dropdown', 'value'),
    Input('data-dropdown', 'value'),
    Input('month-dropdown', 'value'),
    
)
def update_day_options(selected_data, selected_month):
    data = datasets[selected_data]
    times = pd.to_datetime(data.time.values)
    month_times = times[times.month == selected_month]
    available_days = month_times.day.unique()
    available_days.sort_values()
    day_options = [{'label': day, 'value': day} for day in available_days]
    # Set the default day to the first available day
    default_day = available_days[0] if len(available_days) > 0 else None
    return day_options, default_day

# Callback to update the map based on the selected month and day
@app.callback(
    Output('map', 'figure'),
    Input('data-dropdown', 'value'),
    Input('month-dropdown', 'value'),
    Input('day-dropdown', 'value')
)
def update_map(selected_data, selected_month, selected_day):
    
    dataset = datasets[selected_data]
    times = pd.to_datetime(dataset.time.values)
    if selected_day is None or selected_month is None:
        # If no day or month is selected, return an empty figure
        fig = px.scatter_mapbox()
        fig.update_layout(
            title="No date selected.",
            mapbox_style='open-street-map'
        )
        return fig

    # Filter the dataset to the selected date
    selected_date = pd.Timestamp(year=2023, month=selected_month, day=selected_day)
    selected_times = times[(times.month == selected_month) & (times.day == selected_day)]
    
    variable_name = list(dataset.keys())[0]

    if selected_times.empty:
        # Handle case where there is no data for the selected date
        fig = px.scatter_mapbox()
        fig.update_layout(
            title="No data available for the selected date.",
            mapbox_style='open-street-map'
        )
        return fig

    
    units = dataset[variable_name].attrs.get('units', '')
    data = dataset.sel(time=selected_times).mean(dim='time')
    
    # Prepare data for plotting
    aerosol = data[variable_name]
    latitudes = data.lat.values
    longitudes = data.lon.values

    # Calculate the number of points for the new grid
    num_new_lon = longitudes.size * 10
    num_new_lat = latitudes.size * 10

    # Create new longitude and latitude arrays
    new_lon = np.linspace(longitudes.min().item(), longitudes.max().item(), num=num_new_lon)
    new_lat = np.linspace(latitudes.min().item(), latitudes.max().item(), num=num_new_lat)
    
    lon, lat = np.meshgrid( new_lon, new_lat)

    aerosol_interp = aerosol.interp(lon=new_lon, lat=new_lat, method='cubic')

    df_interp = pd.DataFrame({
        'Latitude': lat.ravel(),
        'Longitude': lon.ravel(),
        'Aerosol' : aerosol_interp.values.flatten()
    })
    
    # Create the figure using Plotly Express
    fig = px.scatter_mapbox(
        df_interp,
        lat='Latitude',
        lon='Longitude',
        color='Aerosol',
        color_continuous_scale='Viridis',
        mapbox_style='open-street-map',
        zoom=7,
        center={"lat": 42.16, "lon": 9.13},  # Center map on the data
        title=f"{variable_name.capitalize()} Levels on {selected_date.strftime('%Y-%m-%d')}",
        opacity=0.1,
        height=800,
        width=800
    )

    # Adjust marker size and opacity for better visualization

    colorbar_title = variable_name.capitalize() + ' (' + units +')' 
    fig.layout.coloraxis.colorbar.title = colorbar_title
    fig.update_traces(marker={'size': 8})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
