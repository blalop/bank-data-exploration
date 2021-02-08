import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly.express as px

from accountman.calculator import Calculator


def plot(calc: Calculator) -> html.Div:
    return html.Div(id='graphics', children=[

        html.H1(children='BBVA bank report'),

        html.H3(children='''
            Balance evolution
        '''),

        html.Button('Update', id='update-button'),

        dcc.Graph(
            id='balance',
            figure=px.line(calc.movements,
                           x='date',
                           y='balance',
                           title='Overall balance')
        ),

        dcc.Graph(
            id='pay-balance',
            figure=px.line(calc.salary_movements(),
                           x='date',
                           y='balance',
                           title='Balance at pay moment')
            .update_traces(mode='markers+lines')
        ),

        html.H3(children='''
            Spending vs incoming
        '''),

        dcc.Graph(
            id='combined-by-month',
            figure=px.bar(calc.combined_by_month(),
                          title='Spending vs incoming by month')
        ),

        dcc.Graph(
            id='diff-by-month',
            figure=px.bar(calc.diff_by_month(),
                          title='Diff by month')
        ),

        dcc.Graph(
            id='combined-by-concept',
            figure=px.bar(calc.combined_by_concept(),
                          title='Spending vs incoming by concept')
        ),

        html.H3(children='''
            Spending
        '''),

        dcc.Graph(
            id='spending-boxplot',
            figure=px.box(calc.spending_abs(),
                          y='amount',
                          title='Spending boxplot')
        ),

        html.Div(id='spending-biggest-div', style= {'textAlign': 'center'}, children=[
            html.Label('Biggest spendings'),
            dcc.Input(id='spending-biggest-input', type='number', placeholder='Value of the spending'),
            dt.DataTable(
                id='spending-biggest-tab',
                columns=[{'name': i, 'id': i} for i in calc.spending_biggest().columns],
                style_cell={'textAlign': 'left'},
                style_table={'textAlign': 'center', 'overflowY': 'auto', 'height': '300px'},
            )
        ]),

        dcc.Graph(
            id='spending-by-concept',
            figure=px.bar(calc.spending_by_concept_sorted(),
                          title='Spending by concept')
        ),


    ])
