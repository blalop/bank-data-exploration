import plotly.express as px

import accountman.calculator as calc


def balance_fig():
    return px.line(calc.movements(), x='date', y='balance', title='Overall balance')


def payroll_fig():
    return px.line(calc.payroll_movements(),
                   x='date',
                   y='balance',
                   title='Balance at pay moment')\
        .update_traces(mode='markers+lines')


def spending_incoming_by_month_fig():
    return px.bar(calc.spending_incoming_by_month(), title='Spending vs incoming by month')


def diff_by_month_fig():
    return px.bar(calc.diff_by_month(), title='Diff by month')


def spending_incoming_by_concept_fig():
    return px.bar(calc.spending_incoming_by_concept(), title='Spending vs incoming by concept')


def spending_boxplot():
    return px.box(calc.spending_abs(), title='Spending boxplot')


def spending_by_concept_fig():
    return px.bar(calc.spending_by_concept(), title='Spending by concept')
