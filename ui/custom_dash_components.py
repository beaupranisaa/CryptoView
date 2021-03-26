import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from plotly.subplots import make_subplots

coins = ['Bitcoin','Ethereum', "Ripple", "Dogecoin", 'Tezos','Litecoin','EOS','Binance', 'BTC Cash']
symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "XTZUSDT", "LTCUSDT", "EOSUSDT", "BNBUSDT", "BCHUSDT"]

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

storage_component = html.Div(id='intermediate-value', style={'display': 'none'}) 
