import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, callback
import string
import plotly.graph_objs as go

def follower_number_homepage():
    return pd.read_excel('data/TVS.xlsx').iloc[-1]['number_of_followers']

def latest_tweet_homepage():
    df = pd.read_excel('data/TVS.xlsx')
    df = df[df.flag == 'tweets']
    tweetArray = []
    ls = reversed(df['cleaned_translated_tweet'].to_list())
    for i in ls:
        for j in (i.split("'")):
            if ((j != ']') and (j != ',') and (j != '[') and (j != ' ,') and (j != ', ') and j != ' '):
                if (len(tweetArray) < 10):
                    tweetArray.append(j)
    for i in range(len(tweetArray)):
        if (tweetArray[i][0] in string.whitespace):
            tweetArray[i] = tweetArray[i][1:]
        if (tweetArray[i][-1] in string.whitespace):
            tweetArray[i] = tweetArray[i][:-1]
    new_df = pd.DataFrame({
        "Sr No": [i + 1 for i in range(len(tweetArray))],
        "Tweet": tweetArray
    })
    return html.Div([
        dbc.Table.from_dataframe(new_df, striped=True, bordered=True, hover=True)
    ])

def follower_card(brandName, tom, days):
    df = pd.read_excel('data/{}.xlsx'.format(brandName))
    return dbc.Card(dbc.CardBody(dbc.Row([
                    dbc.Col([
                        html.Div([html.P(brandName + ' @{}'.format(df.Brand[0]), className='card-title')], className="text-xs font-weight-bold text-primary text-uppercase mb-1"),
                        html.Div([html.P(df['number_of_followers'].tolist()[-1], id='followers_number_homepage')], className="h5 mb-0 font-weight-bold text-gray-800"),
                    ]),
                    dbc.Col([
                        html.Div(html.I(className="bi bi-person-circle"))
                    ], className='col-auto'),
                ], className='no-gutters align-items-center')), className='border-left-primary shadow h-100 py-2')

def line_grapher(brandName, tweets_or_mentions, number_of_days):
    df = pd.read_excel('data/{}.xlsx'.format(brandName))
    df = df[(df.flag == tweets_or_mentions.lower())].tail(number_of_days)
    x = df['date'].tolist()
    y = df['tweet_count'].tolist()
    return dcc.Graph(figure=go.Figure(
            data=[go.Scatter(x=x, y=y, mode='lines', marker=dict(color='#0066ff'))],
            layout={'title': tweets_or_mentions + ' Count of ' + brandName,
                    'xaxis': {'title': 'Number of days'},
                    'yaxis': {'title': 'Number of ' + tweets_or_mentions}}
        ))

def sentiments(brandName, tweets_or_mentions, number_of_days):
    df = pd.read_excel('data/{}.xlsx'.format(brandName))
    df = df[(df.flag == tweets_or_mentions.lower())].tail(number_of_days)
    x = df['date'].tolist()
    return dcc.Graph(figure=dict(
            data=[dict(x=x,
                       y=df[j],
                       type='bar',
                       name=j) for j in ['POSITIVE', 'NEGATIVE']],
            layout=go.Layout(title='Sentiments count of '+brandName+' for '+tweets_or_mentions,
                             barmode='stack',
                             xaxis={'title': 'No. of days'},
                             yaxis={'title': 'Count of sentiments'})),
        )


def latesttweet(brandName, tweets_or_mentions, number_of_days):
    df = pd.read_excel('data/{}.xlsx'.format(brandName))
    df = df[(df.flag == tweets_or_mentions.lower())].tail(number_of_days)
    tweetArray =[]
    ls = reversed(df['cleaned_translated_tweet'].to_list())
    for i in ls:
        for j in (i.split("'")):
            if ((j != ']') and (j != ',') and (j != '[') and (j != ' ,') and (j != ', ') and j != ' '):
                if (len(tweetArray) < 10):
                    tweetArray.append(j)
    for i in range(len(tweetArray)):
        if (tweetArray[i][0] in string.whitespace):
            tweetArray[i] = tweetArray[i][1:]
        if (tweetArray[i][-1] in string.whitespace):
            tweetArray[i] = tweetArray[i][:-1]
    new_df = pd.DataFrame({
        "Sr No":[i+1 for i in range(len(tweetArray))],
        "Tweet":tweetArray
    })
    return html.Div([
            html.H3(brandName),
            dbc.Table.from_dataframe(new_df, striped=True, bordered=True, hover=True)
        ])

