from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly.express as px
#import dash_bootstrap_components as dbc



# Set the Bootstrap theme
#app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

#df = pd.read_csv('/home/qnava13/github/ITAM/EstComp/ProyectoFinal/taquerias_cdmx.csv')
df = pd.read_csv('/data/venues_cdmx_completa.csv')


#app.layout = dbc.Container(
#    fluid=True,
#    children=[
#        html.H1(children='Taquerías en CDMX', style={'textAlign': 'center'}),
#        dbc.Row([
#            dbc.Col(html.Label("Seleccione los venues: "), width=2),
#            dbc.Col(dcc.Dropdown(
#                options=[{'label': cat, 'value': cat} for cat in df['Venue_Category'].unique()],
#                value=['Taco Restaurant'],
#                id='VenueCat',
#                multi=True,
#                searchable=True,
#                style={'color': 'darkgrey'}
#            ), width=10),
#        ]),
#        html.Div(id='output_container', children=[]),
#        html.Br(),
#        dcc.Graph(id='tacos_map', figure={})
#    ]
#)

#@app.callback(
#    [Output(component_id='output_container', component_property='children'),
#    Output(component_id='tacos_map', component_property='figure')],
#    [Input(component_id='VenueCat', component_property='value')]
#)
#def update_graph(option_slctd):
#    container = "Los tipos de venues seleccionados son: {}".format(", ".join(option_slctd))
#    dff = df[df["Venue_Category"].isin(option_slctd)]
    
    # Create Plotly Express Map
#    fig = px.scatter_mapbox(
#        dff,
#        lon="Venue_Longitude",
#        lat="Venue_Latitude",
#        text="Venue",
#        color='Venue_Category',
#        mapbox_style='open-street-map'
#    )

#    return container, fig

#if __name__ == '__main__':
#    app.run(debug=True)

app = Dash(__name__)

#app.layout = html.Div([
#    html.H1(children='Taquerías en CDMX', style={'textAlign':'center'}),
#    html.Div([
#        html.Label("Seleccione los venues: "),
#        dcc.Dropdown(
#            options=[cat for cat in df['Venue_Category'].unique()],value=['Taco Restaurant'],id='VenueCat',multi=True,searchable=True)
#    ]),
#    html.Div(id='output_container', children=[]),
#    html.Br(),
#    dcc.Graph(id='tacos_map', figure={})
#])

def layout():
    return html.Div([
   html.H1(children='Taquerías en CDMX', style={'textAlign':'center'}),
    html.Div([
        html.Label("Seleccione los venues: "),
        dcc.Dropdown(
            options=[cat for cat in df['Venue_Category'].unique()],value=['Taco Restaurant'],id='VenueCat',multi=True,searchable=True)
    ]),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='tacos_map', figure={})
])

app.layout = layout

@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='tacos_map', component_property='figure')],
    [Input(component_id='VenueCat', component_property='value')]
)
def update_graph(value):
    print(value)
    print(type(value))

    if not isinstance(value, list):
        value = [value]

    #container = "Hola, los tipos de venues seleccionados son: {}".format(", ".join(selected_values))
    container = len(value)
    
    dffaux = df[df["Venue_Category"].isin(value)]
    
    # Creamos Mapa Plotly Express
    fig = px.scatter_mapbox(dffaux,
        lon = "Venue_Longitude",
        lat = "Venue_Latitude",
        text = "Venue",
        color ='Venue_Category',
        mapbox_style = 'open-street-map')

    return container, fig

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=8050,debug=True,use_reloader=False)