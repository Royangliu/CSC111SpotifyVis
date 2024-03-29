import plotly.graph_objects as go
import pycountry
import csv
import Storage 



def visualize_world_song_data(data: Storage.Tree, title: str, x_axis: str, y_axis: str, file_name: str))
    fig = []
    
    # for-loop iteration goes by values in a tuple (zip makes 2-value tuples with values in the list)
    models = ["Global", "Continent", "Country", "City"]
    colors = ['Reds', 'Blues', 'Greens', 'Viridis']
    
    # ISO-3 mappings 
    city_to_iso3 = {city: ...}
    country_to_iso3 = {country: pycountry.countries.get(alpha_3=country) for country in data.get_all_countries()}
    continent_to_iso3 = {}
    
    
    for model, color in zip(models, colors):
        fig += [go.Figure(data = go.Choropleth(locations = accuracy_df['iso3'],
                                               text = accuracy_df['iso3'], 
                                               z =                     chosen_metric_back_into_original_data[model], 
                   colorscale = colors, autocolorscale=False, reversescale=False, marker_line_color='darkgray',
                   marker_line_width=0.5, colorbar_tickprefix='', colorbar_title= "Top Songs: " + model))]
    
    # visualize figures
    fig[0].show()
    fig[1].show()
    fig[2].show()

