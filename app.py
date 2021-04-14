import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
from dash.dependencies import Output, Input
from scipy.io import arff
import pandas as pd

data = arff.loadarff('ProData_1999_2019_EM2_Class-Final.arff')
dt = pd.DataFrame(data[0])
dt.head()

MAP_ID = "map"
MARKER_GROUP_ID = "marker-group"
COORDINATE_CLICK_ID = "coordinate-click-id"

app = dash.Dash(__name__, external_scripts=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
    dl.Map(style={'width': '1000px', 'height': '500px'},
           center=[-17.782769, -50.924872],
           zoom=3,
           children=[
               dl.TileLayer(url="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"),
               dl.LayerGroup(id=MARKER_GROUP_ID)
           ], id=MAP_ID),
    html.P("Coordinate (click on map):"),
    html.Div(id=COORDINATE_CLICK_ID)]
)


@app.callback(Output(MARKER_GROUP_ID, 'children'), [Input(MAP_ID, 'click_lat_lng')])
def set_marker(x):
    if not x:
        return None
    return dl.Marker(position=x, children=[dl.Tooltip('Test')])


@app.callback(Output(COORDINATE_CLICK_ID, 'children'), [Input(MAP_ID, 'click_lat_lng')])
def click_coord(e):
    if not e:
        return "-"
    return json.dumps(e)


app.layout = html.Div(
    children={
        html.H1(children="Accident Likelihood Analytics"),
        html.P(
            children="Accident Likelihood prediction system",
        ),

        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": dt["WeatherCondition"],
                        "y": dt["Accident_likelihood"],
                        "type": "barchart",
                    },
                ],
                "layout": {"title": "the likelihood of accidents occurring "
                                    "based on different weather conditions"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": dt["Day_of_Week"],
                        "y": dt["WeatherCondition"],
                        "type": "barchart",
                    },
                ],
                "layout": {"title": "Accident likelihood on different days and time of the week"},
            },
        ),
    }
)
if __name__ == "__main__":
    app.run_server(debug=True)
