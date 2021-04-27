# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 12:36:41 2021
@author: Romen Samuel Wabina
"""
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import analytics.analytics as analytics
from ta import add_all_ta_features
from ta.utils import dropna
from sklearn import preprocessing 
from datetime import datetime, timedelta

from data_handler.data_handler import DataHandler

from ui.custom_dash_components import *

###################### DataHandler ######################

dh = DataHandler()

###################### Layout ###########################

app.layout = html.Div(style = {'backgroundColor': colors['background'], 
                                'marginTop' : 0, 
                                'marginBottom' : 0,
                                'paddingTop' : 0,
                                'paddingBottom': 0},
                      children = [minute_interval, 
                                layer_1, tabs, layer_3, selection_tabs,
                                layer_4,day_interval, title_indicators, gauge_indicator, 
                                title_confluence, layer_5, weighing_layer, 
                                layer_6, storage_div ])

@app.callback(
    Output('ohlc', 'figure'),
    Output('storage', 'children'),
    Input('graph_tab','value'),
    Input('time_tabs', 'value'),
    Input('coin-tabs', 'value'),
    Input('macdmarket','value'),
    )
def update_graph(graph_name, time_tabs_name, coin_tab_name, stat_name):
    df_ohlc = dh.get_data(coin_tab_name, time_tabs_name, limit = 1200)
    df_ohlc = df_ohlc.sort_values(by=['timestamp'])

    date_range = json.dumps({"start":df_ohlc.iloc[0].name.strftime('%Y-%m-%d %H:%M:%S'),"end":df_ohlc.iloc[-1].name.strftime('%Y-%m-%d %H:%M:%S')})

    return create_ohlc(df_ohlc, graph_name, time_tabs_name, coin_tab_name, stat_name),date_range

@app.callback(Output('num-indicator', 'figure'),
              [Input('interval-component', 'n_intervals'),
              Input('coin-tabs', 'value'),
              Input('time_tabs','value')])
def update_data(n, symbol, timeframe):
    df = dh.get_data(symbol,timeframe, limit = 3)
    return create_market_change_indicator(df)

@app.callback(Output('Topper','data'),
              [Input('d-interval-component','n_intervals')])
def update_topper(n):
    df = dh
    return topper_rank(df)

@app.callback(Output('market_summary','data'),
              [Input('d-interval-component','n_intervals')])
def update_market_summary(n):
    df = dh
    return market_summary(df)

@app.callback(Output('market_icon','children'),
              [Input('d-interval-component','n_intervals')])
def update_market_summary_icon(n):
    df = dh
    return market_summary_icons(df)

@app.callback(Output('market_graph','figure'),
              [Input('d-interval-component','n_intervals')])
def update_market_summary_figure(n):
    df = dh
    return market_summary_figure(df)

@app.callback(Output('coin-name-title', 'children'),
               Input('coin-tabs', 'value'))
def update_coin_name(symbol):
    return coin_names[symbol]

@app.callback(Output('coin-logo-title', 'src'),
               Input('coin-tabs', 'value'))
def update_coin_logo(symbol):
    return app.get_asset_url(f'img/{coin_imgs[symbol]}')

@app.callback([Output('rsi-gauge', 'figure'),
               Output('bullet-indicator', 'value')],
             [Input('interval-component', 'n_intervals'),
              Input('coin-tabs', 'value'),
              Input('cci', 'value'),
              Input('rsi', 'value'),
              Input('k_avg', 'value'),
              Input('sma', 'value'),
              Input('ema', 'value'),
              Input('macd', 'value'),
              Input('awesome', 'value'),
              Input('ultimate', 'value'),
              ])
def update_technical_indicators(time_tabs_name, coin_tab_name, cci, rsi, k_avg, sma, ema, macd, awesome, ultimate):
    df = dh.get_data(coin_tab_name, '1d', limit = 100).iloc[0:,:] #starting from 1 because the lastest data point's volume isn't the final volume
    df = add_all_ta_features(df.reindex(index=df.index[::-1]), open="open", high = "high", low = "low", close = "close", 
                                volume = "volume", fillna = True)
    df = df.reindex(index=df.index[::-1])

    criteria_weights = [cci, rsi, k_avg, sma, ema, macd, awesome, ultimate]
    return create_gauge_rsi_indicator(df), create_bullet_graph(df,criteria_weights)

@app.callback(Output('indicators-table', 'data'),
             [Input('interval-component', 'n_intervals'),
              Input('coin-tabs', 'value')])

def update_indicator_table(n, coin_tab_name):
    df = dh.get_data(coin_tab_name, '1d', limit = 1000)
    df = add_all_ta_features(df.reindex(index=df.index[::-1]), open = "open", high = "high", low = "low", close = "close", volume = "volume", fillna = True)
    df = df.reindex(index=df.index[::-1])
    return indicators_table(df)

if __name__ == '__main__':
    app.run_server(debug=True)