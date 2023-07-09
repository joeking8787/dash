import dash
from dash import dcc, html
from dash_table import DataTable
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("My Dashboard"),
                        html.Hr(),
                        dbc.Form(
                            [
                                dbc.Form(
                                    [
                                        dbc.Label("Time"),
                                        dcc.Input(id="input-months", type="number", placeholder="Months"),
                                    ],
                                ),
                                dbc.Form(
                                    [
                                        dbc.Label("Income"),
                                        dcc.Input(id="input-income", type="number", placeholder="Income"),
                                    ],
                                ),
                                dbc.Form(id="expenses-form"),
                                dbc.Button("Hide Input Panel", id="toggle-input-panel", n_clicks=0, className="btn btn-primary btn-sm mt-3"),
                                dbc.Button(
                                    "Show Input Panel",
                                    id="show-input-panel",
                                    n_clicks=0,
                                    className="btn btn-primary btn-sm mt-3",
                                    style={"display": "none"},
                                ),
                            ]
                        ),
                    ],
                    width=4,
                    className="bg-light p-4",
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Expense and Income Chart"),
                                dbc.CardBody(dcc.Graph(id="example-graph", figure={})),
                            ],
                            className="mb-4",
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Net Savings Chart"),
                                dbc.CardBody(dcc.Graph(id="savings-graph", figure={})),
                            ],
                        ),
                    ],
                    width=8,
                ),
            ],
            className="mt-4",
        ),
    ],
)

@app.callback(
    Output("toggle-input-panel", "style"),
    Output("show-input-panel", "style"),
    [Input("toggle-input-panel", "n_clicks"), Input("show-input-panel", "n_clicks")],
    [State("toggle-input-panel", "style"), State("show-input-panel", "style")]
)
def toggle_input_panel(n_clicks_hide, n_clicks_show, toggle_style, show_style):
    if n_clicks_hide % 2 == 1:
        toggle_style["display"] = "none"
        show_style["display"] = "block"
    else:
        toggle_style["display"] = "block"
        show_style["display"] = "none"
    return toggle_style, show_style

@app.callback(
    Output("expenses-form", "children"),
    Input("input-months", "value")
)
def generate_expenses_form(months):
    form_groups = []
    for i in range(months):
        form_group = dbc.Form(
            [
                dbc.FormGroup(
                    [
                        dbc.Label(f"Month {i+1} Expense"),
                        dcc.Input(id=f"input-expense-{i}", type="number", placeholder="Expense"),
                    ],
                )
            ]
        )
        form_groups.append(form_group)

    return form_groups

@app.callback(
    Output("example-graph", "figure"),
    Output("savings-graph", "figure"),
    [Input("input-months", "value"), Input("input-income", "value")],
    [State(f"input-expense-{i}", "value") for i in range(12)]
)
def update_graph(months, income, *expenses):
    if months is None or income is None:
        return {}, {}

    expense_values = [expense for expense in expenses if expense is not None]

    expense_data = {'x': list(range(1, months+1)), 'y': expense_values, 'type': 'bar', 'name': 'Expenses'}
    income_data = {'x': list(range(1, months+1)), 'y': [income] * months, 'type': 'bar', 'name': 'Income'}

    savings_values = [income - sum(expense_values)] * months
    savings_data = {'x': list(range(1, months+1)), 'y': savings_values, 'type': 'bar', 'name': 'Net Savings'}

    figure = {
        'data': [expense_data, income_data],
        'layout': {
            'title': 'Expense and Income Dashboard',
            'xaxis': {'title': 'Months'},
            'yaxis': {'title': 'Amount'},
            'barmode': 'stack'
        }
    }

    savings_figure = {
        'data': [savings_data],
        'layout': {
            'title': 'Net Savings Dashboard',
            'xaxis': {'title': 'Months'},
            'yaxis': {'title': 'Net Savings'},
        }
    }

    return figure, savings_figure


if __name__ == "__main__":
    app.run_server(port=8888)
