import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import data_handler
from datetime import datetime
import analytics.analytics as analytics
import ta
import dash_table
import pandas as pd
import numpy as np 
import glob
import random
import base64
import pandas as pd
import dash
import dash_daq as daq

from PIL import Image
from io import BytesIO
from IPython.display import HTML

# Create the app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(external_stylesheets=external_stylesheets)
# app = dash.Dash()

coins = ['Bitcoin','Ethereum', "Ripple", "Dogecoin", 'Tezos','Litecoin','EOS','Binance', 'BTC Cash']
symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "XTZUSDT", "LTCUSDT", "EOSUSDT", "BNBUSDT", "BCHUSDT"]
coin_names = {"BTCUSDT": "Bitcoin", "ETHUSDT":"Ethereum","XRPUSDT":"Ripple","DOGEUSDT":"Dogecoin","XTZUSDT":"Tezos","LTCUSDT":"Litecoin","EOSUSDT":"EOS","BNBUSDT":"Binance","BCHUSDT":"Bitcoin Cash"}
coin_codes = {"BTCUSDT": "Bitcoin", "ETHUSDT":"Ethereum","XRPUSDT":"Ripple","DOGEUSDT":"Dogecoin","XTZUSDT":"Tezos","LTCUSDT":"Litecoin","EOSUSDT":"EOS","BNBUSDT":"Binance","BCHUSDT":"Bitcoin Cash"}
# coin_codes = {"BTCUSDT": "BTC", "ETHUSDT":"ETH","XRPUSDT":"XRP","DOGEUSDT":"DOGE","XTZUSDT":"XTZ","LTCUSDT":"LTC","EOSUSDT":"EOS","BNBUSDT":"BNB","BCHUSDT":"BCH"}
coin_imgs = {"BTCUSDT": "BTC.png", "ETHUSDT":"ETH.png","XRPUSDT":"XRP.png","DOGEUSDT":"DOGE.png","XTZUSDT":"XTZ.png","LTCUSDT":"LITE.png","EOSUSDT":"EOS.png","BNBUSDT":"BNB.png","BCHUSDT":"BITCASH.png"}

timeframes = ['1m','5m','1h', '1d']
plot_type = ['Line Plot','Candlestick']

colors = {'background': '#000022','text': '#DADBFE'}

title = html.H1(children = 'CryptoView', 
                style = {'textAlign': 'left', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '96px',
                        'display':'inline',
                        'marginLeft':40,
                        'font-weight': 9000,
                        'marginTop':0,
                        'marginBottom':0}) 

tabs = dcc.Tabs(id = 'coin-tabs', value = symbols[0],
        children = [dcc.Tab(label=coin,value=symbol) for coin, symbol in zip(coins, symbols)],
        colors = {
                'border' : 'firebrick',
                'primary': 'darkblue',
                'background': 'firebrick'},
        style = {'color': colors['text'],
                'font-family': 'Helvetica',
                'font-size':"120%",
                'marginTop':"0px",
                'paddingLeft': "30px",
                'paddingRight': "30px"})

number_indicator = dcc.Graph(id='num-indicator', 
        style = {'order':3,'marginRight':'30px','margin-left':'auto'},
        figure={
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', height =200,
            width=1100,
            )})

