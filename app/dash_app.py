import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from app import app
from flask import url_for
import os

THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

df = pd.read_csv(os.path.join(THIS_FOLDER, "data/brickset_data.csv"))
df = df[df.num_parts>10]
df = df[df.theme!="Duplo"]
df = df[df.theme!="Action Wheelers"]
df = df[df.theme!="Education"]
df = df[df.theme!="Dacta"]
df = df[df.theme!="Explore"]
df = df[df.theme!="Mindstorms"]
df = df[df.theme!="Quatro"]
df = df[df.set_type=="Normal"]

themes = ['Star Wars', 'City', 'Town', 'Creator', 'Harry Potter', 'Technic', 'Friends',
          'Basic', 'Castle', 'Ninjago', 'Legends of Chima', 'Marvel Super Heroes', 'Pirates']
features = {'year': 'Year of release', 'price': 'Price', 'num_parts': 'Number of parts', 'ppp': 'Price per part'}

def hex_to_rgb(value):
    """Return 'rgb(red, green, blue)' for the color given as '#rrggbb'."""
    value = value.lstrip('#')
    lv = len(value)
    return 'rgb'+str(tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))

colors_hexa = ['#1f77b4',
               '#aec7e8',
               '#ff7f0e',
               '#ffbb78',
               '#2ca02c',
               '#98df8a',
               '#d62728',
               '#ff9896',
               '#9467bd',
               '#c5b0d5',
               '#8c564b',
               '#c49c94',
               '#e377c2']

colors = [hex_to_rgb(col) for col in colors_hexa]
color_discrete_map = dict(zip(themes, colors))


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("github", href="https://github.com/otwtm/lego"))
    ],
    sticky="top",
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("LEGO Analysis"),
                        html.P([
                            """\
This is a little application that lets you visually analyse sets of your favourite Lego themes.

It is built in """, html.A("Plotly Dash", href='https://dash.plot.ly/?_ga=2.191284771.880077638.1578565166-700802424.1578306855', target='_blank'),  """ which is an open-source Python and R framework for building web-based analytic applications.

The application uses data from """, html.A("Brickset.com", href='https://brickset.com/', target='_blank'), """.

You can find the source code in my github account: """, html.A("https://github.com/otwtm/lego", href='https://github.com/otwtm/lego', target='_blank'),""".

"""]
                        ),
                        #dbc.Button("View details", color="secondary"),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.Label(children='Select LEGO themes'),
                        dcc.Dropdown(id='select_theme',
                                     options=[{'label': theme, 'value': theme}
                                              for theme in themes],
                                     value=[],
                                     multi=True
                                     ),
                        html.Br(),
                        html.Label(children='Select x-axis'),
                        dcc.Dropdown(id='select_xaxis_feature',
                                     options=[{'label': features[feat], 'value': feat}
                                              for feat in features],
                                     value='year',
                                     multi=False
                                     ),
                        html.Br(),
                        html.Label(children='Select y-axis'),
                        dcc.Dropdown(id='select_yaxis_feature',
                                     options=[{'label': features[feat], 'value': feat}
                                              for feat in features],
                                     value='price',
                                     multi=False
                                     ),
                        html.Br(),
                        html.Div(id='graph')
                    ]
                ),
            ]
        )
    ],
    className="mt-4",
)


dash_app.layout = html.Div([navbar, body])



@dash_app.callback(
    Output(component_id='graph', component_property='children'),
    [Input(component_id='select_theme', component_property='value'),
     Input(component_id='select_xaxis_feature', component_property='value'),
     Input(component_id='select_yaxis_feature', component_property='value')]
)
def update_value(theme_input_data, xaxis_feature, yaxis_feature):
    dat = df[df.theme.isin(theme_input_data)]
    figure = px.scatter(dat, x=dat[xaxis_feature], y=dat[yaxis_feature], color='theme', size='num_parts', opacity=0.7,
                        hover_name="set_name", hover_data=["set_num"], color_discrete_map=color_discrete_map)


    figure.for_each_trace(
        lambda trace: trace.update(name=trace.name.replace("theme=", "")),
    )
    figure.update_layout(
        xaxis_title=features[xaxis_feature],
        yaxis_title=features[yaxis_feature]
    )
    figure.update_layout(
        legend=go.layout.Legend(
            x=0,
            y=-0.2,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            borderwidth=0,
            orientation="h"
        ),
        height = 600
    )

    graph = dcc.Graph(
        id='lego-graph',
        figure=figure
    )

    graphs = [graph]
    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)

