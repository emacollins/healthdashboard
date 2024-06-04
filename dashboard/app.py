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
    CONN_POOL.putconn(conn)
    return figures["ActiveEnergy"], figures["ExerciseMinutes"], figures["SleepHours"]


@app.callback(
    Output("SummaryCaloriesTotalCaloriesBurned", "children"),
    Output("SummaryCaloriesPowerEquivalentValue", "children"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
        Input("SummaryCaloriesPowerEquivalentDropdown", "value"),
    ],
)
def update_total_calories(start_date: str, end_date: str, comparison_object: str):
    # Calculate the total calories burned for the selected date range
    conn = get_conn()
    total_calories = summary_analytics.calculate_total_calories(
        start_date, end_date, get_username(), conn
    )

    power_equivalent_value, power_equivalent_unit = (
        summary_analytics.calculate_power_equivalent(total_calories, comparison_object)
    )
    CONN_POOL.putconn(conn)
    return (
        f"{total_calories:,}",
        f"{round(power_equivalent_value, 1):,} {power_equivalent_unit}",
    )

@app.callback(
    Output("SummaryExerciseTotalExercise", "children"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
    ],
)
def update_total_exercise(start_date: str, end_date: str):
    # Calculate the total calories burned for the selected date range
    conn = get_conn()
    total_exercise = summary_analytics.calculate_total_exercise(
        start_date, end_date, get_username(), conn
    )
    CONN_POOL.putconn(conn)
    return (
        f"{total_exercise:,}",
    )



@app.callback(
    Output("SummaryCaloriesPowerEquivalentDropdown", "options"),
    Output("SummaryCaloriesPowerEquivalentDropdown", "value"),
    Input("SummaryCaloriesPowerEquivalentDropdown", "id"),
)
def get_power_equivalent_dropdown_values(id: str):
    options = summary_analytics.get_power_equivalent_dropdown_values()
    return options, options[0]

@app.callback(
        Output("BurgersValue", "children"),
        Output("CheezeitsValue", "children"),
        [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
        ]
)
def update_food_equivalent(start_date: str, end_date: str):
    # Calculate the total calories burned for the selected date range
    conn = get_conn()
    total_calories = summary_analytics.calculate_total_calories(
        start_date, end_date, get_username(), conn
    )

    burgers, cheezeits = (
        summary_analytics.calculate_food_equivalent(total_calories)
    )
    CONN_POOL.putconn(conn)
    return (
        f"{round(burgers, 1):,}",
        f"{round(cheezeits, 1):,}",
    )

@app.callback(
        Output("SummaryFavoriteWorkoutsFigure", "figure"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
    ],
)
def update_favorite_workout(start_date: str, end_date: str):
    conn = get_conn()
    figure = summary_charts.get_favorite_workout_chart(
        start_date, end_date, get_username(), conn
    )
    CONN_POOL.putconn(conn)
    return figure

def get_conn():
    return CONN_POOL.getconn()


def get_username():
    # Placeholder function
    return "eric"


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
