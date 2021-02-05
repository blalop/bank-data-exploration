import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
from flask import Flask

from accountman.calculator import Calculator
import accountman.plotter as plotter


server = Flask(__name__)

app = Dash(__name__,
           server=server,
           external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

calc = Calculator('bbva_reports')

app.layout = html.Div(children=[
    html.H1(children='BBVA bank report'),

    html.H3(children='''
        Balance evolution
    '''),

    dcc.Graph(
        id='balance',
        figure=plotter.balance_fig(calc)
    ),

    dcc.Graph(
        id='pay_balance',
        figure=plotter.salary_fig(calc)
    ),

    html.H3(children='''
        Spending vs incoming
    '''),

    dcc.Graph(
        id='combined_by_month',
        figure=plotter.combined_by_month_fig(calc)
    ),

    dcc.Graph(
        id='diff_by_month',
        figure=plotter.diff_by_month_fig(calc)
    ),

    dcc.Graph(
        id='combined_by_concept',
        figure=plotter.combined_by_concept_fig(calc)
    ),

    html.H3(children='''
        Spending
    '''),

    dcc.Graph(
        id='spending_boxplot',
        figure=plotter.spending_boxplot(calc)
    ),

    dcc.Graph(
        id='spending_by_concept',
        figure=plotter.spending_by_concept_fig(calc)
    ),

])


@server.route('/health')
def health():
    return "YES", 200
