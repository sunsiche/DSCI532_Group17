# authors: Yuanzhe Marco Ma, Sicheng Sun, Guanshu Tao, Yuan Xiong
# date: 2021-01-23
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from data_manager import DataManager
import dash_bootstrap_components as dbc
import numpy as np

# retrieve data
data = DataManager().get_data()

# land-on page graphics
table = DataManager().make_table(data)
charts = DataManager().plot_altair(data)

# app layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(
                id='placebolder-left',
                style={'height': '20vh'}
            ),
            html.Div(['Rank By:']),
            dcc.Dropdown(
                id='rankby-widget',
                value='Overall',
                options=[{'label': col, 'value': col} for col in data.columns]
            ),
            html.Br(),
            html.Div(['Order:']),
            dcc.Dropdown(
                id='order-widget',
                value='True',
                options=[{'label': 'Descending', 'value': 'False'},
                         {'label': 'Ascending', 'value': 'True'}]
            ),
            html.Br(),
            html.Div(['Continent:']),
            dcc.Dropdown(
                id='filter-cont-widget',
                value='',
                options=[{'label': val, 'value': val} for val in data['Continent'].unique()]
            ),
            html.Br(),
            html.Div(['Club:']),
            dcc.Dropdown(
                id='filter-club-widget',
                value='',
                options=[{'label': val, 'value': val} for val in data['Club'].dropna().unique()]
            )
        ], md=3),
        dbc.Col([
            html.H1('FIFA STAR BOARD', style={'width': '50vh', 'height': '10vh'}),
            html.H4(['Select Attributes:']),
            dcc.Dropdown(
                id='attribute-widget',
                value=['Name', 'Nationality', 'Age', 'Value(€)', 'Overall'],
                options=[{'label': col, 'value': col} for col in data.columns],
                multi=True
            ),
            html.Iframe(
                id='table',
                srcDoc=table.to_html(index=False),
                style={'border-width': '0', 'width': '100%', 'height': '500px'}
            ),
        ]),
        dbc.Col([
            html.Div(
                id='placebolder-right',
                style={'height': '10vh'}
            ),
            html.Div(['Top 10 by Club and by Nationality']),
            html.Iframe(
                id='charts',
                srcDoc=charts.to_html(),
                style={'border-width': '0', 'width': '150%', 'height': '700px'}
            ),
        ], md=3)
    ])
])

# updates table from all 5 dropdowns
@app.callback(
    Output('table', 'srcDoc'),
    Input('rankby-widget', 'value'),
    Input('order-widget', 'value'),
    Input('attribute-widget', 'value'),
    Input('filter-cont-widget', 'value'),
    Input('filter-club-widget', 'value'))
def update_table(by, order, cols, filter_cont, filter_club):
    table = DataManager().update_table(data, by, order == 'True',
                                       cols, filter_cont, filter_club)
    return table.to_html(index=False)

# updates charts with Rank-by selection 
# updates only when selected col is numeric
@app.callback(
    Output('charts', 'srcDoc'),
    Input('rankby-widget', 'value'))
def update_charts(by):
    global charts
    if not (np.issubdtype(data[by], int) or
            np.issubdtype(data[by], float)):
        return charts
    else:
        charts = DataManager().plot_altair(data, by=by).to_html()
        return charts


if __name__ == '__main__':
    app.run_server(debug=True)
