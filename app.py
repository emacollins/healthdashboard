# Import necessary libraries
import os

import dash
from dash import html
from dash.dependencies import Input, Output, State
from psycopg2 import pool
from pathlib import Path
import base64

import sections as s
import tabs.summary.charts as summary_charts
import tabs.summary.analytics as summary_analytics

import etl.extract.run as extract
import etl.transform.run as transform
import etl.load.run as load

USERNAME = "eric"

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
    Output("SummaryAvgSleep", "children"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
    ],
)
def update_total_exercise(start_date: str, end_date: str):
    # Calculate the total calories burned for the selected date range
    conn = get_conn()
    avg_sleep = summary_analytics.calculate_average_sleep(
        start_date, end_date, get_username(), conn
    )
    CONN_POOL.putconn(conn)
    return (
        f"{avg_sleep:.1f}",
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

@app.callback(
        Output("SummaryWorkoutHeatmapFigure", "figure"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
    ],
)
def update_workout_heatmap(start_date: str, end_date: str):
    conn = get_conn()
    figure = summary_charts.get_workout_heatmap(
        start_date, end_date, get_username(), conn
    )
    CONN_POOL.putconn(conn)
    return figure

@app.callback(
        Output("SummaryHoursSleptVariabilityFigure", "figure"),
        Output("SummaryWakeUpTimeVariabilityFigure", "figure"),
        Output("SummaryFallAsleepTimeVariabilityFigure", "figure"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
    ],
)
def update_sleep_variability(start_date: str, end_date: str):
    conn = get_conn()
    figure = summary_charts.get_sleep_variability_chart(
        start_date, end_date, get_username(), conn
    )
    CONN_POOL.putconn(conn)
    return figure


@app.callback(
    Output("SummaryCaloriesAvgCaloriesBurned", "children"),
    [
        Input("DateRange", "start_date"),
        Input("DateRange", "end_date"),
    ],
)
def update_total_calories(start_date: str, end_date: str):
    # Calculate the total calories burned for the selected date range
    conn = get_conn()
    avg_calories = summary_analytics.calculate_average_calories(
        start_date, end_date, get_username(), conn
    )

    CONN_POOL.putconn(conn)
    return (
        f"{avg_calories:,}",
    )

# Callback to handle file upload
@app.callback(
    Output("output-message", "children"),
    Input("upload-file", "contents"),
    State("upload-file", "filename"),
    State("upload-file", "last_modified"),
)
def etl(contents, filename, last_modified):

    harvest_directory = ETL_DATA_DIRECTORY / "harvest"
    extract_directory = ETL_DATA_DIRECTORY / "extract"
    transform_directory = ETL_DATA_DIRECTORY / "transform"


    if contents is None:
        return "No file uploaded yet."

    # Extract the content type and file data
    content_type, content_string = contents.split(',')

    if "application/zip" not in content_type:
        return "Error: The uploaded file should be a .zip file"

    # Decode the base64 string
    decoded = base64.b64decode(content_string)

    # Save the file to the upload directory

    harvest_file = harvest_directory / "export.zip"
    with open(harvest_file, "wb") as file:
        file.write(decoded)

    extract.main(input_path=str(harvest_file))
    transform.main(record_input_path=str(extract_directory / "exportRecord.csv.gz"),
                   workout_input_path=str(extract_directory / "exportWorkout.csv.gz"),
                   summary_input_path=str(extract_directory / "exportActivitySummary.csv.gz"),
                   output_directory=str(transform_directory),
                   username=get_username(),
                   email="test@test.com"
                   )
    load.main(fact_table_directory=str(transform_directory),
              environment="LOCAL")

    return f"File '{filename}' has been processed"



def get_conn():
    return CONN_POOL.getconn()


def get_username():
    # Placeholder function
    return "eric"


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
