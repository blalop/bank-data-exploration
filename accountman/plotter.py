import plotly.express as px


def balance_fig(calc):
    return px.line(calc.movements, x='date', y='balance', title='Overall balance')


def salary_fig(calc):
    return px.line(calc.salary_movements(),
                   x='date',
                   y='balance',
                   title='Balance at pay moment')\
        .update_traces(mode='markers+lines')


def combined_by_month_fig(calc):
    return px.bar(calc.combined_by_month(), title='Spending vs incoming by month')


def diff_by_month_fig(calc):
    return px.bar(calc.diff_by_month(), title='Diff by month')


def combined_by_concept_fig(calc):
    return px.bar(calc.combined_by_concept(), title='Spending vs incoming by concept')


def spending_boxplot(calc):
    return px.box(calc.spending_abs(), title='Spending boxplot')


def spending_by_concept_fig(calc):
    return px.bar(calc.spending_by_concept(), title='Spending by concept')