def create_market_change_indicator(data):
    ''' 
    Input is a dataframe containing data of at least the last two timestamps
    '''
    current_data = data.iloc[1,:]
    previous_data = data.iloc[2,:]

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        title = 'Closing Price',
        mode = "number+delta",
        value = current_data['close'],
        domain = {'x': [0, 0.33], 'y': [0, 0]},
        delta = {'reference': previous_data['close'], 'relative': True, 'position' : "bottom"},
        number={"font":{"size":60},'prefix':"$"},
        ))
    
    fig.add_trace(go.Indicator(
        title = 'Dollar Volume',
        mode = "number+delta",
        value = current_data['volume']*current_data['close'],
        domain = {'x': [0.33, 0.66], 'y': [0, 0]},
        delta = {'reference': previous_data['volume']*previous_data['close'], 'relative': True, 'position' : "bottom"},
        number={"font":{"size":60},'prefix':"$"},
        ))
    
    fig.add_trace(go.Indicator(
        title = 'Trading Volume',
        mode = "number+delta",
        value = current_data['volume'],
        domain = {'x': [0.66, 1.0], 'y': [0, 0]},
        delta = {'reference': previous_data['volume'], 'relative': True, 'position' : "bottom"},
        number={"font":{"size":60}},
        ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = {'color': colors['text'],'family': "Helvetica"},
        )

    return fig

minute_interval = dcc.Interval(
        id='interval-component',
        interval=60*1000,
        n_intervals=0
    )

time_tabs_styles = {
                'margin': '3px',
                'width': '60px',
                'height': '50px',
                'border-radius': '15px',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center'
            }

time_tab_selected_style = {
                'margin': '3px',
                'width': '60px',
                'height': '50px',
                'border-radius': '15px',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center'
            }

timeframe_tabs = dcc.Tabs(id = 'time_tabs', value = timeframes[0],
        children = [dcc.Tab(label=time, value=time, style = time_tabs_styles, selected_style=time_tab_selected_style) for time in timeframes],
        colors = {
                'border' : 'firebrick',
                'primary': 'darkblue',
                'background': 'firebrick'},
        style = {'color': colors['text'],
                'font-family': 'Helvetica',
                'font-size':"120%",
                'paddingLeft': "50px",
                'paddingRight': "50px",
                'height': '50px',
                'display': 'flex',
                'border-radius': '15px',})

graph_tabs_styles = {
                'margin': '3px',
                'width': '150px',
                'height': '50px',
                'border-radius': '15px',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center'
            }

graph_tab_selected_style = {
                'margin': '3px',
                'width': '150px',
                'height': '50px',
                'border-radius': '15px',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center'
            }

graph_tabs = dcc.Tabs(id = 'graph_tab', value = 'Candlestick',
        children = [dcc.Tab(label=atype, value=atype, style = graph_tabs_styles, selected_style=graph_tab_selected_style) for atype in plot_type],
        colors = {
                'border' : 'firebrick',
                'primary': 'darkblue',
                'background': 'firebrick'},
        style = {'color': colors['text'],
                'font-family': 'Helvetica',
                'font-size':"120%",
                'marginTop':"0px",
                'paddingLeft': "0px",
                'paddingRight': "0px",
                'text-align': 'center',
                'height': '50px',
                'display': 'flex',
                'vertical-align': 'center',
                'border-radius': '15px',
                })

stat_choice = dcc.Checklist(
                id='macdmarket',
                options=[{'label': i, 'value': i} for i in ['MACD', 'Market Volume']],
                value=['MACD', 'Market Volume'],
                inputStyle={'padding' : "10px"},
                labelStyle={'display': 'inline-block',
                            'color': colors['text'],
                            'font-family': 'Helvetica',
                            'font-size':"150%",
                            'paddingLeft' : "10px"},
                style = {'font-family': 'Helvetica',
                        'font-size':"100%",
                        'paddingTop' : "7px",
                        'height': '50px',
                        'display': 'flex'})

selection_tabs = html.Div(id = 'selection',
                        style = {'backgroundColor': colors['background'], 
                                'marginTop' : 0, 
                                'marginBottom' : 0,
                                'paddingLeft': "490px",
                                'paddingTop' : 0,
                                'paddingBottom': 0,
                                'display': 'flex',
                                'width' : 2000},
                      children = [graph_tabs, timeframe_tabs, stat_choice])

title_indicators = html.H6 (children = 'TECHNICAL INDICATORS', 
                style = {'textAlign': 'center', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '30px',
                        'font-weight': 9000,
                        'paddingTop':10,
                        'paddingBottom':0,
                        'paddingLeft':30,
                        'marginTop':0,
                        'marginBottom':0})

title_confluence = html.H6 (children = 'CONFLUENCE', 
                style = {'textAlign': 'center', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '30px',
                        'font-weight': 9000,
                        'paddingTop':10,
                        'paddingBottom':0,
                        'paddingLeft':30,
                        'marginTop':0,
                        'marginBottom':0})

gauge_indicator = dcc.Graph(id ='rsi-gauge',
        style = {'width': '100%',
                 'display': 'inline-block'},
        figure = {
            'layout': go.Layout(
                paper_bgcolor = 'rgba(0,0,0,0)',
                plot_bgcolor = 'rgba(0,0,0,0)',
                height = 350)})

def create_gauge_rsi_indicator(data):
    current_data = data.iloc[0, :]
    previous_data = data.iloc[1, :] 

    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 0.3], 'y': [0, 0]},
        value = current_data['momentum_rsi'],
        mode = 'gauge+number+delta',
        title = {'text': "Relative Strength Index"},
        delta = {'reference': previous_data['momentum_rsi']},
        gauge = {'axis': {'range': [0, 100]},
        'steps' : [
            {'range': [0, 20], 'color': "lightgray"},
            {'range': [80, 100], 'color': 'darkred'}],
            'threshold' : {'line': {'color': "orange", 'width': 4}, 'thickness': 0.75, 'value': current_data['momentum_rsi']}}))

    fig.add_annotation(x = 0.03, y = -0.15,
            text = 'BUY',
            showarrow = False,
            font = dict(
                family = 'Helvetica',
                size = 18))

    fig.add_annotation(x = 0.239, y = -0.15,
            text = 'SELL',
            showarrow = False,
            font = dict(
                family = 'Helvetica',
                size = 18))

    fig.add_trace(go.Indicator(
        domain = {'x': [0.32, 0.7], 'y': [0, 0]},
        value = current_data['trend_cci'],
        mode = 'gauge+number+delta',
        title = {'text': 'Commodity Channel Index'},
        delta = {'reference': previous_data['trend_cci']},
        gauge = {'axis': {'range': [-200, 200]},
        'steps' : [
            {'range': [-200, -100], 'color': 'lightgray'},
            {'range': [100, 200], 'color': 'darkred'}],
            'threshold': {'line': {'color': 'orange', 'width': 4}, 'thickness': 0.75, 'value': current_data['trend_cci']}}))

    fig.add_annotation(x = 0.405, y = -0.15,
            text = 'BUY',
            showarrow = False,
            font = dict(
                family = 'Helvetica',
                size = 18))

    fig.add_annotation(x = 0.614, y = -0.15,
            text = 'SELL',
            showarrow = False,
            font = dict(
                family = 'Helvetica',
                size = 18))

    fig.add_trace(go.Indicator(
        domain = {'x': [0.75, 1], 'y': [0, 0]},
        value = current_data['momentum_uo'],
        mode = 'gauge+number+delta',
        title = {'text': 'Ultimate Oscillator'},
        delta = {'reference': previous_data['momentum_uo']},
        gauge = {'axis': {'range': [None, 100]},
        'steps' : [
            {'range': [0, 30], 'color': 'lightgray'},
            {'range': [70, 100], 'color': 'darkred'}],
            'threshold': {'line': {'color': 'yellow', 'width': 4}, 'thickness': 0.75, 'value': current_data['momentum_uo']}}))

    fig.add_annotation(x = 0.785, y = -0.15,
            text = 'BUY',
            showarrow = False,
            font = dict(
                family = 'Helvetica',
                size = 18))

    fig.add_annotation(x = 0.995, y = -0.15,
            text = 'SELL',
            showarrow = False,
            font = dict(
                family = 'Helvetica',
                size = 18))
    
    fig.update_layout( 
        paper_bgcolor = colors['background'],
        plot_bgcolor = colors['background'],
        font = {'color': colors['text'], 'family': "Helvetica"})
    return fig

