import logging
import json
from urllib.request import urlopen

import plotly
import plotly.express as px
import pandas as pd

CAT_ORDERS = {'politician': ['joebiden',
                             'kamalaharris', 'donaldtrump', 'mikepence']}
COLOUR_PALETTE = {'positive': '#309898', 'neutral': '#9F9F9F',
                  'negative': '#FF9F00', 'Democrat': '#0F70A8', 'Republican': '#A8070C',
                  'Trump': '#A8070C', 'Pence': '#F52329', 'Biden': '#0F70A8',
                  'Harris': '#0A0EF5'}
MARGIN = {'r': 10, 't': 10, 'l': 60, 'b': 10}

with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as states_url:
    USA_STATES = json.load(states_url)

AGG_SENTIMENT_PATH = 'https://raw.githubusercontent.com/lara-ehr/tweet-the-people-vizweb/main/agg_state_sentiment.csv'
AGG_SENTIMENT = pd.read_csv(AGG_SENTIMENT_URL)


def sent_line_plot():
    '''
    Creates line graph object
    '''
    df = AGG_SENTIMENT.drop(['us_state'], axis=1).groupby(
        ['date', 'politician'])
    fig = px.line(df, x='date', y='mean_sentiment', line_group='politician', color='politician', hover_name='politician', category_orders=CAT_ORDERS,
                  color_discrete_sequence=[COLOUR_PALETTE['Biden'], COLOUR_PALETTE['Harris'], COLOUR_PALETTE['Trump'], COLOUR_PALETTE['Pence']])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def sentiment_map(ticket):
    '''
    Creates map of sentiment across US states
    '''
    df = AGG_SENTIMENT[AGG_SENTIMENT['ticket'] == ticket]
    fig = px.choropleth_mapbox(df,
                               geojson=USA_STATES,
                               locations='us_state',
                               animation_frame='date',
                               color='mean_sentiment',
                               featureidkey='properties.name',
                               color_continuous_scale=[
                                   COLOUR_PALETTE['negative'], COLOUR_PALETTE['neutral'], COLOUR_PALETTE['positive']],
                               range_color=(-0.4, 0.4),
                               mapbox_style='carto-darkmatter',
                               zoom=2, center={'lat': 37.0902, 'lon': -95.7129},
                               opacity=0.5,
                               labels={'mean_sentiment': 'average sentiment', 'us_state': 'US state'},
                               template='plotly_dark'
                               )
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'},
                      margin=MARGIN,
                      font_family="Nunito")
    fig["layout"].pop("updatemenus")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
