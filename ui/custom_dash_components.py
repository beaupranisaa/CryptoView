import dash_html_components as html
import dash_core_components as dcc
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

from PIL import Image
from io import BytesIO
from IPython.display import HTML

# Create the app
app = dash.Dash()

coins = ['Bitcoin','Ethereum', "Ripple", "Dogecoin", 'Tezos','Litecoin','EOS','Binance', 'BTC Cash']
symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "XTZUSDT", "LTCUSDT", "EOSUSDT", "BNBUSDT", "BCHUSDT"]
coin_names = {"BTCUSDT": "BITCOIN", "ETHUSDT":"ETHEREUM","XRPUSDT":"RIPPLE","DOGEUSDT":"DOGECOIN","XTZUSDT":"TEZOS","LTCUSDT":"LITECOIN","EOSUSDT":"EOS","BNBUSDT":"BINANCE","BCHUSDT":"BITCOIN CASH"}
coin_codes = {"BTCUSDT": "BTC", "ETHUSDT":"ETH","XRPUSDT":"XRP","DOGEUSDT":"DOGE","XTZUSDT":"XTZ","LTCUSDT":"LTC","EOSUSDT":"EOS","BNBUSDT":"BNB","BCHUSDT":"BCH"}
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
        style = {'float':'right','marginRight':'30px'},
        figure={
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', height =200)})

def create_market_change_indicator(data):
    ''' 
    Input is a dataframe containing data of atleast the last two timestamps
    '''
    current_data = data.iloc[1,:]
    previous_data = data.iloc[2,:]

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        title = 'Closing Price',
        mode = "number+delta",
        value = current_data['close'],
        domain = {'x': [0, 0.5], 'y': [0, 0]},
        delta = {'reference': previous_data['close'], 'relative': True, 'position' : "bottom"},
        number={"font":{"size":60}},
        ))
    
    fig.add_trace(go.Indicator(
        title = 'Volume',
        mode = "number+delta",
        value = current_data['volume'],
        domain = {'x': [0.5, 1.0], 'y': [0, 0]},
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
    
ohlc_graph = dcc.Graph(id='ohlc',
        config={'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ]},
        style = {'display': 'inline-block', 'width': '100%'},
        figure={
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height = 1000,
            width = 1500)})



timeframe_title = html.H2 (children = 'Timeframe:', 
                style = {'textAlign': 'center', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '25px',
                        'font-weight': 9000,
                        'paddingTop':10,
                        'paddingBottom':0,
                        'paddingLeft':30,
                        'marginTop':0,
                        'marginBottom':0,
                        'display': 'inline-block'})

time_tabs_styles = {
                'borderLeft': '3px solid #000022',
                'borderRight': '3px solid #000022',
                'width': '60px',
                'height': '50px',
                'border-radius': '15px',
                'display': 'inline-block'
            }

time_tab_selected_style = {
                'borderLeft': '3px solid #000022',
                'borderRight': '3px solid #000022',
                'width': '60px',
                'height': '50px',
                'border-radius': '15px',
                'display': 'inline-block'
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
                'marginTop':"0px",
                'paddingLeft': "0px",
                'paddingRight': "0px",
                'text-align': 'center',
                'height': '50px',
                'display': 'inline-block',
                'vertical-align': 'center',
                'border-radius': '15px',})

graph_title = html.H2 (children = 'Plot Type:', 
                style = {'textAlign': 'center', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '25px',
                        'font-weight': 9000,
                        'paddingTop':10,
                        'paddingBottom':0,
                        'paddingLeft':30,
                        'marginTop':0,
                        'marginBottom':0,
                        'display': 'inline-block'})
graph_tabs_styles = {
                'borderLeft': '3px solid #000022',
                'borderRight': '3px solid #000022',
                'borderTop': '3px solid #000022',
                'width': '150px',
                'height': '50px',
                'border-radius': '15px',
                'textAlign': 'center',
                'display': 'inline-block'
            }

graph_tab_selected_style = {
                'borderLeft': '3px solid #000022',
                'borderRight': '3px solid #000022',
                'borderTop': '3px solid #000022',
                'width': '150px',
                'height': '50px',
                'border-radius': '15px',
                'textAlign': 'center',
                'display': 'inline-block'
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
                'display': 'inline-block',
                'vertical-align': 'center',
                'border-radius': '15px',
                })
stat_title = html.H2 (children = 'Statistics:', 
                style = {'textAlign': 'center', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '25px',
                        'font-weight': 9000,
                        'paddingTop':10,
                        'paddingBottom':0,
                        'paddingLeft':30,
                        'marginTop':0,
                        'marginBottom':0,
                        'display': 'inline-block'})