buy = html.Div(
    html.Div(children = [
        html.H1(children = 'Buy', id = 'buy',
                style = {'textAlign': 'left', 
                        'color': '#369d75', 
                        'font-family': 'Helvetica', 
                        'font-size': '50px',
                        'marginLeft':'400px',
                        'marginRight':'200px',
                        'marginTop':'30px',
                        'paddingBottom': 60
                        }),
        ],
    ),
    style = {'display':'flex','order':1}
)
bullet_graph = daq.GraduatedBar(id = 'bullet-indicator',
    color={"gradient": True, "ranges":{"#369d75":[0,0.4],"#FDD023":[0.4,0.6],"firebrick":[0.6,1.0]}},
    showCurrentValue=True,
    size=1000,
    min=0,
    max=1,
    step = 0.01,
    style={'display':'flex','align-items': 'center',}
    )  

technicals = html.Div(children = [bullet_graph], 
            style={'width': '100%', 
            'display': 'flex',
            "paddingBottom": 60,
            'order':2,
            'marginTop':'30px',
            })

sell = html.Div(
    html.Div(children = [
        html.H1(children = 'Sell', id = 'sell',
                style = {'textAlign': 'left', 
                        'color': 'firebrick', 
                        'font-family': 'Helvetica', 
                        'font-size': '50px',
                        'marginRight':'400px',
                        'marginLeft':'200px',
                        'marginTop':'30px',
                        'paddingBottom': 60
                        }),
        ],
    ),
    style = {'display':'flex','order':3}
)

def create_bullet_graph(data, weights):
    close = data['close'][0]
    macd_signal = data['trend_macd_signal'][0]
    ao_prev = data['momentum_ao'][1]
    data = np.round(data[['trend_cci', 'momentum_rsi', 'momentum_kama', 'trend_sma_fast', 'trend_ema_fast', 'trend_macd', 'momentum_ao', 'momentum_uo']], 2)
    data = np.transpose(data).iloc[:, 0]
    values = np.array(data)
    signals = analytics.signal_indicator(close, values, macd_signal, ao_prev)
