import dash
import flask

from accountman.calculator import Calculator
import accountman.plotter as plotter


server = flask.Flask(__name__)

app = dash.Dash(__name__,
                server=server,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', 'stylesheet.css'])

calc = Calculator('bbva_reports')

app.layout = plotter.plot(calc)


@server.route('/health')
def health():
    return 'YES', 200


@app.callback(dash.dependencies.Output('graphics', 'children'),
              dash.dependencies.Input('update-button', 'n_clicks'))
def display_page(n):
    calc.update_movements()
    return plotter.plot(calc)

@app.callback(dash.dependencies.Output('spending-biggest-tab', 'data'),
              dash.dependencies.Input('spending-biggest-input', 'value'))
def update_output(input):
    return calc.spending_biggest(input).to_dict('records')
