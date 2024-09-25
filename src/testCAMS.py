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


#%% Declare path and files

filepath = '/Users/alonso-pinar_a/soft/data-viz-challenge-2024/src/'
files = os.listdir(filepath)
filenames = sorted([f for f in files if ( f.endswith('nc') ) ])

#%% Open files - this should be an external python file actually

temp_list = [xr.open_dataset( filepath + elt ) for elt in filenames[:10]]
data = xr.concat(temp_list, dim='time')

ds = data

#%% Dash app

# Extract available months and days from the dataset
times = pd.to_datetime(ds.time.values)
available_months = times.month.unique()
available_months.sort_values()
month_options = [{'label': calendar.month_name[month], 'value': month} for month in available_months]

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout with dropdowns for month and day
app.layout = html.Div([
    html.H1("PM10 Levels Over Time"),
    html.Div([
        html.Label('Select Month:'),
        dcc.Dropdown(
            id='month-dropdown',
            options=month_options,
            value=available_months[0]
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
    dcc.Graph(id='pm10-map')
])

# Callback to update the day options based on the selected month
@app.callback(
    Output('day-dropdown', 'options'),
    Output('day-dropdown', 'value'),
    Input('month-dropdown', 'value')
)
def update_day_options(selected_month):
    # Filter times to the selected month
    month_times = times[times.month == selected_month]
    available_days = month_times.day.unique()
    available_days.sort_values()
    day_options = [{'label': day, 'value': day} for day in available_days]
    # Set the default day to the first available day
    default_day = available_days[0] if len(available_days) > 0 else None
    return day_options, default_day

# Callback to update the map based on the selected month and day
@app.callback(
    Output('pm10-map', 'figure'),
    Input('month-dropdown', 'value'),
    Input('day-dropdown', 'value')
)
def update_map(selected_month, selected_day):
    if selected_day is None:
        # If no day is selected, return an empty figure
        fig = px.scatter_mapbox()
        fig.update_layout(
            title="No day selected.",
            mapbox_style='open-street-map'
        )
        return fig

    # Filter the dataset to the selected date
    selected_date = pd.Timestamp(year=2023, month=selected_month, day=selected_day)
    selected_times = times[(times.month == selected_month) & (times.day == selected_day)]

    if selected_times.empty:
        # Handle case where there is no data for the selected date
        fig = px.scatter_mapbox()
        fig.update_layout(
            title="No data available for the selected date.",
            mapbox_style='open-street-map'
        )
        return fig

    # For simplicity, we'll take the average over the hours in the selected day
    data = ds.sel(time=selected_times).mean(dim='time')

    # Prepare data for plotting
    pm10 = data.dust
    latitudes = data.lat.values
    longitudes = data.lon.values

    # Calculate the number of points for the new grid
    num_new_lon = longitudes.size * 10
    num_new_lat = latitudes.size * 10

    # Create new longitude and latitude arrays
    new_lon = np.linspace(longitudes.min().item(), longitudes.max().item(), num=num_new_lon)
    new_lat = np.linspace(latitudes.min().item(), latitudes.max().item(), num=num_new_lat)
    
    lon, lat = np.meshgrid( new_lon, new_lat)

    dust_interp = pm10.interp(lon=new_lon, lat=new_lat, method='cubic')

    df_interp = pd.DataFrame({
        'Latitude': lat.ravel(),
        'Longitude': lon.ravel(),
        'PM10': dust_interp.values.flatten()
    })

    # Create the figure using Plotly Express
    fig = px.scatter_mapbox(
        df_interp,
        lat='Latitude',
        lon='Longitude',
        color='PM10',
        color_continuous_scale='Viridis',
        mapbox_style='open-street-map',
        zoom=7,
        center={"lat": 42.16, "lon": 9.13},  # Center map on the data
        title=f"PM10 Levels on {selected_date.strftime('%Y-%m-%d')}",
        opacity=0.1,
        height=800,
        width=800
    )

    # Adjust marker size and opacity for better visualization
    fig.update_traces(marker={'size': 8})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
