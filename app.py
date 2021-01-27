import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__)

# dataset heart_failure_records
df_HF = pd.read_csv("heart_failure_clinical_records_dataset.csv")
# Create Count field in df_HF
df_HF["Count"] = [1]*len(df_HF)

# turn anamemia in to a series of catagorical data.
S_HF = pd.Series(df_HF["anaemia"].astype('category'))
# Change the catagories into negative and positive
S_HF = S_HF.cat.rename_categories(["Negative", "Positive"])
# insert it into df_HF
df_HF["anaemia"] = S_HF

# turn sex in to a series of catagorical data.
S_HF = pd.Series(df_HF["sex"].astype('category'))
# Change the catagories into negative and positive
S_HF = S_HF.cat.rename_categories(["Female", "Male"])
# insert it into df_HF
df_HF["sex"] = S_HF

# turn diabetes in to a series of catagorical data.
S_HF = pd.Series(df_HF["diabetes"].astype('category'))
# Change the catagories into negative and positive
S_HF = S_HF.cat.rename_categories(["Negative", "Positive"])
# Change the order of the categories.
S_HF = S_HF.cat.reorder_categories(["Positive", "Negative"])
# insert it into df_HF
df_HF["diabetes"] = S_HF

# turn deth in to a series of catagorical data to make the bar chart.
S_HF = pd.Series(df_HF["DEATH_EVENT"].astype('category'))
# Change the catagories into negative and positive
S_HF = S_HF.cat.rename_categories(["Alive", "Dead"])
# insert it into df_HF
df_HF["DEATH_EVENT"] = S_HF

# turn diabetes in to a series of catagorical data.
S_HF = pd.Series(df_HF["smoking"].astype('category'))
# Change the catagories into negative and positive
S_HF = S_HF.cat.rename_categories(["Non-smoking", "Smoking"])
# Change the order of the categories.
S_HF = S_HF.cat.reorder_categories(["Smoking", "Non-smoking"])
# insert it into df_HF
df_HF["smoking"] = S_HF

# remame columns
df_HF = df_HF.rename(columns={"age": "Age", "anaemia": "Anaemia", "diabetes": "Diabetes", "platelets": "Platelets", "serum_creatinine": "Serum Creatinine",
                              "serum_sodium": "Serum Sodium", "sex": "Sex", "smoking": "Smoking", "DEATH_EVENT": "Death Event", "Count": "Count"})


# Navigation Bar
navbar = html.Div(children=[html.Nav(className="nav justify-content-center bg-dark text-light", children=[
    html.H1(children=["Welcome to the dashboard - Group C"])
]), html.Nav(className="nav justify-content-center bg-dark text-light", children=[
    html.H2(children=["Heart Failure Clinical Records"])
])
])


Navigation_bar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(dbc.NavbarBrand(
                    "Variable:", className="ml-2")),
            ],
            align="center",
            no_gutters=True,
        ),
        dbc.NavbarToggler(
            id="navbar-toggler"),
        dbc.Collapse(
            dbc.InputGroup(
                [
                    dbc.Select(
                        options=[
                            {'label': 'Sex',
                             'value': 'Sex'},
                            {'label': 'Diabetes',
                             'value': 'Diabetes'},
                            {'label': 'Age',
                             'value': 'Age'},
                            {'label': 'Anaemia',
                             'value': 'Anaemia'},
                            {'label': 'Platelets',
                             'value': 'Platelets'},
                            {'label': 'Serum Creatinine',
                             'value': 'Serum Creatinine'},
                            {'label': 'Serum Sodium',
                             'value': 'Serum Sodium'},
                            {'label': 'Smoking',
                             'value': 'Smoking'},
                            {'label': 'Death Event',
                             'value': 'Death Event'}

                        ],
                        value='Sex', id='select',
                    ),


                ]
            ), id="navbar-collapse", navbar=True, className="col-4"),
    ],
    color="dark",
    dark=True,

)


app.layout = html.Div(className="container-fluid",
                      children=[navbar, Navigation_bar, html.Br(), html.Div(className="row",
                                                                            children=[html.Div(className="col-sm-6",
                                                                                               children=[html.Div(className="card text-white bg-dark mb-3", children=[html.Div(className="card-body", children=[html.H3(className="card-title text-center", children=["Univariate Analysis"]), dcc.Graph(
                                                                                                   id='example-graph1',
                                                                                               )])])]),
                                                                                      html.Div(className="col-sm-6", id="hide",
                                                                                               children=[html.Div(className="card text-white bg-dark mb-3", children=[html.H3(className="card-title text-center", children=["Bivariate Analysis"]), html.Div(className="card-body", children=[dcc.Graph(
                                                                                                   id='example-graph2',
                                                                                               )])])])
                                                                                      ]
                                                                            )

                                ]
                      )


@ app.callback(
    Output('example-graph1', 'figure'),
    Output('example-graph2', 'figure'),
    Input('select', 'value'))
def update_figure(Val):
    uni = px.bar()
    bi = px.bar()
    if Val == "Death Event":
        uni = px.pie(data_frame=df_HF.groupby(
            [Val]).count().reset_index(), names=Val, values="Count", title=f"Pie chart of {Val}")
    elif type(df_HF[Val][0]) == type("str"):
        uni, bi = px.pie(data_frame=df_HF.groupby(
            [Val]).count().reset_index(), names=Val, values="Count", title=f"Pie chart of {Val}"), px.bar(df_HF.groupby([Val, "Death Event"]).count(
            ).reset_index(), x=Val, y="Count", color="Death Event", title=f"Bar chart of {Val} vs deth")
    else:
        uni, bi = px.histogram(
            df_HF, x=Val, title=f"Histogram of {Val}"), px.box(
            df_HF, x="Death Event", y=Val, title=f"Box plot of {Val}")
    uni.update_layout(
        font_color="rgb(255, 255, 255)", paper_bgcolor='rgb(43, 63, 82)', plot_bgcolor='rgb(43, 63, 82)')
    bi.update_layout(
        font_color="rgb(255, 255, 255)", paper_bgcolor='rgb(43, 63, 82)', plot_bgcolor='rgb(43, 63, 82)')
    return uni, bi


@ app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