#    total_buy = ((1.5 * signals.count('SELL')) + (2 * signals.count('STRONG SELL')) + 
#                    signals.count('NEUTRAL'))/(len(signals)) #Need to change this, for initialization only
    
    signals_value = []
    for sig in signals:
        if sig == 'STRONG BUY':
            signals_value.append(0.0)
        elif sig == 'BUY':
            signals_value.append(0.25)
        elif sig == 'NEUTRAL':
            signals_value.append(0.5)
        elif sig == 'SELL':
            signals_value.append(0.75)
        elif sig == 'STRONG SELL':
            signals_value.append(1.0)
    
    weights = np.array(weights)
    signals_value = np.array(signals_value)
    weighted_signals = weights@signals_value/np.sum(weights)
    return weighted_signals



day_interval = dcc.Interval(
        id='d-interval-component',
        interval=60*60*60*1000,
        n_intervals=0)

indicators = ['Indicators', '24H Values', '24H Signals']
indicators_col_name = ["Indicators","24h Values", "24h Signals"]

techindicator_summary = html.Div(dash_table.DataTable(
    id = 'indicators-table',
    columns = [{"name" : indicators_col_name[i], "id":col, 
        "type": 'any',} for i,col in enumerate(indicators)],
    editable = False,
    style_header = {'background_color': colors['background'],
                    'font-family': 'Helvetica',
                    'font-size': '175%',
                    # 'fontWeight': 'bold',
                    'textAlign': 'center',
                    'marginTop': 0,
                    'color': colors['text'],
                    'marginBottom': 0,
                    'border': '0px',
                    'textAlign': 'center',
                    'paddingRight':20,
                    'paddingLeft': 20,
                    'paddingBottom': 10},
    style_table = {'width': '10px',
                   'paddingLeft': 50,
                   'paddingBottom': 5},
    style_cell = {'minWidt': 100, 
                  'width': 110,
                  'maxWidt': 300,
                  'font-size' : '160%',
                  'font-family': 'Helvetica',
                  'backgroundColor': 'firebrick',
                  'color': colors['text'],
                  'textAlign': 'center'},
    style_data = {'border': '5px solid #000022'},
    style_data_conditional = [
        {
            'if': {'filter_query': '{24H Signals} eq "BUY" or {24H Signals} eq "STRONG BUY"'},
            'backgroundColor': '#369d75',
            'color': 'white'
        },
        {
            'if': {'filter_query': '{24H Signals} eq "NEUTRAL"'},
            'backgroundColor': 'dodgerblue',
            'color': 'white'
        }]
    ), 
    style={ 'width': '35%', 
            'order':1, 
            'height':370,
            'marginLeft': '300px',
            'align-items':'center',
            'paddingLeft': '150px'
            })

def indicators_table(data):
    close = data['close'][0]
    macd_signal = data['trend_macd_signal'][0]
    ao_prev = data['momentum_ao'][1]
    data = np.round(data[['trend_cci', 'momentum_rsi', 'momentum_kama', 'trend_sma_fast', 'trend_ema_fast', 'trend_macd', 'momentum_ao', 'momentum_uo']], 2)
    data = np.transpose(data).iloc[:, 0]
    values = np.array(data)
    signals = analytics.signal_indicator(close, values, macd_signal, ao_prev)
    indicators = ['Trend CCI', 'Relative Strength', 'Kaufmans Average', 'Simple MA', 'Exponential MA', 'MACD', 'Awesome Oscillator', 'Ultimate Oscillator']
    columns = ['Indicators', '24H Values', '24H Signals',  'Simple MA', 'Exponential MA', 'MACD', 'Awesome Oscillator', 'Ultimate Oscillator']
    df = pd.DataFrame(data = [indicators, values, signals], columns = columns)
    df = np.transpose(df)
    df = df.reset_index(drop = True)
    df = df.rename(columns = {0: 'Indicators', 1: '24H Values', 2: '24H Signals'})
    df = df.to_dict('records')
    return df

toppers = ["gainer","gainer_perc", "loser","loser_perc"]
col_name = ["24h Gainer","24h Gainer","24h Loser","24h Loser"]
col_colours = ['#369d75','firebrick']