stat_choice = dcc.Checklist(
                id='macdmarket',
                options=[{'label': i, 'value': i} for i in ['MACD', 'Market Volume']],
                value=['MACD', 'Market Volume'],
                labelStyle={'display': 'inline-block',
                'color': colors['text'],
                'font-family': 'Helvetica',
                'font-size':"150%"},
                style = {'font-family': 'Helvetica',
                'font-size':"100%",
                'marginTop':"0px",
                'paddingLeft': "0px",
                'paddingRight': "0px",
                'text-align': 'center',
                'height': '50px',
                'display': 'inline-block',
                'vertical-align': 'top',
                'horizontalAlign': "center"})

selection_tabs = html.Div(id = 'selection',
                        style = {'backgroundColor': colors['background'], 
                                'marginTop' : 0, 
                                'marginBottom' : 0,
                                'paddingTop' : 0,
                                'paddingBottom': 0,
                                'display': 'inline-block',
                                'width' : 1500},
                      children = [graph_title, graph_tabs, timeframe_title, timeframe_tabs,stat_title,stat_choice])

title_indicators = html.H6 (children = 'Technical Indicators', 
                style = {'textAlign': 'center', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '25px',
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
    current_data = data.iloc[0, :] #Change it to 1
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
    
    fig.add_trace(go.Indicator(
        domain = {'x': [0.32, 0.7], 'y': [0, 0]},
        value = current_data['trend_cci'],
        mode = 'gauge+number+delta',
        title = {'text': 'Commodity Channel Index'},
        delta = {'reference': previous_data['trend_cci']},
        gauge = {'axis': {'range': [-200, 200]},
        'steps' : [
            {'range': [-200, -150], 'color': 'white'},
            {'range': [-150, -100], 'color': 'lightgray'},
            {'range': [100, 150], 'color': 'firebrick'},
            {'range': [150, 200], 'color': 'darkred'}],
            'threshold': {'line': {'color': 'orange', 'width': 4}, 'thickness': 0.75, 'value': current_data['trend_cci']}}))

    fig.add_trace(go.Indicator(
        domain = {'x': [0.75, 1], 'y': [0, 0]},
        value = current_data['momentum_kama'],
        mode = 'gauge+number+delta',
        title = {'text': 'Moving Averages'},
        delta = {'reference': previous_data['momentum_kama']},
        gauge = {'axis': {'range': [None, data['close'].max()]},
        'steps' : [
            {'range': [0, 0.25*data['close'].max()], 'color': 'lightgray'},
            {'range': [0.75*data['close'].max(), data['close'].max()], 'color': 'darkred'}],
            'threshold': {'line': {'color': 'yellow', 'width': 4}, 'thickness': 0.75, 'value': current_data['momentum_kama']}}))

    fig.update_layout( 
        paper_bgcolor = colors['background'],
        plot_bgcolor = colors['background'],
        font = {'color': colors['text'], 'family': "Helvetica"})
    return fig
     

title_summary = html.H6(children = 'Summary', 
                style = {'textAlign': 'center', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '25px',
                        'paddingTop': 0,
                        'paddingBottom':0,
                        'paddingLeft':30,
                        'marginTop':0,
                        'marginBottom':0}) 

bullet_graph = dcc.Graph(id = 'bullet-indicator',
        style = {'width': '100%',
                 'paddingBottom': 0,
                 'paddingTop' : 0,
                 'marginTop': 0,
                 'marginBottom':0},
        figure = {
            'layout': go.Layout(
                paper_bgcolor = 'rgba(0,0,0,0)',
                plot_bgcolor = 'rgba(0,0,0,0)',
                height = 250)})

def create_bullet_graph(data):
    norm_data = analytics.normalize_indicator(data)
    current_data = norm_data[0, :]
    previous_data = norm_data[1, :]

#    print(data.columns)
#    print(current_data[4:],np.mean(current_data[4:]))
#    print(previous_data[4:],np.mean(previous_data[4:]))

    fig = go.Figure(go.Indicator(
        mode = 'number+gauge+delta',
        gauge = {'shape': 'bullet',
                 'axis' : {'range' : [0, 1]},
                 'threshold' : {
                     'line' : {'color': 'yellow', 'width': 3},
                     'thickness' : 0.75,
                     'value' : np.mean(current_data[4:])},
                 'steps': [
                     {'range' : [0, 0.4], 'color': 'lightgray'},
                     {'range' : [0.8, 1], 'color': 'firebrick'}]},
        value = np.mean(current_data[4:]),
        delta = {'reference': np.mean(previous_data[4:])},
        domain = {'x': [1, 0], 'y': [0, 0]}))
    
    fig.update_layout(
        paper_bgcolor = colors['background'],
        plot_bgcolor = colors['background'],
        font = {'color': colors['text'], 'family': 'Helvetica'})
    return fig

day_interval = dcc.Interval(
        id='d-interval-component',
        interval=60*60*60*1000,
        n_intervals=0)

indicators = ["trend_cci", "trend_cci", "trend_macd_signal"]
indicators_col_name = ["Indicators","Value", "Signal"]


techindicator_summary = dash_table.DataTable(
    id = 'indicators-table',
    columns = [{"name" : indicators_col_name[i], "id":col, 
        "type": "numeric",} for i,col in enumerate(indicators)],
    editable = True,
    style_header = {'background_color': colors['background'],
                    'font-family': 'Helvetica',
                    'font-size': '120%',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'marginTop': 0,
                    'color': colors['text'],
                    'marginBottom': 0,
                    'border': '0px',
                    'textAlign': 'center',
                    'paddingRight':20,
                    'paddingLeft': 50,
                    'paddingBottom': 10},
    style_table = {'width': '10px',
                   'paddingLeft': 50,
                   'paddingBottom': 20},
    style_cell = {'minWidt': 100, 
                  'width': 110,
                  'maxWidt': 300,
                  'font-family': 'Helvetica',
                  'backgroundColor': 'firebrick',
                  'color': colors['text'],
                  'textAlign': 'center'},
    style_data = {'border': '5px solid #000022'})

def indicators_table(data):
    # data = np.transpose(data)
    # data = data[data.columns[0]]
    # data = data.to_dict('records')
    data = data[['trend_cci', 'momentum_stoch_rsi', 'trend_macd_signal']]
    # data = np.transpose(data).iloc[:, 0]
    data = np.transpose(data.to_dict('records'))[0:5]
    #data = list(data.to_dict('index').values())[0:5]
    return data



toppers = ["gainer","gainer_perc", "loser","loser_perc"]
col_name = ["24h GAINER","","24h LOSER",""]
col_colours = ['#008000','#FF0000']

toppers_table = dash_table.DataTable(
    id='Topper',
    columns=[{"name" : col_name[i],
              "id":col, 
            "type": "numeric",
            } 
            for i,col in enumerate(toppers)],
    style_header = {'backgroundColor': '#000022',
                    'font-family': 'Helvetica',
                    'font-size':"120%",
                    'color':"#DADBFE",
                    'fontWeight': 'bold',
                    'paddingRight':100,
                    'marginTop':0,
                    'marginBottom':0,
                    'border': '0px',
                    'text-align': 'center',
                    },
    style_table = {'width':'10px'},
    style_cell={'minWidt': 95, 
                'width': 95, 
                'maxWidth': 140,
                'font-family': 'Helvetica',
                'backgroundColor': '#000022',
                'color': '#DADBFE',
                'text-align': 'center'},
    style_data={ 'border': '5px solid #000022'},
    style_data_conditional=([ {'if': {'column_id': c},
                                    'backgroundColor': col_colours[i],
                                    'fontWeight': 'bold'
                             } for i,c in enumerate(["gainer","loser"])] +
                             [{'if': {'column_id': c},
                                    'color': col_colours[i],
                                    'fontWeight': 'bold'
                             } for i,c in enumerate(["gainer_perc","loser_perc"])
     ]),
    )

market_sum = ["coin","close", "open","volume"]
market_sum_col_name = ["","close", "open","volume"]

market_summary_table = dash_table.DataTable(
    id='market_summary',
    columns=[{"name" : market_sum_col_name[i],
              "id":col, 
            "type": "numeric",
            } 
            for i,col in enumerate(market_sum)],
    style_header = {'backgroundColor': '#000022',
                    'font-family': 'Helvetica',
                    'font-size':"120%",
                    'color':"#DADBFE",
                    'fontWeight': 'bold',
                    'paddingRight':75,
                    'marginTop':0,
                    'marginBottom':0,
                    'border': '0px',
                    'textAlign': 'center',
                    },
    style_table = {'width':'10px'},
    style_cell={'minWidt': 95, 
                'width': 95, 
                'maxWidth': 140,
                'font-family': 'Helvetica',
                'font-weight': 'bold',
                'backgroundColor': '#000022',
                'color': '#DADBFE',
                'textAlign': 'center'},
    style_data={ 'border': '5px solid #000022'}
    )

market_summary_icon = html.Div(id = 'market_icon')

market_summary_graph = dcc.Graph(id='market_graph', 
        style = {'display': 'inline-block', 'width': '100%'},
        figure={
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height = 250,
            width = 200
            )}
        )

def create_ohlc(df_ohlc, graph_name, time_tabs_name, coin_tab_name, stat_name):
    timestamp_dict = {  '1m':df_ohlc.index.strftime("%H:%M %d/%m/%Y"),
                        '5m':df_ohlc.index.strftime("%H:%M %d/%m/%Y"),
                        '1h':df_ohlc.index.strftime("%H:%M %d/%m/%Y"),
                        '1d':df_ohlc.index.strftime("%H:%M %d/%m/%Y")}
                
    x_data = timestamp_dict[time_tabs_name]

    if graph_name == 'Candlestick':
        fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2], vertical_spacing=0, shared_xaxes=True) 

        fig.add_trace(go.Candlestick(x=x_data,open=df_ohlc['open'], high=df_ohlc['high'], low=df_ohlc['low'], close=df_ohlc['close'],
                                increasing_line_color='#2FB835', decreasing_line_color='#FF3535', name='candlestick'), row=1, col=1)

        fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font = {'color': colors['text'],'family': "Helvetica"},
                )

    else :
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.009, horizontal_spacing=0.009, row_heights=[0.8, 0.2])

        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['close'], mode = 'lines', yaxis="y1", xaxis="x1",
            name='Close Price',
            connectgaps=True, marker = dict(color='rgb(255, 255, 0)')),row=1, col=1)

        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['open'], mode = 'lines', yaxis="y1", xaxis="x1",
            name='Open Price',
            connectgaps=True, marker = dict(color = 'rgb(0, 0, 255)')),row=1, col=1)
        
        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['high'], mode = 'lines', yaxis="y1", xaxis="x1",
            name='Highest',
            connectgaps=True, marker = dict(color='rgb(225, 0, 0)')),row=1, col=1)
        
        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['low'], mode = 'lines', yaxis="y1", xaxis="x1",
            connectgaps=True, marker = dict(color='rgb(0, 255, 0)')),row=1, col=1)

    fig.update_layout(
        yaxis=dict(
        title="USD",
        titlefont=dict(
            color="#FFFFFF"
        ),
        tickfont=dict(
            color="#FFFFFF"
        ),
        layer="above traces",
        anchor="free",
        side="left",
        position=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = {'color': colors['text'],'family': "Helvetica"},
        newshape_line_color='white')

    if 'MACD' in stat_name:
        macd_data = ta.trend.macd(df_ohlc['close'])
        fig.add_trace(go.Scatter(x = x_data, y = macd_data, mode = 'lines', yaxis="y2", xaxis="x2",
            name='MACD',
            connectgaps=True, marker = dict(color='#6FE9FF')), row=2, col=1)
        fig.update_layout(
            yaxis2=dict(
            title="MACD",
            titlefont=dict(
                color="#6FE9FF"),
            tickfont=dict(
                color="#6FE9FF"),
            layer="below traces",
            anchor="x",
            overlaying="y2",
            side="left")
            )
        

    if 'Market Volume' in stat_name:
        fig.add_trace(go.Bar(x = x_data, y = df_ohlc['volume'], yaxis="y3", xaxis="x2",
            name='Market Volume', marker = dict(color='#FF84E3')), row=2, col=1)
        fig.update_layout(
            yaxis3=dict(
            title="Market Volume",
            titlefont=dict(
                color="#FF84E3"),
            tickfont=dict(
                color="#FF84E3"),
            layer="below traces",
            anchor="x",
            overlaying="y3",
            side="right")
            )
    fig.update_xaxes(range=[1000,1200],
            showgrid=False, zeroline=False, rangeslider_visible=False,
            showspikes=True, spikemode='across', spikesnap='cursor', showline=True,
            spikecolor="rgb(10, 10, 10)",spikethickness=0.3, spikedash='solid')

    fig.update_yaxes(showspikes=True, spikedash='solid',spikemode='across', showticklabels=True,
                    spikecolor="rgb(10, 10, 10)",spikesnap="cursor",spikethickness=0.3, )

    if ('Market Volume' not in stat_name and 'MACD' not in stat_name):
        fig.update_layout(
        xaxis=dict(showticklabels=True),
        xaxis2=dict(showticklabels=False))
    else:
        fig.update_layout(
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

coin_logo_title = html.Div(html.Img(id='coin-logo-title',src=app.get_asset_url('img/BTC.png'),
        style={'height':'40px', 
                'width':'40px',}),
    style = {'height':'100%','display':'inline','paddingLeft':100 }
)

coin_name_title = html.Div(
    html.Div(children = [
        coin_logo_title, 
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
                        'display':'inline'
                        }),
        ],
        style = {'vertical-align':'middle','display':'table-cell'}
    ),
    style = {'float':'left','height': 200,'display':'table'}
)

logo = html.Img(id='logo',src=app.get_asset_url('img/logo.png'),
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
    coin_name_title, number_indicator
],style = {'display':'inline-block','width':'100%'})

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