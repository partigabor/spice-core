import pandas as pd
import numpy as np
import plotly.express as px

import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html
from dash.dependencies import Input, Output
import webbrowser
from base64 import b64encode
import io
import json

# Variables

transparent = 'rgba(255,255,255,0)'
half_transparent = 'rgba(255,255,255,0.5)'
quarter_transparent = 'rgba(255,255,255,0.25)'
tenth_transparent = 'rgba(255,255,255,0.1)'

font_size = 16
font_color = "black"
font_family = "Raleway"
marker_symbol = 'circle'
marker_size = 16
max_marker_size = 32
edge_color = transparent
edge_size = 1
opacity = 0.7

grid_color = '#EDEDED'
lines = 'gainsboro'
water = 'white'
land = 'gainsboro'
copyright_color = 'lightgray'
background_color = transparent
legend_background_color = tenth_transparent

# Elements

## Traces
ne_traces = dict(
    textposition = 'middle right',
    textfont = dict(size=font_size, color=font_color, family=font_family),
    hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Species: <i>%{customdata[0]}</i><br>" +
        "Family: <i>%{customdata[1]}</i><br>" +
        "Region of origin: %{customdata[2]}<br>" +
        "Arabic: %{customdata[3]} <i>%{customdata[4]}</i><br>" +
        "Chinese: %{customdata[5]} <i>%{customdata[6]}</i><br>" +
        "Spreadability: %{customdata[7]}<br>" +
        "<extra></extra>",
    marker = dict(
        symbol = marker_symbol,
        # size = marker_size,
        line = dict(
            color=edge_color,
            width=edge_size
        )
    )
)

## Layout
ne_layout = dict(
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    geo = dict(
        resolution=110, #50 is large or 110 small
    #     scope='world',
        projection_type = 'natural earth',
        projection_scale = 1,
        # projection_rotation = {'lat': 15, 'lon': 30, 'roll': 0}, #not good for NE
        bgcolor=background_color,
        showcoastlines=True, coastlinewidth = 1, coastlinecolor = lines,
        # showcountries=True, countrywidth = 1, countrycolor = lines, 
        showframe=True, framewidth = 1, framecolor = lines, 
        showlakes=True, lakecolor = water,
        showland=True, landcolor = land, 
        showocean=True, oceancolor = water,
        showrivers=True, riverwidth = 1, rivercolor = water,
        # showsubunits=True, subunitwidth = 1, subunitcolor = lines, 
        # lonaxis = dict(showgrid = True, gridwidth = 0.5, dtick = 10, gridcolor=grid_color),
        # lataxis = dict (showgrid = True, gridwidth = 0.5, dtick = 10, gridcolor=grid_color),
    ),
    showlegend = True,
    legend=dict(x=0, y=0, xanchor="left", yanchor="bottom", bgcolor=half_transparent,  
                font=dict(color=font_color, size=font_size, family=font_family), 
                title_font=dict(color=font_color, size=font_size+2, family=font_family),
                traceorder = 'normal', orientation="v"),
    title=dict(x=0.5, y=0.99, xanchor='center', yanchor='top', text='',
               font=dict(color=font_color, size=font_size+4, family=font_family)),
    margin={"r":0,"t":0,"l":0,"b":0},
    hoverlabel=dict(#bgcolor="white", 
                    font_size=font_size, 
                    font_family=font_family),
    )



# Data

# Path
path_in = "data/"
# Read and store content of an excel file 
read_file = pd.read_excel(path_in+"spices.xlsx")
# Write the dataframe object into csv file
read_file.to_csv (path_in+"spices.csv", index = None, header=True)
# Load in dataset
df_spices=pd.read_csv(path_in+'spices.csv', header =[0], delimiter=',', encoding="utf-8")
# Include
df_spices = df_spices.loc[df_spices['include'] == 'in'] # include ones to include
# Copy
df = df_spices.copy()

# Add size using spreadability
df['spreadability'] = df['spreadability'].astype(float)
df['spreadability'] = df['spreadability'].round(3)
df['size'] = df['spreadability'] + 2



# Plotly with Dash

#########################
app = dash.Dash(__name__)

buffer = io.StringIO()
#########################

fig = px.scatter_geo(df, lat='lat', lon='lon',
    text='id',
    color="family",
    color_discrete_sequence=px.colors.qualitative.Prism,
    opacity = opacity,
    size="size",
    # size_max=max_marker_size,
    # hover_name="id", 
    hover_data={'species':True, 'family':True, 'region of origin':True, 'Arabic':True, 'Ar transliteration':True, 'Chinese':True, 'pinyin':True, 'spreadability':':.2f', 'url':True, 'lon':False, 'lat':False, 'size':False},
    labels={"group": "category"},
    )


fig.update_traces(ne_traces)

fig.update_layout(ne_layout)

fig.update_layout(clickmode='event+select')

fig.write_html(buffer)

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

######################
app.layout = html.Div([
    # html.H4('Simple plot export options'),
    # html.P("↓↓↓ try downloading the plot as PNG ↓↓↓", style={"text-align": "right", "font-weight": "bold"}),
    dcc.Graph(
        id="graph_interaction", figure=fig),
        html.Pre(id='data'),
    html.A(
        html.Button("Download"), 
        id="download",
        href="data:text/html;base64," + encoded,
        download="map.html"
    )
])

@app.callback(
    Output('data', 'children'),
    Input('graph_interaction', 'clickData'))
def open_url(clickData):
    if clickData:
        webbrowser.open(clickData["points"][0]["customdata"][8])
    else:
        raise PreventUpdate
        # return json.dumps(clickData, indent=2)

app.run_server(debug=True)

# if __name__ == '__main__':
#     app.run_server(debug=True)

############### Deployment ###############
### https://dash.plotly.com/deployment ###
##########################################