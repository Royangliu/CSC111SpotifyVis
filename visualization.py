import plotly.graph_objects as go

fig = []

# for-loop iteration goes by values in a tuple (zip makes 2-value tuples with values in the list)
models = ["global", "continent", "country", "city"]
colors = ['Reds', 'Blues', 'Greens', 'Viridis']

for model, color in zip(models, colors):
    fig += [go.Figure(data = go.Choropleth(locations = accuracy_df['iso3'],
                                           text = accuracy_df['iso3'], 
                                           z =                     chosen_metric_back_into_original_data[model], 
               colorscale = colors, autocolorscale=False, reversescale=False, marker_line_color='darkgray',
               marker_line_width=0.5, colorbar_tickprefix='', colorbar_title=chosen_metric))]

# visualize figures
fig[0].show()
fig[1].show()
fig[2].show()

