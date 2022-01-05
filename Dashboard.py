import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("query.csv")
df_small = df.drop(
    columns=['locationSource', 'magSource', 'status', 'nst', 'gap', 'magError', 'magNst', 'dmin', 'rms', 'net', 'id',
             'updated', 'horizontalError', 'depthError'])
df_small[['Date', 'Time']] = df_small.time.str.split('T', expand=True)
df_small[['Year', 'Month', 'Day']] = df_small.Date.str.split('-', expand=True)
# if df_small.loc[df['place']].str.contains(','):
#    df_small[['Distance', 'Region']] = df_small.place.str.split(',', expand=True)
df_small['Time'] = df_small['Time'].map(lambda x: str(x)[:-1])

app.layout = html.Div([

    html.H1("Earthquakes around the World", style={'text-align': 'center'}),
    html.H4("Facts and Figures about Earthquakes", style={'text-align': 'left'}),

    dcc.Dropdown(id='Dropdown',
                 options=[{'label': i, 'value': i} for i in df_small['Date'].unique()],
                 multi=True,
                 style={"width": "70%"}),

    dcc.Slider(id='my-slider',
               min=0, max=8, step=0.1, value=0,
               tooltip={'always_visible': True},
               marks={0.5 * i: '{}'.format(0.5 * i) for i in range(16)}),

    html.Div(children=[
        dcc.Graph(id='Magnitude', figure={}),
        dcc.Graph(id='Depth', figure={})],
        style={'display': 'inline-block', 'vertical-align': 'topleft',
                'margin-left': '2.5vw', 'margin-top': '2.5vw',
                'width': '25vw', 'height': '45vh'}),

    html.Div(children=[
        dcc.Graph(id='WorldMap', figure={})],
        style={'display': 'inline-block', 'vertical-align': 'middle',
               'margin-left': '2.5vw', 'margin-top': '2.5vw',
               'width': '40vw', 'height': '100vh'}),

    html.Div(children=[
        dcc.Graph(id='Barplot', figure={}),
        dcc.Graph(id='Lineplot', figure={})],
        style={'display': 'inline-block', 'vertical-align': 'topright',
               'margin-left': '2.5vw', 'margin-top': '2.4vw',
               'width': '25vw', 'height': '45vh'})

])


@app.callback(
    [Output(component_id='Magnitude', component_property='figure'),
     Output(component_id='Depth', component_property='figure'),
     Output(component_id='WorldMap', component_property='figure'),
     Output(component_id='Barplot', component_property='figure'),
     Output(component_id='Lineplot', component_property='figure')],
    [Input(component_id='Dropdown', component_property='value'),
     Input(component_id='my-slider', component_property='value')]
)
def update_graph(option_slctd, option_slctd2):
    dff = df_small.copy()

    if bool(option_slctd):
        dff = dff[dff["Date"].isin(option_slctd)]
    if option_slctd2 > 0:
        dff = dff[dff['mag'] == option_slctd2]

    fig = px.box(dff, x='Month', y='mag')

    fig2 = px.density_heatmap(dff, x="mag", y="depth", marginal_x="rug", marginal_y="histogram")

    fig3 = px.density_mapbox(dff, lat='latitude', lon='longitude', z='mag',
                            hover_name='place', hover_data=['Date'],
                            radius=10, center=dict(lat=0, lon=0), zoom=0, mapbox_style="stamen-terrain")


    #fig4 = px.bar_polar(dff, r="mag", theta="latitude", color="depth", template="plotly_dark",
                       #color_discrete_sequence=px.colors.sequential.Plasma_r)

    #fig4 = px.line_polar(dff, r="mag", theta="longitude", color="depth", line_close=True,
                        #color_discrete_sequence=px.colors.sequential.Plasma_r)

    fig4 = px.bar(dff, x='Month', y='mag',
             color='mag',
             labels={'mag':'Magnitude'}, height=400)

    fig5 = px.parallel_coordinates(dff,
                              dimensions=['mag', 'depth', 'latitude',
                                          'longitude'],
                              color_continuous_scale=px.colors.diverging.Tealrose,
                              color_continuous_midpoint=2)

    return fig, fig2, fig3, fig4, fig5


if __name__ == "__main__":
    app.run_server(debug=False)