toppers_table = html.Div(dash_table.DataTable(
    id='Topper',
    columns=[{"name" : col_name[i],
              "id":col, 
            "type": "numeric",

            } 
            for i,col in enumerate(toppers)],
    style_header = {'backgroundColor': '#000022',
                    'font-family': 'Helvetica',
                    'font-size':"180%",
                    'color':"#DADBFE",
                    # 'fontWeight': 'bold',
                    'border': '0px',
                    'textAlign': 'center',
                    },
    style_table = {'width': '8px',
                   'paddingLeft': 50,
                   'paddingTop': 40},
    style_cell = {'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                  'font-family': 'Helvetica',
                  'backgroundColor': '#000022',
                  'color': '#DADBFE',
                  'text-align': 'center'},
    style_data={ 'border': '5px solid #000022'},
    style_data_conditional=([ {'if': {'column_id': c},
                                    'backgroundColor': col_colours[i],
                                    # 'fontWeight': 'bold'
                             } for i,c in enumerate(["gainer","loser"])] +
                             [{'if': {'column_id': c},
                                    'color': col_colours[i],
                                    'fontWeight': 'bold'
                             } for i,c in enumerate(["gainer_perc","loser_perc"])
     ]),
    merge_duplicate_headers=True
    ),
    style = {'display':'flex',
            'marginTop': '20px',
            'marginLeft': '200px',
            'order':1,
            'width': '35%'
    }
    )
market_sum = ["coin","close", "open","volume"]
market_sum_col_name = ["Market Summary","Market Summary","Market Summary","Market Summary"]
market_col_colours = ['#FFFF00','#0000FF','#FFA500']
market_summary_table = html.Div(dash_table.DataTable(
    id='market_summary',
    columns=[{"name" : market_sum_col_name[i],
              "id":col, 
            "type": "numeric",
            } 
            for i,col in enumerate(market_sum)],
    merge_duplicate_headers = True,
    style_header = {'backgroundColor': '#000022',
                    'font-family': 'Helvetica',
                    'font-size':"180%",
                    'color':"#DADBFE",
                    # 'fontWeight': 'bold',
                    'border': '0px',
                    'textAlign':"center",
                    },
    style_table = {'width':'10px',
                   'display':'inline-block'},
    style_cell={'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'font-family': 'Helvetica',
                # 'font-weight': 'bold',
                'backgroundColor': '#000022',
                'color': '#DADBFE',
                'textAlign': 'center'},
    style_data={ 'border': '10px solid #000022'},
    style_data_conditional=([ {'if': {'column_id': c,'row_index': 0},
                                    'color': market_col_colours[i],
                                    'fontWeight': 'bold'
                             } for i,c in enumerate(["close","open","volume"])
     ]),
    ),
    style = {'display':'flex',
             'marginTop': '10px',
             'order':3,
             'width': '45%',
    }
    )

market_summary_icon = html.Div(html.Div(id = 'market_icon'),
        style = {'display':'flex',
                 'paddingLeft': 100,
                 'marginLeft': '300px',
                 'marginTop': '95px',
                 'order':2,
                 'width': '10%'
        }
        )

market_summary_graph = html.Div(dcc.Graph(id='market_graph', 
        config = {'displayModeBar': False},
        style = {'display': 'flex', 
                 'width': '100%',
                 'margin_bottom':'5px',
                 'paddingRight': 200,
                 'paddingBottom': 500},
        figure={
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height = 250,
            width = 200
            )}
        ),
        style = {'display':'flex',
                 'paddingRight': '250px',
                 'marginBottom': '150px',
                 'marginTop': '15px',
                 'order':4,
                 'width': '15%'
        }
        )

ohlc_graph = dcc.Graph(id='ohlc',
    config={'modeBarButtonsToAdd':['drawline',
                                    'drawopenpath',
                                    'drawcircle',
                                    'drawrect',
                                    'eraseshape']},
    style = {'display': 'flex',
            'width': '100%',
            'paddingLeft': "80px",
            },
    figure={
    'layout': go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height = 800,
        #width = 1500,
        )}) 

