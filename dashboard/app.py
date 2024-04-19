# Import necessary libraries
import os
from datetime import datetime as dt

import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
from psycopg2 import pool

import sections as s
import tabs.summary.charts as summary_charts
import tabs.summary.analytics as summary_analytics

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
SUMMARY_DATA = None

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
        Output("SummaryCaloriesFigure", "figure"),
        Output("SummaryExerciseFigure", "figure"),
        Output("SummarySleepFigure", "figure"),
    ],
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
    ],
)
def generate_summary_rolling_figures(start_date: str, end_date: str):
    conn = get_conn()
    figures = summary_charts.generate_summary_charts(
        start_date, end_date, get_username(), conn
    )
    return figures["ActiveEnergy"], figures["ExerciseMinutes"], figures["SleepHours"]


@app.callback(
    Output("SummaryCaloriesTotalCaloriesBurned", "children"),
    Output("SummaryCaloriesPowerEquivalentValue", "children"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
        Input("SummaryCaloriesPowerEquivalentDropdown", "value")
    ],
)
def update_total_calories(start_date: str, end_date: str, comparison_object: str):
    # Calculate the total calories burned for the selected date range
    conn = get_conn()
    total_calories = summary_analytics.calculate_total_calories(start_date, end_date, get_username(), conn)

    power_equivalent_value = summary_analytics.calculate_power_equivalent(total_calories, comparison_object)

    return f"{total_calories:,}", f"{power_equivalent_value:,} minutes"


def get_conn():
    return CONN_POOL.getconn()


def get_username():
    # Placeholder function
    return "eric"


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
