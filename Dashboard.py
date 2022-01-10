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
df_small = df_small[df_small.place.str.contains(',')]
df_small[['Distance', 'Region']] = df_small.place.str.split(',', expand=True, n=1)
df_small[['Date', 'Time']] = df_small.time.str.split('T', expand=True)
df_small[['Year', 'Month', 'Day']] = df_small.Date.str.split('-', expand=True)

df_small['Time'] = df_small['Time'].map(lambda x: str(x)[:-1])

markdown_text = """
## Earthquakes around the World
### Facts and Figures about Earthquakes around the World January 1st 2021 to July 1st 2021.

**Time Period:** 1.1.2021 to 1.07.2021  
**Area:**            Worldwide  
**Place:**           Distance in km to nearest Settlement  
**Regions:**         Country or State of the USA  

**Magnitude:**       Strength according to Richter scale  
**Depth:**           Earthquakefocus (hypocenter) below the epicenter in km  

**Source:**          https://earthquake.usgs.gov/
"""

app.layout = html.Div([

    # html.H1("Earthquakes around the World", style={'text-align': 'center'}),
    # html.H4("Facts and Figures about Earthquakes around the World January - July 2020", style={'text-align': 'left'}),
    html.P(),

    html.Label('Choose Month'),

    dcc.Dropdown(id='Dropdown',
                 options=[
                     {'label': 'January', 'value': '01'},
                     {'label': 'February', 'value': '02'},
                     {'label': 'March', 'value': '03'},
                     {'label': 'April', 'value': '04'},
                     {'label': 'May', 'value': '05'},
                     {'label': 'June', 'value': '06'},
                     {'label': 'July', 'value': '07'},
                 ],
                 multi=True,
                 style={"width": "70%", 'textAlign': 'left'}),

    html.Label('Choose Magnitude'),

    # dcc.Slider(id='my-slider',
    #           min=0, max=8, step=0.1, value=0,
    #          tooltip={'always_visible': True},
    #         marks={0.5 * i: '{}'.format(0.5 * i) for i in range(16)}),

    dcc.RangeSlider(
        id='my-range-slider',  # any name you'd like to give it
        marks={1 * i: '{}'.format(1 * i) for i in range(8)},
        step=0.1,  # number of steps between values
        min=0,
        max=8,
        value=[0, 7.5],  # default value initially chosen
        dots=True,  # True, False - insert dots, only when step>1
        included=True,  # True, False - highlight handle
        vertical=False,  # True, False - vertical, horizontal slider
        className='None',
        tooltip={'always visible': True,  # show current slider values
                 'placement': 'top'}),

    html.Div(children=[
        dcc.Graph(id='Magnitude', figure={}),
        dcc.Graph(id='Depth', figure={})],
        style={'display': 'inline-block', 'vertical-align': 'topleft',
               'margin-left': '2.5vw', 'margin-top': '2.5vw',
               'width': '25vw', 'height': '45vh'}),

    html.Div(children=[
        dcc.Graph(id='WorldMap', figure={}),
        dcc.Markdown(id='my-markdown', children=markdown_text)],
        style={'display': 'inline-block', 'vertical-align': 'middle',
               'margin-left': '2.5vw', 'margin-top': '2.5vw',
               'width': '40vw', 'height': '95vh'}),

    html.Div(children=[
        dcc.Graph(id='Barplot', figure={}),
        dcc.Graph(id='Lineplot', figure={})],
        style={'display': 'inline-block', 'vertical-align': 'topright',
               'margin-left': '2.5vw', 'margin-top': '2.5vw',
               'width': '25vw', 'height': '45vh'})

])


@app.callback(
    [Output(component_id='Magnitude', component_property='figure'),
     Output(component_id='Depth', component_property='figure'),
     Output(component_id='WorldMap', component_property='figure'),
     Output(component_id='Barplot', component_property='figure'),
     Output(component_id='Lineplot', component_property='figure')],
    [Input(component_id='Dropdown', component_property='value'),
     Input(component_id='my-range-slider', component_property='value')]
)
def update_graph(option_slctd, option_slctd2):
    dff = df_small.copy()

    if bool(option_slctd):
        dff = dff[dff["Month"].isin(option_slctd)]

    dff = dff[dff['magnitude'].between(option_slctd2[0], option_slctd2[1], inclusive=True)]

    fig = px.box(dff, x='Month', y='magnitude')
    fig.update_layout(title={'text': 'Mean values of magnitude per month'},
                      yaxis={'title': 'Magnitude'},
                      xaxis={'title': 'Month'})

    fig2 = px.density_heatmap(dff, x="magnitude", y="depth", marginal_x="rug", marginal_y="histogram", template='plotly_dark')
    fig2.update_layout(title={'text': 'Comparison magnitude and depth, count of quakes'},
                       yaxis={'title': 'Depth'},
                       xaxis={'title': 'Magnitude'})

    fig3 = px.density_mapbox(dff, lat='latitude', lon='longitude', z='magnitude',
                             hover_name='place', hover_data=['Date'],
                             radius=10, center=dict(lat=0, lon=0), zoom=0, mapbox_style="stamen-terrain", template='plotly_dark')
    fig3.update_layout(title={'text': 'World map with all the data(magnitude by color)'})

    fig4 = px.bar(dff, x='Month', y='magnitude',
                  color='magnitude',
                  labels={'mag': 'Magnitude'}, height=450)
    fig4.update_layout(title={'text': 'Number of earthquakes per magnitude'},
                       yaxis={'title': 'Count'},
                       xaxis={'title': 'Month'})

    fig5 = px.scatter_polar(dff, r="Month", theta="Region",
                            color="magnitude",
                            color_discrete_sequence=px.colors.sequential.Plasma_r, template="plotly_dark")
    fig5.update_layout(title={'text': 'Comparison of the regions per magnitude'})


    return fig, fig2, fig3, fig4, fig5


if __name__ == "__main__":
    app.run_server(debug=False)