def create_ohlc(df_ohlc, graph_name, time_tabs_name, coin_tab_name, stat_name):
    timestamp_dict = {  '1m':df_ohlc.index.strftime("%H:%M %d/%m/%Y"),
                        '5m':df_ohlc.index.strftime("%H:%M %d/%m/%Y"),
                        '1h':df_ohlc.index.strftime("%H:%M %d/%m/%Y"),
                        '1d':df_ohlc.index.strftime("%H:%M %d/%m/%Y")}
                
    x_data = timestamp_dict[time_tabs_name]

    if graph_name == 'Candlestick':
        fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2], 
                            vertical_spacing=0, shared_xaxes=True,
                            specs=[[{"secondary_y": False}],
                                   [{"secondary_y": True}]]) 

        fig.add_trace(go.Candlestick(x=x_data,open=df_ohlc['open'], high=df_ohlc['high'], low=df_ohlc['low'], close=df_ohlc['close'],
                                increasing_line_color='#2FB835', decreasing_line_color='#FF3535', name='candlestick'), row=1, col=1)

        fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font = {'color': colors['text'],'family': "Helvetica"},
                )

    else :
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.009, 
                            horizontal_spacing=0.009, row_heights=[0.8, 0.2],
                            specs=[[{"secondary_y": False}],
                                   [{"secondary_y": True}]])

        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['close'], mode = 'lines', yaxis="y1", xaxis="x1",
            name='Close Price',
            connectgaps=True, marker = dict(color='rgb(255, 255, 0)')),row=1, col=1)

        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['open'], mode = 'lines', yaxis="y1", xaxis="x1",
            name='Open Price',
            connectgaps=True, marker = dict(color = 'rgb(0, 0, 255)')),row=1, col=1)
        
        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['high'], mode = 'lines', yaxis="y1", xaxis="x1",
            name='High',
            connectgaps=True, marker = dict(color='rgb(225, 0, 0)')),row=1, col=1)
        
        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['low'], mode = 'lines', yaxis="y1", xaxis="x1",
            name='Low',
            connectgaps=True, marker = dict(color='rgb(0, 255, 0)')),row=1, col=1)

    fig.update_layout(
        legend=dict(orientation="h",yanchor="bottom",y=1.0,xanchor="right",x=0.94),
        yaxis=dict(title="USD",titlefont=dict(color="#FFFFFF"),tickfont=dict(color="#FFFFFF"),
        layer="above traces",
        anchor="free",
        side="left",
        position=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = {'color': colors['text'],'family': "Helvetica"},
        newshape_line_color='#FFF8B7',
        newshape_line_width=2,
        margin_t=50,
        margin_b=100
        )

    if 'MACD' in stat_name:
        macd_data = ta.trend.macd(df_ohlc['close'])
        fig.add_trace(go.Scatter(x = x_data, y = macd_data, mode = 'lines', yaxis="y2", xaxis="x2",
            name='MACD', connectgaps=True, marker = dict(color='#6FE9FF')), 
            row=2, col=1, secondary_y=False)
        fig.update_layout(
            yaxis2=dict(
            title="MACD",
            fixedrange=True,
            titlefont=dict(
                color="#6FE9FF"),
            tickfont=dict(
                color="#6FE9FF"),
            layer="below traces",
            side="left")
            )
        
    if 'Market Volume' in stat_name:
        if len(stat_name) == 1:
            fig.add_trace(go.Bar(x = x_data, y = df_ohlc['volume'], yaxis="y2", xaxis="x2",
                name='Market Volume', marker = dict(color='#FF84E3')), 
                row=2, col=1, secondary_y=False)
            fig.update_layout(
                yaxis2=dict(
                title="Market Volume",
                fixedrange=True,
                titlefont=dict(
                    color="#FF84E3"),
                tickfont=dict(
                    color="#FF84E3"),
                layer="below traces",
                side="right")
                )
        else:
            fig.add_trace(go.Bar(x = x_data, y = df_ohlc['volume'], yaxis="y3", xaxis="x2",
                name='Market Volume', marker = dict(color='#FF84E3')), 
                row=2, col=1, secondary_y=True)
            fig.update_layout(
                yaxis3=dict(
                title="Market Volume",
                fixedrange=True,
                titlefont=dict(
                    color="#FF84E3"),
                tickfont=dict(
                    color="#FF84E3"),
                layer="below traces",
                side="right")
                )

    data_count = (fig.data[0].x).shape[0]

    if data_count < 1200 :
        fig.update_xaxes(range=[data_count-200,data_count],
            showgrid=False, zeroline=False, rangeslider_visible=False,
            showspikes=True, spikemode='across', spikesnap='cursor', showline=True,
            spikecolor="rgb(10, 10, 10)",spikethickness=0.3, spikedash='solid')

        if graph_name == 'Line Plot':
            y_min = min(fig.data[0].y[data_count-200:data_count])
            y_max = max(fig.data[0].y[data_count-200:data_count])
        else:
            y_min = min(fig.data[0].low[data_count-200:data_count])
            y_max = max(fig.data[0].high[data_count-200:data_count])
        # fig.update_yaxes(range=[y_min-2,y_max+2],
        #     showspikes=True, spikedash='solid',spikemode='across', showticklabels=True,
        #     spikecolor="rgb(10, 10, 10)",spikesnap="cursor",spikethickness=0.3, )
    else:
        fig.update_xaxes(range=[1000,1200],
            showgrid=False, zeroline=False, rangeslider_visible=False,
            showspikes=True, spikemode='across', spikesnap='cursor', showline=True,
            spikecolor="rgb(10, 10, 10)",spikethickness=0.3, spikedash='solid')
        
        if graph_name == 'Line Plot':
            y_min = min(fig.data[0].y[data_count-200:data_count])
            y_max = max(fig.data[0].y[data_count-200:data_count])
        else:
            y_min = min(fig.data[0].low[data_count-200:data_count])
            y_max = max(fig.data[0].high[data_count-200:data_count])

    fig.update_yaxes(showspikes=True, spikedash='solid',spikemode='across', showticklabels=True,
                spikecolor="rgb(10, 10, 10)",spikesnap="cursor",spikethickness=0.3, )
        
    # if graph_name == 'Line Plot':
    #     y_mins = []
    #     y_maxs = []
    #     for trace_data in fig.data:
    #         y_mins.append(min(trace_data.y))
    #         y_maxs.append(max(trace_data.y))
    #     y_min = min(y_mins)
    #     y_max = max(y_maxs)
    #     print(y_min)
    #     print(y_max)

    if ('Market Volume' not in stat_name and 'MACD' not in stat_name):
        fig.update_layout(
        yaxis = dict(range=[y_min,y_max]),
        xaxis=dict(showticklabels=True),
        xaxis2=dict(showticklabels=False))
    else:
        fig.update_layout(
            yaxis = dict(range=[y_min,y_max]),
            xaxis=dict(showticklabels=False),
            xaxis2=dict(showticklabels=True),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='closest',
            font = {'color': colors['text'],'family': "Helvetica"})

    return fig

storage_component = html.Div(id='intermediate-value', style={'display': 'none'}) 

day_interval = dcc.Interval(
        id='d-interval-component',
        interval=60*60*60*1000,
        n_intervals=0
    )

def sort_coin(data, sort_by):
    sorted_coin = []
    for i, coin in enumerate(symbols):
        coin_info = {}
        df = data.get_data(coin,'1d',limit = 3)
        curr = df.iloc[1,:]
        prev = df.iloc[2,:]
        out = '{:.1f}'.format(100*(curr['close']-prev['close'])/curr['close'])
        coin_info['percents'] = out
        coin_info['closes'] = df['close'].iloc[1]
        coin_info['opens'] = df['open'].iloc[1]
        coin_info['volumes'] = df['volume'].iloc[1]
        sorted_coin.append(coin_info)
        if sort_by == 'percent':
            coin_info['coins'] = coin_names[coin]
        else:
            coin_info['coins'] = coin_codes[coin]
    if sort_by == 'percent':
        return sorted(sorted_coin, key = lambda i: float(i['percents']), reverse=True)
        # return sorted(sorted_coin.items(), key=lambda item: item[1],reverse=True)
    else:
        return sorted(sorted_coin, key = lambda i: float(i['volumes']),reverse=True)

def topper_rank(data):
    sorted_coin = sort_coin(data, 'percent')
    ranks = []
    for i in range(3):
        rank = {}
        rank['gainer'] = sorted_coin[i]['coins']
        rank['gainer_perc'] = '{}%'.format(sorted_coin[i]['percents'])
        rank['loser'] = sorted_coin[-(i+1)]['coins']
        rank['loser_perc'] = '{}%'.format(sorted_coin[-(i+1)]['percents'])
        ranks.append(rank)
    return ranks

def market_summary(data):
    sorted_coin = sort_coin(data, 'volume')
    ranks = []
    rank_top = {}
    rank_top['coin'] = ''
    rank_top['close'] = 'Close'
    rank_top['open'] = 'Open'
    rank_top['volume'] = 'Volume'
    ranks.append(rank_top)
    for i in range(3):
        rank = {}
        rank['coin'] = sorted_coin[i]['coins']
        rank['close'] = '{:.3f}'.format(sorted_coin[i]['closes'])
        rank['open'] = '{:.3f}'.format(sorted_coin[i]['opens'])
        rank['volume'] = sorted_coin[i]['volumes']
        ranks.append(rank)
    return ranks

def get_thumbnail(path):
    i = Image.open(path)
    i.thumbnail((30, 30), Image.LANCZOS)
    buff = BytesIO()
    i.save(buff, format="PNG")
    encoded_image = base64.b64encode(buff.getvalue()).decode('UTF-8')
    return (html.Img(src='data:image/png;base64,{}'.format(encoded_image)))

def market_summary_icons(data):
    sorted_coin = sort_coin(data, 'volume')
    images_div = []
    for i in range(3):
        coin = sorted_coin[i]['coins']
        images_div.append(html.Div([get_thumbnail(f'img/{coin}.png')]))
    return images_div

def market_summary_figure(data):
    sorted_coin = sort_coin(data, 'volume')

    fig = make_subplots(rows=3, cols=1 ,vertical_spacing=0.009,horizontal_spacing=0.009, row_heights=[1/3, 1/3, 1/3])
    
    for i in range(3):
        d2 = dict((v, k) for k, v in coin_codes.items())
        df = data.get_data(d2[sorted_coin[i]['coins']],'1m',limit =1000)
        df = df.sort_values(by=['timestamp'])
        x_data = df.index.strftime("%H:%M")
        fig.add_trace(go.Scatter(x = x_data, y = df['close'], mode = 'lines',
        showlegend = False,
        connectgaps=True, marker = dict(color='rgb(255, 255, 0)')),row=i+1, col=1)

    fig.update_xaxes(showgrid=False, zeroline=False, rangeslider_visible=False, showticklabels=False,
                showspikes=True, spikemode='across', spikesnap='cursor', showline=False,
                spikecolor="rgb(10, 10, 10)",spikethickness=0.3, spikedash='solid')

    fig.update_yaxes(showspikes=False, spikedash='solid',spikemode='across', showticklabels=False,showgrid=False, zeroline=False, 
                    spikecolor="rgb(10, 10, 10)",spikesnap="cursor",spikethickness=0.3)

    fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font = {'color': colors['text'],'family': "Helvetica"},
    )

    return fig

