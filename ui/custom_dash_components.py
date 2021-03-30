import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import data_handler
from datetime import datetime
import ta

coins = ['Bitcoin','Ethereum', "Ripple", "Dogecoin", 'Tezos','Litecoin','EOS','Binance', 'BTC Cash']
symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "XTZUSDT", "LTCUSDT", "EOSUSDT", "BNBUSDT", "BCHUSDT"]
timeframes = ['1m','5m','1h', '1d']
plot_type = ['Line Plot','Candlestick']

colors = {'background': '#000022','text': '#DADBFE'}

title = html.H1(children = 'CryptoView', 
                style = {'textAlign': 'left', 
                        'color': colors['text'], 
                        'font-family': 'Helvetica', 
                        'font-size': '76px',
                        'font-weight': 9000,
                        'paddingTop':10,
                        'paddingBottom':20,
                        'paddingLeft':30,
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
        style = {'display': 'inline-block'},
        figure={
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height = 300)})

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
        delta = {'reference': previous_data['close'], 'relative': True, 'position' : "bottom"}))
    
    fig.add_trace(go.Indicator(
        title = 'Volume',
        mode = "number+delta",
        value = current_data['volume'],
        domain = {'x': [0.5, 1.0], 'y': [0, 0]},
        delta = {'reference': previous_data['volume'], 'relative': True, 'position' : "bottom"}))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = {'color': colors['text'],'family': "Helvetica"})
    return fig

minute_interval = dcc.Interval(
        id='interval-component',
        interval=60*1000,
        n_intervals=0
    )
    
ohlc_graph = dcc.Graph(id='ohlc', 
        style = {'display': 'inline-block', 'width': '100%'},
        figure={
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height = 1000,
            width = 1500)})

time_tabs_styles = {
                'borderLeft': '3px solid #000000',
                'width': '150px',
                'height': '50px'
            }

time_tab_selected_style = {
                'borderLeft': '3px solid #000000',
                'width': '150px',
                'height': '50px'
            }

timeframe_tabs = dcc.Tabs(id = 'time_tabs', value = timeframes[0],
        children = [dcc.Tab(label=time, value=time, style = time_tabs_styles, selected_style=time_tab_selected_style) for time in timeframes],
        colors = {
                'border' : 'firebrick',
                'primary': 'darkblue',
                'background': 'firebrick'},
        style = {'color': colors['text'],
                'font-family': 'Helvetica',
                'font-size':"150%",
                'marginTop':"0px",
                'paddingLeft': "0px",
                'paddingRight': "0px",
                'text-align': 'center',
                'height': '50px',
                'display': 'inline-block', 'vertical-align': 'top'})

graph_tabs_styles = {
                'borderLeft': '3px solid #000000',
                'borderTop': '3px solid #000000',
                'width': '300px',
                'height': '50px'
            }

graph_tab_selected_style = {
                'borderLeft': '3px solid #000000',
                'borderTop': '3px solid #000000',
                'width': '300px',
                'height': '50px'
            }

graph_tabs = dcc.Tabs(id = 'graph_tab', value = 'Candlestick',
        children = [dcc.Tab(label=atype, value=atype, style = graph_tabs_styles, selected_style=graph_tab_selected_style) for atype in plot_type],
        colors = {
                'border' : 'firebrick',
                'primary': 'darkblue',
                'background': 'firebrick'},
        style = {'color': colors['text'],
                'font-family': 'Helvetica',
                'font-size':"150%",
                'marginTop':"0px",
                'paddingLeft': "0px",
                'paddingRight': "0px",
                'text-align': 'center',
                'height': '50px',
                'display': 'inline-block', 'vertical-align': 'top'
                })

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
                "horizontalAlign": "center"})


def create_ohlc(df_ohlc, graph_name, time_tabs_name, coin_tab_name, stat_name):
    timestamp_dict = {  '1m': df_ohlc.index.strftime("%H:%M"),
                        '5m':df_ohlc.index.strftime("%H:%M"),
                        '1h':df_ohlc.index.strftime("%H:%M %d/%m/%Y"),
                        '1d':df_ohlc.index.strftime("%d/%m/%Y")}
                
    x_data = timestamp_dict[time_tabs_name]

    if graph_name == 'Candlestick':
        fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2], vertical_spacing=0) 

        fig.add_trace(go.Candlestick(x=x_data,open=df_ohlc['open'], high=df_ohlc['high'], low=df_ohlc['low'], close=df_ohlc['close'],
                                increasing_line_color='#2FB835', decreasing_line_color='#FF3535', name='candlestick'), row=1, col=1)

        fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font = {'color': colors['text'],'family': "Helvetica"},
                )

    else :
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009, row_heights=[0.7, 0.3])

        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['close'], mode = 'lines',
            name='Close Price',
            connectgaps=True, marker = dict(color='rgb(255, 255, 0)')),row=1, col=1)

        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['open'], mode = 'lines',
            name='Open Price',
            connectgaps=True, marker = dict(color = 'rgb(0, 0, 255)')),row=1, col=1)
        
        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['high'], mode = 'lines',
            name='Highest',
            connectgaps=True, marker = dict(color='rgb(225, 0, 0)')),row=1, col=1)
        
        fig.add_trace(go.Scatter(x = x_data, y = df_ohlc['low'], mode = 'lines',
            connectgaps=True, marker = dict(color='rgb(0, 255, 0)')),row=1, col=1)

        fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font = {'color': colors['text'],'family': "Helvetica"},
                )

    if 'MACD' in stat_name:
        macd_data = ta.trend.macd(df_ohlc['close'])
        fig.add_trace(go.Scatter(x = x_data, y = macd_data, mode = 'lines',
            name='MACD',
            connectgaps=True, marker = dict(color='#6FE9FF')), row=2, col=1)

    if 'Market Volume' in stat_name:
        fig.add_trace(go.Bar(x = x_data, y = df_ohlc['volume'],
            name='Market Volume', marker = dict(color='#FF84E3')), row=2, col=1)
    
    fig.update_xaxes(showgrid=False, zeroline=False, rangeslider_visible=False, showticklabels=True,
                showspikes=True, spikemode='across', spikesnap='cursor', showline=False,
                spikecolor="rgb(10, 10, 10)",spikethickness=0.3, spikedash='solid')

    fig.update_yaxes(showspikes=True, spikedash='solid',spikemode='across', 
                    spikecolor="rgb(10, 10, 10)",spikesnap="cursor",spikethickness=0.3)

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest',
        font = {'color': colors['text'],'family': "Helvetica"},
)
    return fig

storage_component = html.Div(id='intermediate-value', style={'display': 'none'}) 
