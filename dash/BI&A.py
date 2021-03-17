# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 12:36:41 2021
@author: Romen Samuel Wabina
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import sample as model
import technicalanalysis 


coins = ['Bitcoin', 'Etheriumm', 'Ripple',
         'Tether', 'BTC Cash', 'BTC SV', 'Litecoin',
         'EOS', 'Binance', 'Tezos']
###################### Load Data ######################













###################### Layout ##############################
# Create the app
app = dash.Dash()
sma_fast, sma_slow = technicalanalysis.moving_averages()
colors = {'background': '#000112','text': '#DADBFE'}
avian1 = model.SIRSI_MODEL(beta0 = 0.5, beta1 = 0.5, h = 0.1, Iw = 1, T = 600, transmission = 'Periodic')
avian2 = model.SIRSI_MODEL(beta0 = 0.5, beta1 = 0.5, h = 0.1, Iw = 1, T = 1655, transmission = 'Non-Periodic')
Sd, IHd, Rd, S, I = avian1.main()
Sd2, IHd2, Rd2, S2, I2 = avian2.main()
timestamp, open, high, close, low = technicalanalysis.prices()
macd_line, signal_line = technicalanalysis.macd_signals()
momentum_rsi, momentum_stoch_rsi, momentum_stoch_rsi_k = technicalanalysis.relative_strength()
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

candlestick = go.Figure(data= [go.Candlestick(x = timestamp, 
                                              open = open, 
                                              high = high,
                                              low = low,
                                              close = close)])
candlestick.update_layout(
    title='Candlestick Chart',
    yaxis_title='AAPL Stock',
    shapes = [dict(x0 ='2017-11-09', x1 ='2017-12-09', 
                    y0 = 0, y1 = 0, 
                    xref='x',
                    yref='paper',
                    line_width = 0)])


candlestick.update_layout(paper_bgcolor = colors['background'], 
                          font = {'color': colors['text'], 'family': "Helvetica"},
                          plot_bgcolor = colors['background'])

gauge_rsi = go.Figure()
gauge_rsi.add_trace(go.Indicator(
    domain = {'x': [0, 0.5], 'y': [0, 0.5]},
    value = 450,
    mode = "gauge+number+delta",
    title = {'text': "Relative Strength Index"},
    delta = {'reference': 140},
    gauge = {'axis': {'range': [None, 110]},
             'steps' : [{'range': [0, 70], 'color': "lightgray"},
                        {'range': [70, 140], 'color': "gray"}],
             'threshold' : {'line': {'color': "darkred", 'width': 4}, 'thickness': 1, 'value': 100}}))

gauge_rsi.add_trace(go.Indicator(
    domain = {'x': [0.5, 1], 'y': [0, 0.5]},
    value = 450,
    mode = "gauge+number+delta",
    title = {'text': "Commodity Channel Index"},
    delta = {'reference': 150},
    gauge = {'axis': {'range': [None, 110]},
             'steps' : [{'range': [-100, 0], 'color': "lightgray"},
                        {'range': [0, 100], 'color': "gray"}],
             'threshold' : {'line': {'color': "darkred", 'width': 4}, 'thickness': 1, 'value': 100}}))

gauge_rsi.update_layout(paper_bgcolor = colors['background'],
                        plot_bgcolor = colors['background'],
                        font = {'color': colors['text'], 
                                'family': "Helvetica"})


num_indicator = go.Figure()
num_indicator.add_trace(go.Indicator(
    mode = "number+delta",
    value = close[2000],
    domain = {'x': [0, 0.4], 'y': [0, 0]},
    delta = {'reference': 400, 'relative': True, 'position' : "bottom"}))

num_indicator.add_trace(go.Indicator(
    mode = 'number+delta',
    value = macd_line[1],
    domain = {'x': [0.3, 0.7], 'y': [0, 0]},
    delta = {'reference': 400, 'relative': True, 'position' : "bottom"}))

num_indicator.add_trace(go.Indicator(
    mode = "number+delta",
    value = macd_line[2],
    delta = {'reference': 400, 'relative': True, 'position': 'bottom'},
    domain = {'x': [0.7, 1], 'y': [0, 0]}))