coin_logo_title = html.Div(html.Img(id = 'coin-logo-title',src=app.get_asset_url('img/BTC.png'),
        style={'height':'50px', 
                'width':'50px',}),
    style = {'order':1,'align-self':'center','paddingLeft':150 }
)

coin_name_title = html.Div(
    html.Div(children = [
        html.H1(children = 'Bitcoin', id = 'coin-name-title',
                style = {'textAlign': 'left', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '60px',
                        #'fontWeight': 'bold',
                        'paddingTop':20,
                        'paddingBottom':20,
                        'paddingLeft':60,
                        'marginTop':0,
                        'marginBottom':0,
                        }),
        ],
        style = {'vertical-align':'middle','display':'table-cell'}
    ),
    style = {'order':2,'align-self':'center','height': 200,'display':'table'}
)

logo = html.Img(id='logo', src=app.get_asset_url('img/logo.png'),
        style={'height':'120px','display':'inline-block'})
  
layer_1 = html.Div(id = 'layer-1', children = [
    logo, title
],style = { 
            'display':'flex',
            'align-items':'center',
            'paddingTop':30,
            'paddingBottom':40,
            'paddingLeft':30,
})

layer_3 = html.Div(id = 'layer-3', children = [
    coin_logo_title, coin_name_title, number_indicator
],style = {'display':'flex','width':'100%'})

