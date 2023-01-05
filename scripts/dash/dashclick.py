import webbrowser
import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json

app = dash.Dash(__name__)
df = pd.DataFrame(
   dict(
      x=[1, 2],
      y=[2, 4],
      urls=["https://www.tutorialspoint.com","https://plotly.com/dash/"],
   )
)
fig = px.scatter(df, x="x", y="y",custom_data=["urls"])
fig.update_layout(clickmode='event+select')
fig.update_traces(marker_size=20)

app.layout = html.Div(
   [
      dcc.Graph(
         id="graph_interaction",
         figure=fig,
      ),
      html.Pre(id='data')
   ]
)

@app.callback(
   Output('data', 'children'),
   Input('graph_interaction', 'clickData'))
def open_url(clickData):
   if clickData:
      webbrowser.open(clickData["points"][0]["customdata"][0
])
   else:
      raise PreventUpdate
      # return json.dumps(clickData, indent=2)
      
if __name__ == '__main__':
   app.run_server(debug=True)