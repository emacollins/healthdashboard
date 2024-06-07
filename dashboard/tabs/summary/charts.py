from datetime import datetime
from typing import Dict

import pandas as pd
import scipy.stats as stats
import plotly.graph_objects as go
import plotly.express as px
import sql
import tabs.summary.charts_config as cc
import utils
import colors


def create_trendline_column(
    data: pd.DataFrame, x: str, y: str, chart_name: str
) -> pd.DataFrame:
    """Add trendline values column to plot

    Args:
        data (pd.DataFrame): Data to add trendline column to

    Returns:
        pd.DataFrame: Dataframe with column trendline column
    """

    if "trendline" in data.columns:
        return data

    slope, intercept, r, p, se = stats.linregress(data[x], data[y])

    data[chart_name + "_trendline"] = slope * data[x] + intercept

    return data


def create_summary_figure(
    data,
    chart_name: str,
):
    """Create a Plotly figure for the summary charts

    Args:
        data (pd.DataFrame): The data to plot.
        chart_name (str): The name of the chart to create.

    Returns:
        go.Figure: The created figure.
    """

    chart_config = cc.summary_charts_config[chart_name]
    mode = "lines"

    fig = go.Figure(layout=chart_config["layout"])
    fig.update_layout(showlegend=False)
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[chart_config["y_data_column"]],
            mode=mode,
            line=dict(shape="spline"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[chart_name + "_trendline"],
            mode=mode,
            line=dict(dash="dash"),
        )
    )

    return fig


def generate_summary_charts(
    start_date: str, end_date: str, username: str, conn: object
) -> Dict[str, go.Figure]:
    """Generate summary charts for the given date range and username

    Args:
        start_date (str): Start date for the summary
        end_date (str): End date for the summary
        username (str): Username for the summary
        conn (object): Connection object to the database
        smooth (bool): Whether to smooth the chart

    Returns:
        dict: A dict of go.Figure objects
    """
    days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days
    data = utils.query_db(
        sql.GET_SUMMARY, conn, (username, username, username, start_date, end_date)
    )
    data = data.set_index("date")

    # TODO: Add to user input settings
    if days > 364:
        window = 30
    elif days > 30:
        window = 7
    else:
        window = 1

    data = data.rolling(window=window).mean().dropna()
    data["date_index"] = range(len(data))  # used for trendline

    # Generate the summary charts
    figures = {key: None for key in cc.summary_charts_config.keys()}

    for chart in figures:
        data = create_trendline_column(
            data, "date_index", cc.summary_charts_config[chart]["y_data_column"], chart
        )
        figures[chart] = create_summary_figure(data, chart)

    return figures


def get_favorite_workout_chart(
    start_date: str, end_date: str, username: str, conn: object
) -> go.Figure:
    """Creates bar chart of top workouts in date range

    Args:
        start_date (str): _description_
        end_date (str): _description_
        username (str): _description_
        conn (object): _description_
    """
    config = cc.favorite_workout_chart_config
    days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days
    data = utils.query_db(
        sql.GET_EXERCISE_COUNT, conn, (username, start_date, end_date)
    )
    data = data.sort_values(by="count", ascending=True)
    data = data.tail(5)
    data[config["y_data_column"]] = data[config["y_data_column"]].apply(
        utils.split_activity_name_string
    )
    fig = go.Figure(layout=config["layout"])
    fig.add_trace(
        go.Bar(
            y=data[cc.favorite_workout_chart_config["y_data_column"]],
            x=data[cc.favorite_workout_chart_config["x_data_column"]],
            text=data[cc.favorite_workout_chart_config["x_data_column"]],
            textposition="auto",
            orientation="h",
            textfont={"color": "white", "size": 14},
        )
    )
    return fig


def get_workout_heatmap(
    start_date: str, end_date: str, username: str, conn: object
) -> go.Figure:
    """Creates heatmap of workout time by days of the week and time

    Args:
        start_date (str): _description_
        end_date (str): _description_
        username (str): _description_
        conn (object): _description_
    """
    config = cc.workout_heatmap_chart_config
    data = utils.query_db(sql.GET_EXERCISE_MIN, conn, (username, start_date, end_date))
    day_map = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
    }
    data["day"] = data["day"].map(day_map)

    def label_time(t):
        if (t >= 17) & (t < 21):
            return "Evening"
        elif (t >= 21) & (t < 4):
            return "Night"
        elif (t >= 4) & (t < 12):
            return "Morning"
        elif (t >= 12) & (t < 17):
            return "Afternoon"

    data["time_label"] = data["hour"].apply(label_time)
    data = data.groupby(["day", "time_label"]).sum().reset_index()
    data = data.pivot(index="time_label", columns="day", values="value").reindex(
        columns=list(day_map.values()),
        index=["Night", "Evening", "Afternoon", "Morning"],
    )
    data = data[~(data.isna()).all(axis=1)]
    fig = go.Figure(
    data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale=["white", colors.SUMMARY_EXERCISE_COLOR],
        showscale=False
    )
)

    fig.update_layout(**config["layout"])

    return fig

def get_sleep_variability_chart(start_date: str, end_date: str, username: str, conn: object) -> go.Figure:
    """Generates a sleep variability chart

    Args:
        start_date (str): _description_
        end_date (str): _description_
        username (str): _description_
        conn (object): _description_

    Returns:
        go.Figure: _description_
    """
    data = utils.query_db(sql.GET_SLEEP_VARIABILITY_DATA, conn, (username, start_date, end_date))
    data_fall_aslee_time = data.groupby(by="wake_up_date")["start_ts"].min()
    data_wake_up_time = data.groupby(by="wake_up_date")["end_ts"].max()
    data