#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:38:18 2024

@author: alonso-pinar_a
"""

import dash
from dash import dcc, Input, Output
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import json

#%% Declare path and files

filepath = '/Users/alonso-pinar_a/soft/data-viz-challenge-2024/data/edf_corse/reseaux/'
file = 'lignes-basse-tension-bt-aerien.geojson'
file2 = 'lignes-haute-tension-hta-aerien.geojson'
file3 = 'lignes-haute-tension-htb-aerien.geojson'

#%% Open files - this should be an external python file actually

with open( filepath + file) as f:
    geojson_data = json.load(f)

with open( filepath + file2) as f:
    geojson_data2 = json.load(f)

with open( filepath + file3) as f:
    geojson_data3 = json.load(f)
    
#%% Create the dash app

points = []
for feature in geojson_data['features']:
    if 'geo_point_2d' in feature['properties']:
        points.append({
            'lat': feature['properties']['geo_point_2d']['lat'],
            'lon': feature['properties']['geo_point_2d']['lon'],
            'statut': feature['properties']['statut']
        })
points2 = []
for feature in geojson_data2['features']:
    if 'geo_point_2d' in feature['properties']:
        points2.append({
            'lat': feature['properties']['geo_point_2d']['lat'],
            'lon': feature['properties']['geo_point_2d']['lon'],
            'statut': feature['properties']['statut']
        })
points3 = []
for feature in geojson_data3['features']:
    if 'geo_point_2d' in feature['properties']:
        points3.append({
            'lat': feature['properties']['geo_point_2d']['lat'],
            'lon': feature['properties']['geo_point_2d']['lon'],
            'statut': feature['properties']['statut']
        })
        
# Create a Dash application
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(id="tabs-example", value='tab-1', children=[
        dcc.Tab(label='EDF', value='tab-1'),
        dcc.Tab(label='Environnement', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

# Callback to render content based on selected tab
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-example', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H1("Risque sur le réseau electrique aérien"),
            dcc.Graph(
                id='geojson-map',
                figure={
                    'data': [
                        # First scatter layer
                        go.Scattermapbox(
                            lat=[point['lat'] for point in points],
                            lon=[point['lon'] for point in points],
                            mode='markers',
                            marker=go.scattermapbox.Marker(
                                size=10,
                                color='blue'  # Set color for the first set of points
                            ),
                            text=[point['statut'] for point in points],
                            name='BT aérien'
                        ),
                        # Second scatter layer
                        go.Scattermapbox(
                            lat=[point['lat'] for point in points2],
                            lon=[point['lon'] for point in points2],
                            mode='markers',
                            marker=go.scattermapbox.Marker(
                                size=10,
                                color='red'  # Set a different color for the second set of points
                            ),
                            text=[point['statut'] for point in points2],
                            name='HTA aérien'
                        ),
                        go.Scattermapbox(
                            lat=[point['lat'] for point in points3],
                            lon=[point['lon'] for point in points3],
                            mode='markers',
                            marker=go.scattermapbox.Marker(
                                size=10,
                                color='orange'  # Set a different color for the second set of points
                            ),
                            text=[point['statut'] for point in points3],
                            name='HTB aérien'
                        )
                    ],
                    'layout': go.Layout(
                        title="Réseau aérien",
                        mapbox_style="open-street-map",
                        mapbox=dict(
                            zoom=7,
                            center={"lat": 42.16, "lon": 9.13}  # Center map on the data
                        ),
                        height=800,
                        width=800
                    )
                }
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H1("Risques environnement"),
            dcc.Graph(
                id='geojson-map',
                figure={
                    'data': [
                        # First scatter layer
                        go.Scattermapbox(
                            lat=[point['lat'] for point in points],
                            lon=[point['lon'] for point in points],
                            mode='markers',
                            marker=go.scattermapbox.Marker(
                                size=10,
                                color='blue'  # Set color for the first set of points
                            ),
                            text=[point['statut'] for point in points],
                            name='BT aérien'
                        ),
                        # Second scatter layer
                        go.Scattermapbox(
                            lat=[point['lat'] for point in points2],
                            lon=[point['lon'] for point in points2],
                            mode='markers',
                            marker=go.scattermapbox.Marker(
                                size=10,
                                color='red'  # Set a different color for the second set of points
                            ),
                            text=[point['statut'] for point in points2],
                            name='HTA aérien'
                        ),
                        go.Scattermapbox(
                            lat=[point['lat'] for point in points3],
                            lon=[point['lon'] for point in points3],
                            mode='markers',
                            marker=go.scattermapbox.Marker(
                                size=10,
                                color='orange'  # Set a different color for the second set of points
                            ),
                            text=[point['statut'] for point in points3],
                            name='HTB aérien'
                        )
                    ],
                    'layout': go.Layout(
                        title="Réseau aérien",
                        mapbox_style="open-street-map",
                        mapbox=dict(
                            zoom=7,
                            center={"lat": 42.16, "lon": 9.13}  # Center map on the data
                        ),
                        height=800,
                        width=800
                    )
                }
            )
        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)