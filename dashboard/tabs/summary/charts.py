from datetime import datetime
from typing import Dict

import pandas as pd
import scipy.stats as stats
import plotly.graph_objects as go
import sql
import tabs.summary.charts_config as cc
import utils


def create_trendline_column(data: pd.DataFrame, x: str, y: str) -> pd.DataFrame:
    """Add trendline values column to plot

    Args:
        data (pd.DataFrame): Data to add trendline column to

    Returns:
        pd.DataFrame: Dataframe with column trendline column
    """

    if "trendline" in data.columns:
        return data

    slope, intercept, r, p, se = stats.linregress(data[x], data[y])

    data["trendline"] = slope * data[x] + intercept

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
            y=data["trendline"],
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
    data["date_index"] = range(len(data))
    data = create_trendline_column(data, "date_index", "total_calories")

    # Generate the summary charts
    figures = {key: None for key in cc.summary_charts_config.keys()}

    for chart in figures:
        figures[chart] = create_summary_figure(data, chart)

    return figures
