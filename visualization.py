"""
CSC111 Project 2
Group members: Colleen Chang, Richard Li, Roy Liu, Mina (Chieh-Yi) Wu

File Description
=============================================================================
This file contains functions necessary to visualize the tree data within ""

"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import country_converter as coco

import storage


def generate_code_stream_df(data: storage.Tree, kind: str) -> pd.DataFrame:
    """
    Returns a processed dataframe listing "ISO3" codes for each country and "Streams" for the total number of
    streams among the specified region's top 5 songs

    Preconditions:
        - data.is_empty is False
        - kind in ["continent", "country", "city"]
    """
    region_to_streams = data.get_region_streams(kind)

    if kind == "continent":
        # TODO: get unique continent codes
        return pd.DataFrame()
    elif kind == "country":
        iso3_to_streams = {coco.convert(names=c, to='ISO3'): region_to_streams[c] for c in region_to_streams}
        df_dict = {"ISO3": [code for code in iso3_to_streams],
                   "Streams": [iso3_to_streams[code] for code in iso3_to_streams]}
        iso_stream_df = pd.DataFrame(df_dict, columns=["ISO3", "Streams"]).sort_values("ISO3")
        return iso_stream_df
    else:
        # TODO: get unique city codes
        return pd.DataFrame()


def generate_code_top_5_df(data: storage.Tree, kind: str) -> pd.DataFrame:
    """
    Returns a processed dataframe listing _ codes for each region with 5 columns to record the regions overall top 5
    songs (will be added as custom data in the visualization)

    Preconditions:
        - data.is_empty is False
        - kind in ["continent", "country", "city"]
    """
    region_top_5 = data.get_region_top_songs(kind)

    if kind == "continent":
        # TODO: get unique continent codes
        return pd.DataFrame()
    elif kind == "country":
        iso3_top_5 = {coco.convert(names=c, to='ISO3'): region_top_5[c] for c in region_top_5}
        df_dict = {"ISO3": [code for code in iso3_top_5],
                   "Top 1 Song": [iso3_top_5[code][0] for code in iso3_top_5],
                   "Top 2 Song": [iso3_top_5[code][1] for code in iso3_top_5],
                   "Top 3 Song": [iso3_top_5[code][2] for code in iso3_top_5],
                   "Top 4 Song": [iso3_top_5[code][3] for code in iso3_top_5],
                   "Top 5 Song": [iso3_top_5[code][4] for code in iso3_top_5]
                   }
        iso_top_song_df = pd.DataFrame(data=df_dict).sort_values("ISO3")
        return iso_top_song_df
    else:
        # TODO: get unique city codes
        return pd.DataFrame()


def visualize_world_song_data(data: storage.Tree) -> None:
    """
    Visualizes data using functions from Storage.py
    """
    fig = []

    # for-loop iteration goes by values in a tuple (zip makes 2-value tuples with values in the list)
    # TODO: models = ["Global", "Continent", "Country", "City"]
    models = ["country"]
    colors = ['Reds', 'Blues', 'Greens', 'Viridis']

    # DATA FRAMES FOR CONTINENTS
    # TODO

    # DATA FRAMES FOR COUNTRIES
    iso_stream_df = generate_code_stream_df(data, "country")
    iso_top_song_df = generate_code_top_5_df(data, "country")

    # DATA FRAMES FOR CITIES
    # TODO

    for model, color in zip(models, colors):
        fig += [go.Figure(data=go.Choropleth(locations=iso_stream_df['ISO3'],
                                             text=iso_stream_df['ISO3'],
                                             z=iso_stream_df['Streams'],
                                             customdata=np.stack((iso_top_song_df['ISO3'],
                                                                  iso_top_song_df['Top 1 Song'],
                                                                  iso_top_song_df['Top 2 Song'],
                                                                  iso_top_song_df['Top 3 Song'],
                                                                  iso_top_song_df['Top 4 Song'],
                                                                  iso_top_song_df['Top 5 Song']), axis=-1),
                                             hovertemplate="<b>Country Code: %{customdata[0]} </b><br>" +
                                                           "1st Top Song: %{customdata[1]}<br>" +
                                                           "2nd Top Song: %{customdata[2]}<br>" +
                                                           "3rd Top Song: %{customdata[3]}<br>" +
                                                           "4th Top Song: %{customdata[4]}<br>" +
                                                           "5th Top Song: %{customdata[5]}</b>",
                                             colorscale=color, autocolorscale=False, reversescale=False,
                                             colorbar_title="Top Songs: " + model))]

    fig[0].show()
