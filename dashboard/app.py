# Import necessary libraries
import dash
from dash import html, dcc
import pandas as pd
import os
from datetime import datetime as dt
from psycopg2 import pool

import charts
import sections as s

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
    children=[
        s.MAIN_HEADER,
        s.SETTINGS_BAR,
        s.TABS,
    ],
)


@app.callback(
    [
        dash.dependencies.Output("SummaryCaloriesFigure", "figure"),
        dash.dependencies.Output("SummaryExerciseFigure", "figure"),
        dash.dependencies.Output("SummarySleepFigure", "figure"),
    ],
    [
        dash.dependencies.Input("DateRange", "start_date"),
        dash.dependencies.Input("DateRange", "end_date"),
    ],
)
def generate_summary_rolling_figures(start_date: dt, end_date: dt):
    conn = get_conn()
    figures = charts.generate_summary_charts(
        start_date, end_date, get_username(), conn
    )
    return figures["ActiveEnergy"], figures["ExerciseMinutes"], figures["SleepHours"]


def get_conn():
    return CONN_POOL.getconn()


def get_username():
    # Placeholder function
    return "eric"


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
