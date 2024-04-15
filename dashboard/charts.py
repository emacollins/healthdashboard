import pandas as pd
import plotly.graph_objects as go
import sql
from datetime import datetime
import scipy.stats as stats
import charts_config as cc
from typing import Dict


def query_db(query: str, conn: object, params: tuple = None) -> pd.DataFrame:
    with conn.cursor() as cur:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
    return df


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
    fig.add_trace(go.Scatter(x=data.index, y=data[chart_config["y_data_column"]], mode=mode))

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
    days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
    data = query_db(sql.GET_SUMMARY, conn, (username, username, start_date, end_date))
    data = data.set_index("date")

    if days > 364:
        window = 30
    else:
        window = 7

    data = data.rolling(window=window).mean().dropna()

    # Generate the summary charts
    figures = {key: None for key in cc.summary_charts_config.keys()}

    for chart in figures:
        figures[chart] = create_summary_figure(data, chart)

    return figures