debug_text = html.H3(id = 'debug-text',children = 'hi', 
                style = {'textAlign': 'left', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '24px',
                        'display':'inline',
                        'marginLeft':40,
                        'font-weight': 9000,
                        'marginTop':0,
                        'marginBottom':0}) 


storage_div = html.Div(id='storage', style={'display': 'none'})

layer_4 = html.Div(id = 'layer-4', children = [
    ohlc_graph
],style = {'display':'inline-block','width':'100%'})

layer_5 = html.Div(id = 'layer-5', children = [ sell, technicals, buy
],style = {'display':'flex','width':'100%'})


layer_6 =  html.Div(id = 'layer-6', children = [ toppers_table, market_summary_icon, market_summary_table,market_summary_graph
],style = {'display':'flex','width':'100%'})


def create_slider(id):
    slider = dcc.Slider(id=id, min=0, max=1.0, step=0.01, value=0.5)
    return slider
    
sliders = html.Div([
    create_slider('cci'),
    create_slider('rsi'),
    create_slider('k_avg'),
    create_slider('sma'),
    create_slider('ema'),
    create_slider('macd'),
    create_slider('awesome'),
    create_slider('ultimate'),
], style = {'order':2,
            'width':'35%',
            'margin-top':'auto',
            'margin-right':'100px',
            'padding-left':'250px',
            'align-items':'center'
}
)

weighing_layer = html.Div([
    techindicator_summary,
    sliders
], style = {'width':'100%',
            'display':'flex'
})