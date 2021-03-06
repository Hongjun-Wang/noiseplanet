# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:19:54 2020

@author: arthurd
"""


import json
import numpy as np

from noiseplanet import utils
from noiseplanet.matcher import model
from noiseplanet import ui


def create_html_plot():
    
    print("Test Route HTML plot")

    trackname = 'track_1'
    file_name_raw = 'data/track/' + trackname + '.geojson'
    file_name_nearest = 'data/track_nearest/' + trackname + '_nearest.geojson'
    file_name_hmm = 'data/track_hmm/' + trackname + '_hmm.geojson'
    
    with open(file_name_raw) as f:
        geojson_raw = json.load(f)
    with open(file_name_nearest) as f:
        geojson_nearest = json.load(f)
    with open(file_name_hmm) as f:
        geojson_hmm = json.load(f)
    
    # convert in dataframe
    df_raw = utils.geojson_to_df(geojson_raw, normalize_header=True)
    df_nearest = utils.geojson_to_df(geojson_nearest, normalize_header=True)
    df_hmm = utils.geojson_to_df(geojson_hmm, normalize_header=True)
       
    # Fill None values by interpolation
    df_raw = df_raw.interpolate(method='quadratic', axis=0)
    df_nearest = df_nearest.interpolate(method='quadratic', axis=0)
    df_hmm = df_hmm.interpolate(method='quadratic', axis=0)
    
    # Delete rows where no positions
    df_raw = df_raw[df_raw['type'].notnull()]
    df_nearest = df_nearest[df_nearest['type'].notnull()]
    df_hmm = df_hmm[df_hmm['type'].notnull()]
    
    # Create tracks
    coord = np.array([*df_raw['coordinates']])
    X = coord[:, 0]
    Y = coord[:, 1]
    track_raw = np.column_stack((Y, X))
    
    coord = np.array([*df_nearest['coordinates']])
    X = coord[:, 0]
    Y = coord[:, 1]
    track_nearest = np.column_stack((Y, X))
    
    coord = np.array([*df_hmm['coordinates']])
    X = coord[:, 0]
    Y = coord[:, 1]
    track_hmm = np.column_stack((Y, X))
    
    # track length
    print("Track length :", len(track_raw))
    
    graph = model.graph_from_track(track_raw)
    
    route_nearest, stats_nearest = model.route_from_track(graph, track_nearest)
    route_hmm, stats_hmm = model.route_from_track(graph, track_hmm)
    
    # plot
    ui.foroute.plot_html(track_raw, track_corr=track_nearest, route_corr=route_nearest,
              proj=True,
              graph=graph,
              file_name='my_map_nearest_' + trackname + '.html'
              )
    
    ui.foroute.plot_html(track_raw, track_corr=track_hmm, route_corr=route_hmm,
              proj=True,
              graph=graph,
              file_name='my_map_hmm_' + trackname + '.html'
              )




if __name__ == "__main__":
    
    create_html_plot()
        
    # Q, R = hexgrid.nearest_hexagons(lon, lat, side_length=side_length, origin=origin,
    #                     proj_init=proj_init, proj_out=proj_out)
    # Xcenter, Ycenter = hexgrid.hexs_to_cartesians(Q, R, side_length=side_length, origin=origin,
    #                     proj_init=proj_out, proj_out=proj_init)
    # hexagons = hexgrid.hexagons_coordinates(Xcenter, Ycenter, side_length=side_length,
    #                                 proj_init=proj_init, proj_out=proj_out)


    # add_hexagons_folium(m, hexagons)
    
    
    
