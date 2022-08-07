import string

import dash
import pandas as pd
from dash import Dash, html, dcc, dash_table, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import config as cfg
import base64
from utils import *

dash.register_page(__name__)
wine_mask = np.array(Image.open("twittertry.png"))

layout = html.Div([
    dbc.Breadcrumb(
    items=[
        {"label": "Main", "href": "/", "external_link": True},
        {"label": "Compare Brands", "active": True},
    ],
    ),
    html.H1('Compare Brands'),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row(html.H4('Select Brands',className="text-dark my-1 fs-2 text-center")),
                dbc.Row(dcc.Dropdown(['Hero', 'Honda'], 'Honda', multi=True, id='compete-brand-dropdown', clearable=False))
            ],
                    width={"size": 3},),

            dbc.Col([
                dbc.Row(html.H4('Tweets or Mentions',className="text-dark my-1 fs-2 text-center")),
                dbc.Row(dcc.Dropdown(['Tweets', 'Mentions'], 'Mentions', multi=False, id='tweets-or-mentions-dropdown', clearable=False))

            ]
                    ,width={"size": 3},),
            dbc.Col([
                dbc.Row(html.H4('No. of Days',className="text-dark my-1 fs-2 text-center")),
                dbc.Row(dcc.Dropdown([i for i in range(2,11)], value=5,id='number-of-days-dropdown', clearable=False))
            ]
                    ,width={"size": 3},)

            ], justify='center',
        ),
        html.Br()]),
    dbc.Container([
        html.H2('Number of Followers', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='followers-area', justify="center"),
        html.Br(),
        html.H2('Tweet Counts', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='line-graph-area', justify="center"),
        html.Br(),
        html.H2('Tweet Sentiments', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='sentiments-area', justify="center"),
        html.Br(),
        html.H2('Wordcloud', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='wordcloud-area', justify="center"),
        html.Br(),
        html.H2('Latest #10 tweets', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='tweet-table-area', justify="center"),

    ]),
])










@callback(
    Output('followers-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_followers_count(brand_list, tweets_or_mentions, number_of_days):
    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                            follower_card('TVS', tweets_or_mentions, number_of_days),
                            ],
                           id='TVS-column', width="auto", className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    follower_card(brand, tweets_or_mentions, number_of_days),
                                    ],
                                   id=brand+'-column', width="auto", className='m-3'))
    return column_list


@callback(
    Output('line-graph-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_line_graph(brand_list, tweets_or_mentions, number_of_days):

    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                        line_grapher('TVS', tweets_or_mentions, number_of_days),
                            ],
                           id='TVS-column', width="auto", className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    line_grapher(brand, tweets_or_mentions, number_of_days),
                                    ],
                                   id=brand+'-column', width="auto", className='m-3'))
    return column_list




@callback(
    Output('sentiments-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_sentiments(brand_list, tweets_or_mentions, number_of_days):
    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                            sentiments('TVS', tweets_or_mentions, number_of_days),
                            ],
                           id='TVS-column', width="auto", className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    sentiments(brand, tweets_or_mentions, number_of_days),
                                    ],
                                   id=brand+'-column', width="auto", className='m-3'))
    return column_list


@callback(
    Output('wordcloud-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_sentiments_wordclouds(brand_list, tweets_or_mentions, number_of_days):
    def wordclouder(brandName, tweets_or_mentions, number_of_days):
        df = pd.read_excel('data/{}.xlsx'.format(brandName))
        df = df[(df.flag == tweets_or_mentions.lower())].tail(number_of_days)
        rows =['Cleaned_translated_tweet', 'Hashtags']
        content_arr=[]
        for row in rows:
            ls = df[row.lower()].to_list()
            listToStr = ' '.join([str(elem) for elem in ls])
            listToStr = listToStr.translate({ord('['): None, ord(']'): None})
            if(row=='Hashtags'):
                lst0 = [i[2:-2] for i in listToStr.split()]  # removes hashtags and inverted commas
                lst = []
                for i in lst0:
                    if '#' in i:
                        k = i.split('#')  # if multiple hashtags in one tweet/mention then splits them
                        for j in k:
                            if (j.isalpha()):
                                lst.append(
                                    j)  # only considers words, if after split accounts are tagged then neglects them
                    else:
                        lst.append(i)
            else:
                lst = [i for i in listToStr.split() if i.isalpha()]
            lst = [word for word in lst if word not in cfg.my_stopwords]
            comment_words = ''
            # stopwords = set(cfg.my_stopwords)
            comment_words += " ".join(lst) + " "

            wordcloud = WordCloud(width=1600, height=800,
                                  background_color='white',
                                  # stopwords=stopwords,
                                  min_font_size=5, mask=wine_mask).generate(comment_words)
            img = wordcloud.to_image()
            content_arr.append(img)

        return html.Div([
            dbc.Card([dbc.CardHeader(html.H3(brandName),),
                dbc.CardBody([
                    dbc.Tabs(
                        [
                            dbc.Tab(dbc.Card(
                                dbc.CardImg(src=content_arr[0], top=True)
                            ), label='Cleaned_translated_tweet'),
                            dbc.Tab(dbc.Card(
                                dbc.CardImg(src=content_arr[1], top=True)
                            ), label='Hashtags'),
                        ])
                ]),
            ]
            )])
    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                            wordclouder('TVS', tweets_or_mentions, number_of_days),
                            ],
                           id='TVS-column', width=int(12/(len(brand_list)+1)) - 1,className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    wordclouder(brand, tweets_or_mentions, number_of_days),
                                    ],
                                   id=brand+'-column', width=int(12/(len(brand_list)+1)) - 1, className='m-3'))
    return column_list


@callback(
    Output('tweet-table-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_sentiments(brand_list, tweets_or_mentions, number_of_days):
    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                            latesttweet('TVS', tweets_or_mentions, number_of_days),
                            ],
                           id='TVS-column', width="auto", className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    latesttweet(brand, tweets_or_mentions, number_of_days),
                                    ],
                                   id=brand+'-column', width="auto", className='m-3'))
    return column_list