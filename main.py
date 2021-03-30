# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 12:36:41 2021
@author: Romen Samuel Wabina
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import analytics.analytics as analytics
from ta import add_all_ta_features 
from datetime import datetime, timedelta

from data_handler.data_handler import DataHandler

from ui.custom_dash_components import *

###################### DataHandler ######################

dh = DataHandler()

###################### Layout ###########################

# Create the app
app = dash.Dash()

app.layout = html.Div(style = {'backgroundColor': colors['background'], 
                                'marginTop' : 0, 
                                'marginBottom' : 0,
                                'paddingTop' : 0,
                                'paddingBottom': 0},
                      children = [minute_interval, title, tabs, number_indicator, timeframe_tabs, graph_tabs, stat_choice, ohlc_graph ])

@app.callback(
    Output('ohlc', 'figure'),
    Input('graph_tab','value'),
    Input('time_tabs', 'value'),
    Input('coin-tabs', 'value'),
    Input('macdmarket','value'),
    )

def update_graph(graph_name, time_tabs_name, coin_tab_name, stat_name):

    df_ohlc = dh.get_data(coin_tab_name, time_tabs_name, limit = 1000)
    df_ohlc = df_ohlc.sort_values(by=['timestamp'])
    return create_ohlc(df_ohlc, graph_name, time_tabs_name, coin_tab_name, stat_name)


@app.callback(Output('num-indicator', 'figure'),
              [Input('interval-component', 'n_intervals'),
              Input('coin-tabs', 'value')])
def update_data(n, symbol):
    df = dh.get_data(symbol,'1m', limit = 3)
    return create_market_change_indicator(df)

if __name__ == '__main__':
    app.run_server(debug=True)