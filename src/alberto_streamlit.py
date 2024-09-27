#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 15:46:31 2024

@author: alonso-pinar_a
"""

import streamlit as st
import plotly.express as px
import xarray as xr
import pandas as pd
import calendar
import numpy as np
import yaml
from attrdictionary import AttrDict as attributedict

#############################################################
## Load configs parameter
#############################################################

with open("./../configs/main_alberto.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

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

# Load datasets with caching to improve performance
@st.cache(allow_output_mutation=True)
def load_data():
    dust_data = xr.open_dataset(dust)
    pm10_data = xr.open_dataset(pm10)
    pm25_data = xr.open_dataset(pm25)
    pmwildfires_data = xr.open_dataset(pmwildfires)
    return dust_data, pm10_data, pm25_data, pmwildfires_data

dust_data, pm10_data, pm25_data, pmwildfires_data = load_data()

available_data = ['Dust', 'PM10 particles', 'PM2.5 particles', 'PM wildfires']
datasets = {
    'Dust': dust_data,
    'PM10 particles': pm10_data,
    'PM2.5 particles': pm25_data,
    'PM wildfires': pmwildfires_data
}

#############################################################
## Streamlit app
#############################################################

st.title("Air Pollution Levels Over Time")

# Sidebar controls
st.sidebar.header("Filter Options")
selected_data = st.sidebar.selectbox('Select Data:', available_data)

# Function to get available months
def get_available_months(selected_data):
    data = datasets[selected_data]
    times = pd.to_datetime(data.time.values)
    available_months = np.unique(times.month)
    available_months.sort()
    month_options = [calendar.month_name[month] for month in available_months]
    return available_months, month_options

available_months, month_options = get_available_months(selected_data)

selected_month_name = st.sidebar.selectbox('Select Month:', month_options)
selected_month_index = month_options.index(selected_month_name)
selected_month = available_months[selected_month_index]

# Function to get available days
def get_available_days(selected_data, selected_month):
    data = datasets[selected_data]
    times = pd.to_datetime(data.time.values)
    month_times = times[times.month == selected_month]
    available_days = np.unique(month_times.day)
    available_days.sort()
    return available_days

available_days = get_available_days(selected_data, selected_month)
day_options = [int(day) for day in available_days]
selected_day = st.sidebar.select_slider('Select Day:', options=day_options, value=int(day_options[0]))

# Animate checkbox
animate = st.sidebar.checkbox('Animate over days')

# Function to generate static map
def generate_map(selected_data, selected_month, selected_day):
    dataset = datasets[selected_data]
    times = pd.to_datetime(dataset.time.values)
    selected_date = pd.Timestamp(year=2023, month=selected_month, day=int(selected_day))
    selected_times = times[(times.month == selected_month) & (times.day == selected_day)]
    variable_name = list(dataset.keys())[0]

    if len(selected_times) == 0:
        st.warning("No data available for the selected date.")
        return None

    units = dataset[variable_name].attrs.get('units', '')
    data = dataset.sel(time=selected_times).mean(dim='time')
    aerosol = data[variable_name]
    latitudes = data.lat.values
    longitudes = data.lon.values

    # Interpolate data
    num_new_lon = int(longitudes.size * 10)
    num_new_lat = int(latitudes.size * 10)
    new_lon = np.linspace(longitudes.min().item(), longitudes.max().item(), num=num_new_lon)
    new_lat = np.linspace(latitudes.min().item(), latitudes.max().item(), num=num_new_lat)
    lon, lat = np.meshgrid(new_lon, new_lat)
    aerosol_interp = aerosol.interp(lon=new_lon, lat=new_lat, method='linear')

    df_interp = pd.DataFrame({
        'Latitude': lat.ravel(),
        'Longitude': lon.ravel(),
        'Aerosol': aerosol_interp.values.flatten()
    })

    # Create the figure
    fig = px.scatter_mapbox(
        df_interp,
        lat='Latitude',
        lon='Longitude',
        color='Aerosol',
        color_continuous_scale='Viridis',
        mapbox_style='open-street-map',
        zoom=7,
        center={"lat": 42.16, "lon": 9.13},
        title=f"{variable_name.capitalize()} Levels on {selected_date.strftime('%Y-%m-%d')}",
        opacity=0.1,
        height=800,
        width=800
    )
    fig.layout.coloraxis.colorbar.title = f"{variable_name.capitalize()} ({units})"
    fig.update_traces(marker={'size': 5})

    return fig

# Function to generate animated map
def generate_animated_map(selected_data, selected_month):
    dataset = datasets[selected_data]
    times = pd.to_datetime(dataset.time.values)
    selected_times = times[times.month == selected_month]
    available_days = np.unique(selected_times.day)

    if len(available_days) == 0:
        st.warning("No data available for the selected month.")
        return None

    variable_name = list(dataset.keys())[0]
    units = dataset[variable_name].attrs.get('units', '')
    df_list = []

    for day in available_days:
        day_times = selected_times[selected_times.day == day]
        data = dataset.sel(time=day_times).mean(dim='time')
        aerosol = data[variable_name]
        latitudes = data.lat.values
        longitudes = data.lon.values

        # Interpolate data
        num_new_lon = int(longitudes.size * 2)
        num_new_lat = int(latitudes.size * 2)
        new_lon = np.linspace(longitudes.min().item(), longitudes.max().item(), num=num_new_lon)
        new_lat = np.linspace(latitudes.min().item(), latitudes.max().item(), num=num_new_lat)
        lon, lat = np.meshgrid(new_lon, new_lat)
        aerosol_interp = aerosol.interp(lon=new_lon, lat=new_lat, method='linear')

        df_interp = pd.DataFrame({
            'Latitude': lat.ravel(),
            'Longitude': lon.ravel(),
            'Aerosol': aerosol_interp.values.flatten(),
            'Day': int(day)
        })
        df_list.append(df_interp)

    df_all = pd.concat(df_list, ignore_index=True)

    # Create the animated figure
    fig = px.scatter_mapbox(
        df_all,
        lat='Latitude',
        lon='Longitude',
        color='Aerosol',
        animation_frame='Day',
        color_continuous_scale='Viridis',
        mapbox_style='open-street-map',
        zoom=7,
        center={"lat": 42.16, "lon": 9.13},
        title=f"{variable_name.capitalize()} Levels in {calendar.month_name[selected_month]}",
        opacity=0.5,
        height=800,
        width=800
    )
    fig.layout.coloraxis.colorbar.title = f"{variable_name.capitalize()} ({units})"
    fig.update_traces(marker={'size': 5})

    return fig

# Generate and display the map
if animate:
    fig = generate_animated_map(selected_data, selected_month)
else:
    fig = generate_map(selected_data, selected_month, selected_day)

if fig:
    st.plotly_chart(fig, use_container_width=True)
