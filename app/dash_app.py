import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from app import app


dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

df = pd.read_csv("data/brickset_data.csv")
df = df[df.num_parts>10]
df = df[df.theme!="Duplo"]
df = df[df.theme!="Action Wheelers"]
df = df[df.theme!="Education"]
df = df[df.theme!="Dacta"]
df = df[df.theme!="Explore"]
df = df[df.theme!="Mindstorms"]
df = df[df.theme!="Quatro"]
df = df[df.set_type=="Normal"]

themes = ['Star Wars', 'City', 'System', 'Creator', 'Harry Potter', 'Technic', 'Friends',
          'Basic', 'Castle', 'Ninjago', 'Legends of Chima', 'Marvel Super Heroes', 'Pirates']
features = {'year': 'Year of release', 'price': 'Price', 'num_parts': 'Number of parts', 'ppp': 'Price per part'}

ppp = df.groupby(['year', 'theme'],  as_index=False).agg({'ppp': 'mean'})

print(df.head())



navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    brand="Demo",
    brand_href="#",
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
sdfsdfdfsdf

"""]
                        ),
                        dbc.Button("View details", color="secondary"),
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
    """
    figure = go.Figure()
    for theme in theme_input_data:
        figure.add_trace(go.Scatter(x=dat[dat.theme==theme][xaxis_feature], y=dat[dat.theme==theme][yaxis_feature],
                                 mode='markers'))
    """    
    figure = px.scatter(dat, x=dat[xaxis_feature], y=dat[yaxis_feature], color='theme', size='num_parts', opacity=0.5,
                        hover_name="set_name", hover_data=["set_num"])


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
            y=-0.3,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            borderwidth=0,
            orientation="h"
        )
    )

    graph = dcc.Graph(
        id='lego-graph',
        figure=figure
    )

    graphs = [graph]
    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)

