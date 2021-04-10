import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import random
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

fig = make_subplots(rows=1, cols=2)

fig.add_trace(go.Candlestick(x=[],open=[],high=[],low=[],close=[]), row=1, col=1)
fig.add_trace(go.Candlestick(x=[],open=[],high=[],low=[],close=[]), row=1, col=2)

app.layout = html.Div([
    html.Div([

        dcc.Graph(
            id='graph-extendable',
            figure=fig
        ),
    ]),

    dcc.Interval(
        id='interval-graph-update',
        interval=1000,
        n_intervals=0),
])

@app.callback(Output('graph-extendable', 'prependData'),
              [Input('interval-graph-update', 'n_intervals')]
              )
def create_then_prepend_single_trace(n_intervals):

    return (dict(x=[np.array([n_intervals]),np.array([n_intervals])], 
            open=[np.array([-n_intervals**2]),-np.array([-n_intervals**2])],
            high=[np.array([-n_intervals**2])+2,-np.array([-n_intervals**2])+3],
            low=[np.array([-n_intervals**2])-1,-np.array([-n_intervals**2])-2],
            close=[np.array([-n_intervals**2])+1,-np.array([-n_intervals**2])],
            ),[0,1])

#@app.callback(Output('graph-extendable', 'extendData'),
#              [Input('interval-graph-update', 'n_intervals')]
#              )
#def create_then_extend_single_trace(n_intervals):
#
#    return (dict(x=[np.array([n_intervals]),np.array([n_intervals])], y=[-np.array([-n_intervals**2]),np.array([-n_intervals**2])]),[0,1])

if __name__ == '__main__':
    app.run_server(debug=True)