num_indicator.update_layout(paper_bgcolor = colors['background'], 
                            font = {'color': colors['text'], 
                                    'family': "Helvetica"})


num_describe = go.Figure()
num_describe.add_trace(go.Indicator(
    mode = 'number',
    domain = {'x': [0,0], 'y': [0, 0]},
    value = 200))
num_describe.update_layout(paper_bgcolor = colors['background'],
                           font = {'color': colors['text'],
                                   'family': 'Helvetica'})


app.layout = html.Div(style = {'backgroundColor': colors['background']},
                      children = [html.H2(children = 'CryptoView: A Cryptocurrency Platform using Business Intelligence',
                                          style = {'textAlign': 'center',
                                                   'color': colors['background'],
                                                   'font-family': 'Helvetica'}),
                                  
                                  html.H1(children = 'CryptoView: A Cryptocurrency Platform using Business Intelligence',
                                          style = {'textAlign': 'center',
                                                   'color': colors['text'],
                                                   'font-family': 'Helvetica',
                                                   'font-weight': 9000}),
                                  
                                  dcc.Tabs(id = 'tabs-styled-with-props', value = 'tab1',
                                           children = [dcc.Tab(label = 'Bitcoin', value = 'tab1',
                                                               children = [html.H1(children = 'Bitcoin BTC',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'display': 'inline-block',
                                                                                            'width': '30%'}),

                                                                           dcc.Graph(figure = num_indicator,
                                                                                     style = {'width': '80%',
                                                                                              'margin-left':300,
                                                                                              'display': 'block',
                                                                                              'backgroundColor': colors['background']}) 
                                                                           ]),
                                                       dcc.Tab(label = 'Ethereum', value = 'tab2',
                                                               children = [html.H1(children = 'Etherium ETH',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'width': '50%', 
                                                                                            'display': 'inline-block'}),
                                                                           html.P(children = '24hr Volume | Market Capitalization | PE | Dividend Yield',
                                                                                  style = {'textAlign': 'right',
                                                                                           'color': 'orange',
                                                                                           'font-family': 'Sans-Serif',
                                                                                           'font-size': 20,
                                                                                           'width': '40%', 'display': 'inline-block'})
                                                                           ]),
                                                       dcc.Tab(label = 'Ripple', value = 'tab3',
                                                               children = [html.H1(children = 'Ripple XRP',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'width': '50%', 
                                                                                            'display': 'inline-block'}),
                                                                           html.P(children = '24hr Volume | Market Capitalization | PE | Dividend Yield',
                                                                                  style = {'textAlign': 'right',
                                                                                           'color': 'orange',
                                                                                           'font-family': 'Sans-Serif',
                                                                                           'font-size': 20,
                                                                                           'width': '40%', 'display': 'inline-block'})
                                                                           ]),
                                                       dcc.Tab(label = 'Tether', value = 'tab4',
                                                               children = [html.H1(children = 'Tether USDT',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'width': '50%', 
                                                                                            'display': 'inline-block'}),
                                                                           html.P(children = '24hr Volume | Market Capitalization | PE | Dividend Yield',
                                                                                  style = {'textAlign': 'right',
                                                                                           'color': 'orange',
                                                                                           'font-family': 'Sans-Serif',
                                                                                           'font-size': 20,
                                                                                           'width': '40%', 'display': 'inline-block'})
                                                                           ]),
                                                       dcc.Tab(label = 'BTC Cash', value = 'tab5',
                                                               children = [html.H1(children = 'BTC Cash BCH',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'width': '50%', 
                                                                                            'display': 'inline-block'}),
                                                                           html.P(children = '24hr Volume | Market Capitalization | PE | Dividend Yield',
                                                                                  style = {'textAlign': 'right',
                                                                                           'color': 'orange',
                                                                                           'font-family': 'Sans-Serif',
                                                                                           'font-size': 20,
                                                                                           'width': '40%', 'display': 'inline-block'})
                                                                           ]),
                                                       dcc.Tab(label = 'Bitcoin SV', value = 'tab6',
                                                               children = [html.H1(children = 'Bitcoin SV BSV',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'width': '50%', 
                                                                                            'display': 'inline-block'}),
                                                                           html.P(children = '24hr Volume | Market Capitalization | PE | Dividend Yield',
                                                                                  style = {'textAlign': 'right',
                                                                                           'color': 'orange',
                                                                                           'font-family': 'Sans-Serif',
                                                                                           'font-size': 20,
                                                                                           'width': '40%', 'display': 'inline-block'})
                                                                           ]),
                                                       dcc.Tab(label = 'Litecoin', value = 'tab7',
                                                               children = [html.H1(children = 'Litecoin LTC',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'width': '50%', 
                                                                                            'display': 'inline-block'}),
                                                                           html.P(children = '24hr Volume | Market Capitalization | PE | Dividend Yield',
                                                                                  style = {'textAlign': 'right',
                                                                                           'color': 'orange',
                                                                                           'font-family': 'Sans-Serif',
                                                                                           'font-size': 20,
                                                                                           'width': '40%', 'display': 'inline-block'})
                                                                           ]),
                                                       dcc.Tab(label = 'EOS', value = 'tab8',
                                                               children = [html.H1(children = 'EOS.IO EOS',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'width': '50%', 
                                                                                            'display': 'inline-block'}),
                                                                           html.P(children = '24hr Volume | Market Capitalization | PE | Dividend Yield',
                                                                                  style = {'textAlign': 'right',
                                                                                           'color': 'orange',
                                                                                           'font-family': 'Sans-Serif',
                                                                                           'font-size': 20,
                                                                                           'width': '40%', 'display': 'inline-block'})
                                                                           ]),
                                                       dcc.Tab(label = 'Binance', value = 'tab9',
                                                               children = [html.H1(children = 'Binance BNB',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'width': '50%', 
                                                                                            'display': 'inline-block'}),
                                                                           html.P(children = '24hr Volume | Market Capitalization | PE | Dividend Yield',
                                                                                  style = {'textAlign': 'right',
                                                                                           'color': 'orange',
                                                                                           'font-family': 'Sans-Serif',
                                                                                           'font-size': 20,
                                                                                           'width': '40%', 'display': 'inline-block'})
                                                                           ]),
                                                       dcc.Tab(label = 'Tezos', value = 'tab10',
                                                               children = [html.H1(children = 'Tezos XTZ',
                                                                                   style = {'textAlign': 'left',
                                                                                            'color': colors['text'],
                                                                                            'font-family': 'Sans-Serif',
                                                                                            'font-size': 50,
                                                                                            'margin-left': 50,
                                                                                            'width': '50%', 
                                                                                            'display': 'inline-block'}),
                                                                           html.P(children = '24hr Volume | Market Capitalization | PE | Dividend Yield',
                                                                                  style = {'textAlign': 'right',
                                                                                           'color': 'orange',
                                                                                           'font-family': 'Sans-Serif',
                                                                                           'font-size': 20,
                                                                                           'width': '40%', 'display': 'inline-block'})
                                                                           ]),],
                                           colors = {
                                                   'border' : 'firebrick',
                                                   'primary': 'darkblue',
                                                   'background': 'firebrick'},
                                           style = {'color': colors['text'],
                                                    'font-family': 'Helvetica',
                                                    'font-weight': 'bold',
                                                    'marginLeft': "40px",
                                                    'marginRight': "40px"}),
                                                                  

                                  dcc.Graph(id = 'ohlc_main',
                                            figure = {'data': [{'x': timestamp[2800:2953], 'y': high[2800:2953], 'type': 'line', 'name': 'Opening Price'},
                                                               {'x': timestamp[2800:2953], 'y': close[2800:2953], 'type': 'line', 'name': 'Closing Price'},
                                                               {'x': timestamp[2800:2953], 'y': low[2800:2953], 'type': 'line', 'name': 'Lowest Price'},
                                                               {'x': timestamp[2800:2953], 'y': high[2800:2953], 'type': 'line', 'name': 'Highest Price'},
                                                               {'x': timestamp[2800:2953], 'y': sma_fast[2800:2953], 'type': 'line', 'name': 'fSMA'},
                                                               {'x': timestamp[2800:2953], 'y': sma_slow[2800:2953], 'type': 'line', 'name': 'sSMA'}],
                                                       'layout':{'plot_bgcolor': colors['background'],
                                                                 'paper_bgcolor': colors['background'],
                                                                 'font': {'color': colors['text']},
                                                                 'plot_bgcolor': colors['background']}}),
                                  

                                  
                                  dcc.Graph(figure = num_indicator,
                                             style = {'width': '50%', 'display': 'inline-block',
                                                      'backgroundColor': colors['background']}), 
                                  
                                  dcc.Graph(figure = gauge_rsi,
                                            style = {'width': '50%', 'display': 'inline-block',
                                                     'backgroundColor': colors['background']}),
                                 
                                  
                                  dcc.Graph(id = 'hist_graph1',
                                            figure = {'data': [{'y': Sd,'type': 'line', 'name':'Susceptible'},
                                                               {'y': IHd, 'type': 'line', 'name': 'Infected'},
                                                               {'y': Rd, 'type': 'line', 'name': 'Recovered'}],
                                                      'layout': {'plot_bgcolor': colors['background'],
                                                                 'paper_bgcolor': colors['background'],
                                                                 'font': {'color': colors['text']}}},
                                            style = {'width': '50%', 'display': 'inline-block'}),
                                                                   
                                  dcc.Graph(id = 'hist_graph2',
                                            figure = {'data': [{'y': Sd2, 'type': 'line', 'name': 'Susceptible'},
                                                               {'y': IHd2, 'type': 'line', 'name': 'Infected'},
                                                               {'y': Rd2, 'type': 'line', 'name': 'Recovered'}],
                                                      'layout':{'plot_bgcolor': colors['background'],
                                                                 'paper_bgcolor': colors['background'],
                                                                 'font': {'color': colors['text']},
                                                                 'plot_bgcolor': colors['background']}},
                                            
                                            style = {'width': '50%', 'display': 'inline-block'}),
                                  
                                    dcc.Graph(id = 'hist_graph3',
                                            figure = {'data': [{'x': timestamp, 'y': momentum_rsi, 'type': 'line', 'name': 'Momentum RSI'},],
                                                      'layout': {'plot_bgcolor': colors['background'],
                                                                 'paper_bgcolor': colors['background'],
                                                                 'font': {'color': colors['text']}}},
                                            style = {'width': '50%', 'display': 'inline-block'}),
                                                                   
                                  dcc.Graph(id = 'hist_graph4',
                                            figure = {'data': [{'x': timestamp, 'y': macd_line, 'type': 'line', 'name': 'MACD Line'},
                                                               {'x': timestamp, 'y': signal_line, 'type': 'line', 'name': 'Signal line'}],
                                                      'layout':{'plot_bgcolor': colors['background'],
                                                                 'paper_bgcolor': colors['background'],
                                                                 'font': {'color': colors['text']},
                                                                 'plot_bgcolor': colors['background']}},
                                            
                                            style = {'width': '50%', 'display': 'inline-block'}),
                                  
                                  dcc.Graph(id = 'ohlc',
                                            figure = {'data': [{'x': timestamp, 'y': high, 'type': 'line', 'name': 'Opening Price'},
                                                               {'x': timestamp, 'y': close, 'type': 'line', 'name': 'Closing Price'},
                                                               {'x': timestamp, 'y': low, 'type': 'line', 'name': 'Lowest Price'},
                                                               {'x': timestamp, 'y': high, 'type': 'line', 'name': 'Highest Price'}],
                                                       'layout':{'plot_bgcolor': colors['background'],
                                                                 'paper_bgcolor': colors['background'],
                                                                 'font': {'color': colors['text']},
                                                                 'plot_bgcolor': colors['background']}})
                                  ])

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# @app.callback(dash.dependencies.Output('table', 'rows'),
#               [dash.dependencies.Input('drop_value', 'value')])
# def update_info_table(drop_value):
#     if drop_value == 'coin_list':
#         new_data = df['BTC'].to_dict()
#         return new_data

#Create a function instead that automatically creates plots 

if __name__ == '__main__':
    app.run_server(debug=True)
