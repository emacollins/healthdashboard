# Import necessary libraries
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import os
from datetime import datetime as dt
from psycopg2 import pool

import charts

USERNAME = "eric"
CONN_POOL = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PW"),
    host=os.environ.get("DB_HOST"),
    port="5432",
    database=os.environ.get("DB_NAME"),
)

# Initialize your Dash app
app = dash.Dash(__name__)

# Define your Dash app layout
app.layout = html.Div(
    className="body",
    children=[
        html.H1(
            children="Health Dashboard",
            style={"color": "white", "font-family": "Arial"},
        ),
        html.Div(
            children=[
                dcc.DatePickerRange(
                    id="DateRange", start_date=dt(2022, 7, 1), end_date=dt(2024, 4, 1)
                ),
                dcc.Checklist(
                    [
                        {
                            "label": html.Div(
                                ["Apply Smoothing"], style={"color": "White", "font-size": 20}
                            ),
                            "value": True,
                        }
                    ],
                    id="Smoothing",
                    labelStyle={"display": "flex", "align-items": "center"}
                ),
            ]
        ),
        html.Div(
            children=[
                dcc.Graph(id="ActiveEnergy"),
                dcc.Graph(id="ExerciseMinutes"),
                dcc.Graph(id="StandHours"),
            ],
            style={"display": "flex"},
        ),
    ],
)


@app.callback(
    [
        dash.dependencies.Output("ActiveEnergy", "figure"),
        dash.dependencies.Output("ExerciseMinutes", "figure"),
        dash.dependencies.Output("StandHours", "figure"),
    ],
    [
        dash.dependencies.Input("DateRange", "start_date"),
        dash.dependencies.Input("DateRange", "end_date"),
        dash.dependencies.Input("Smoothing", "value"),
    ],
)
def generate_summary_charts(start_date: dt, end_date: dt, smooth: bool):
    conn = get_conn()
    figures = charts.generate_summary_charts(
        start_date, end_date, get_username(), conn, smooth
    )
    return figures["ActiveEnergy"], figures["ExerciseMinutes"], figures["StandHours"]


def get_conn():
    return CONN_POOL.getconn()


def get_username():
    # Placeholder function
    return "eric"


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
