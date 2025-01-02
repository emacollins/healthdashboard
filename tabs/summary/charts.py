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
        start_date (str): Start date for the summary
        end_date (str): End date for the summary
        username (str): Username for the summary
        conn (object): Connection object to the database
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
        start_date (str): Start date for the summary
        end_date (str): End date for the summary
        username (str): Username for the summary
        conn (object): Connection object to the database
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
            showscale=False,
        )
    )

    fig.update_layout(**config["layout"])

    return fig


def calculate_sleep_variability(data: pd.DataFrame, window: int) -> pd.DataFrame:
    """Calculates sleep wake up and fall asleep variability columns

    data should have columns:
        creation_ts
        fall_asleep_ts
        wake_up_ts

    Fall asleep and wake up variability and calculating by finding the absolute difference
    (in hours) to the reference point, which is always midnight on the creation_ts (generallty
    the day you wake up). This will ensure a consistent reference point in the vast majority of days.

    Args:
        data (pd.DataFrame): Dataframe of raw data to process
        window (int): Rolling window size for calculating standard deviation

    Returns:
        pd.DataFrame: Data containing variability
    """

    data["Hours Slept Variability"] = (
        (((data["wake_up_ts"] - data["fall_asleep_ts"]).dt.total_seconds()) / 3600)
        .rolling(window)
        .std()
    )

    data["Wake Up Time Variability"] = (
        (
            abs(
                (
                    data["wake_up_ts"] - data["creation_ts"].dt.normalize()
                ).dt.total_seconds()  # Normalize to midnight reference point
            )
            / 3600
        )
        .rolling(window)
        .std()
    )

    data["Fall Asleep Time Variability"] = (
        (
            abs(
                (
                    data["fall_asleep_ts"] - data["creation_ts"].dt.normalize()
                ).dt.total_seconds()
            )
            / 3600
        )
        .rolling(window)
        .std()
    )

    return data


def get_sleep_variability_chart(
    start_date: str, end_date: str, username: str, conn: object
) -> tuple[go.Figure]:
    """Generates a sleep variability chart

    Looks at the hours slept variability, wake up time and fall asleep time variabilty.
    Wake up and fall asleep time are measured as absolute number of hours (float) from midnight
    of the wake up date.

    Args:
        Args:
        start_date (str): Start date for the summary
        end_date (str): End date for the summary
        username (str): Username for the summary
        conn (object): Connection object to the database
    Returns:
        go.Figure: Sleep Variability figure
    """
    window = 60  # rolling window parameter
    data_columns = ["creation_ts", "fall_asleep_ts", "wake_up_ts"]
    mode = "lines"
    data = utils.query_db(
        sql.GET_SLEEP_VARIABILITY_DATA, conn, (username, start_date, end_date)
    )
    for col in data.columns:
        data[col] = pd.to_datetime(data[col], utc=True)
        if col not in data_columns:
            raise ValueError(
                "GET_SLEEP_VARIABILITY_DATA SQL query did not return expected columns for calcing sleep var"
            )

    data = calculate_sleep_variability(data=data, window=window)
    data = (
        data.set_index("creation_ts")
        .drop(columns=["fall_asleep_ts", "wake_up_ts"])
        .dropna()
    )
    
    figs = []
    for metric in data.columns:
        fig = go.Figure()
        fig.update_layout(cc.sleep_variability_charts_config[metric]["layout"])
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[metric],
                mode=mode,
                line=dict(shape="spline"),
            )
        )
        figs.append(fig)
    return tuple(figs)
