
import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
from flask import Flask

import accountman.plotter as plotter

server = Flask(__name__)

app = Dash(__name__,
           server=server,
           external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div(children=[
    html.H1(children='BBVA bank report'),

    html.H3(children='''
        Balance evolution
    '''),

    dcc.Graph(
        id='balance',
        figure=plotter.balance_fig()
    ),

    dcc.Graph(
        id='pay_balance',
        figure=plotter.payroll_fig()
    ),

    html.H3(children='''
        Spending vs incoming
    '''),

    dcc.Graph(
        id='spending_incoming_by_month',
        figure=plotter.spending_incoming_by_month_fig()
    ),

    dcc.Graph(
        id='diff_by_month',
        figure=plotter.diff_by_month_fig()
    ),

    dcc.Graph(
        id='spending_incoming_by_concept',
        figure=plotter.spending_incoming_by_concept_fig()
    ),

    html.H3(children='''
        Spending
    '''),

    dcc.Graph(
        id='spending_boxplot',
        figure=plotter.spending_boxplot()
    ),

    dcc.Graph(
        id='spending_by_concept',
        figure=plotter.spending_by_concept_fig()
    ),

])


@server.route('/health')
def alive():
    return "YES", 200
