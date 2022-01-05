import pandas as pd
import plotly.express as px

df = pd.read_csv('query.csv')
print(df)
df_small = df.drop(columns=['locationSource', 'magSource', 'status', 'nst', 'gap', 'magError', 'magNst', 'dmin', 'rms', 'net', 'id', 'updated', 'horizontalError', 'depthError'])
"""Weglassen von Attributen, welche für die weiteren Untersuchungen vorerst nicht von Bedeutung sind. So wird der Dataframe diesbezüglich etwas übersichtlicher."""
print(df_small)

df_small[['Date', 'Time']] = df_small.time.str.split('T', expand=True)
df_small[['Year', 'Month', 'Day']] = df_small.Date.str.split('-', expand=True)
df_small['Time'] = df_small['Time'].map(lambda x: str(x)[:-1])

df_small[['Distance', 'Region']] = df_small.place.str.split(',', expand=True)

df_small_region = df_small.loc[df['place']].str.contains(',')
for wert in df_small['place']:
    if df_small.loc[df['place']].str.contains(','):
        df_small[['Distance', 'Region']] = df_small.place.str.split(',', expand=True)
    else:
        df_small['Distance'] = ''
        df_small['Region'] = df['place']

"""if df_small.loc[df['place']].str.contains(','):
    df_small[['Distance', 'Region']] = df_small.place.str.split(',', expand=True)
else:
    df_small['Distance'] = ''
    df_small['Region'] = df['place']"""

fig = px.scatter(df_small, x='depth', y='mag')
fig.show()

fig = px.scatter_matrix(df, dimensions=["depth", "mag", "latitude", "longitude"])
fig.update_traces(diagonal_visible=False)
fig.show()