from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly.express as px

#df = pd.read_csv('/home/qnava13/github/ITAM/EstComp/ProyectoFinal/taquerias_cdmx.csv')
df = pd.read_csv('/data/venues_cdmx_completa.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Taquerías en CDMX', style={'textAlign':'center'}),
    html.Div([
        html.Label("Seleccione los venues: "),
        dcc.Dropdown(
            options=[{'label': cat, 'value': cat} for cat in df['Venue_Category'].unique()],
            value=['Taco Restaurant'],
            id='VenueCat',
            multi=True,
            searchable=True
        ),
    ]),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='tacos_map', figure={})
])

@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='tacos_map', component_property='figure')],
    [Input(component_id='VenueCat', component_property='value')]
)
def update_graph(selected_values):
    print(selected_values)
    print(type(selected_values))

    if not isinstance(selected_values, list):
        selected_values = [selected_values]

    container = "Los tipos de venues seleccionados son: {}".format(", ".join(selected_values))
    
    dff = df[df["Venue_Category"].isin(selected_values)]
    
    # Creamos Mapa Plotly Express
    fig = px.scatter_mapbox(dff,
        lon = "Venue_Longitude",
        lat = "Venue_Latitude",
        text = "Venue",
        color ='Venue_Category',
        mapbox_style = 'open-street-map')

    return container, fig

if __name__ == '__main__':
    app.run(debug=True)