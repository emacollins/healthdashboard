# Import necessary libraries
import os

import dash
from dash import html
from dash.dependencies import Input, Output, State
from psycopg2 import pool
from pathlib import Path
import base64

import sections
import sql
import utils

import tabs.summary.charts as summary_charts
import tabs.summary.analytics as summary_analytics

import etl.extract.run as extract
import etl.transform.run as transform
import etl.load.run as load


ETL_DATA_DIRECTORY = Path().cwd() / "etl" / "data"

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
        sections.MAIN_HEADER,
        sections.SETTINGS_BAR,
        sections.TABS,
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
        Input("UserSelectDropdown", "value"),
    ],
)
def generate_summary_rolling_figures(start_date: str, end_date: str, user: str):
    conn = get_conn()
    figures = summary_charts.generate_summary_charts(start_date, end_date, user, conn)
    CONN_POOL.putconn(conn)
    return figures["ActiveEnergy"], figures["ExerciseMinutes"], figures["SleepHours"]


@app.callback(
    Output("SummaryExerciseTotalExercise", "children"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
        Input("UserSelectDropdown", "value"),
    ],
)
def update_total_exercise(start_date: str, end_date: str, user: str):
    # Calculate the total calories burned for the selected date range
    conn = get_conn()
    total_exercise = summary_analytics.calculate_total_exercise(
        start_date, end_date, user, conn
    )
    CONN_POOL.putconn(conn)
    return (f"{total_exercise:,}",)


@app.callback(
    Output("SummaryAvgSleep", "children"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
        Input("UserSelectDropdown", "value"),
    ],
)
def update_total_exercise(start_date: str, end_date: str, user: str):
    # Calculate the total calories burned for the selected date range
    conn = get_conn()
    avg_sleep = summary_analytics.calculate_average_sleep(
        start_date, end_date, user, conn
    )
    CONN_POOL.putconn(conn)
    return (f"{avg_sleep:.1f}",)


@app.callback(
    Output("SummaryFavoriteWorkoutsFigure", "figure"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
        Input("UserSelectDropdown", "value"),
    ],
)
def update_favorite_workout(start_date: str, end_date: str, user: str):
    conn = get_conn()
    figure = summary_charts.get_favorite_workout_chart(start_date, end_date, user, conn)
    CONN_POOL.putconn(conn)
    return figure


@app.callback(
    Output("SummaryWorkoutHeatmapFigure", "figure"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
        Input("UserSelectDropdown", "value"),
    ],
)
def update_workout_heatmap(start_date: str, end_date: str, user: str):
    conn = get_conn()
    figure = summary_charts.get_workout_heatmap(start_date, end_date, user, conn)
    CONN_POOL.putconn(conn)
    return figure


@app.callback(
    Output("SummaryHoursSleptVariabilityFigure", "figure"),
    Output("SummaryWakeUpTimeVariabilityFigure", "figure"),
    Output("SummaryFallAsleepTimeVariabilityFigure", "figure"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
        Input("UserSelectDropdown", "value"),
    ],
)
def update_sleep_variability(start_date: str, end_date: str, user: str):
    conn = get_conn()
    figure = summary_charts.get_sleep_variability_chart(
        start_date, end_date, user, conn
    )
    CONN_POOL.putconn(conn)
    return figure


@app.callback(
    Output("SummaryCaloriesAvgCaloriesBurned", "children"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
        Input("UserSelectDropdown", "value"),
    ],
)
def update_total_calories(start_date: str, end_date: str, user: str):
    # Calculate the total calories burned for the selected date range
    conn = get_conn()
    avg_calories = summary_analytics.calculate_average_calories(
        start_date, end_date, user, conn
    )

    CONN_POOL.putconn(conn)
    return (f"{avg_calories:,}",)


# Callback to handle file upload
@app.callback(
    Output("output-message", "children"),
    Input("upload-file", "contents"),
    Input("upload-username-input", "value"),
    State("upload-file", "filename"),
    State("upload-file", "last_modified"),
)
def etl(contents, user, filename, last_modified):

    if (user is None) or (len(user) < 1):
        return "Please enter your username"

    if contents is None:
        return "No file uploaded yet."

    # Extract the content type and file data
    content_type, content_string = contents.split(",")

    if "application/zip" not in content_type:
        return "Error: The uploaded file should be a .zip file"

    # Decode the base64 string
    decoded = base64.b64decode(content_string)

    # Save the file to the upload directory
    user_directory = ETL_DATA_DIRECTORY / user
    user_directory.mkdir()
    harvest_directory = user_directory / "harvest"
    harvest_directory.mkdir()
    harvest_file = harvest_directory / "export.zip"

    with open(harvest_file, "xb") as file:
        file.write(decoded)

    extract_data = extract.main(input_path=str(harvest_file), output_file=False)
    transform_data = transform.main(
        data=extract_data, username=user, email="test@test.com"
    )

    load.main(data=transform_data, environment="LOCAL")

    return f"File '{filename}' has been processed"


@app.callback(
    Output("UserSelectDropdown", "options"), Input("UserSelectDropdown", "id")
)
def get_all_users(id):
    df = utils.query_db(sql.GET_USERS, conn=get_conn())
    return list(df["username"])


def get_conn():
    return CONN_POOL.getconn()


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
