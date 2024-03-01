import plotly.graph_objects as go
import pandas as pd


def create_time_series_plot(df: pd.DataFrame,
                            metric: str,
                            group_values_by: str,
                            date_column: str = 'creationDate'):
    """
    Creates a time-series plot for a given metric.

    Parameters:
    df (pandas.DataFrame): The health data.
    metric (str): The health metric to plot.
    group_values_by (str):

    Returns:
    plotly.graph_objects.Figure: The time-series plot.
    """

    grouping_dates = ['date', 'year', 'month-year']
    if group_values_by not in grouping_dates:
        assert 0 == 1, 'Supplied group_values_by parameter not valid'
    
    if group_values_by == 'date':
        df['date'] = pd.to_datetime(df[date_column]).dt.date
    elif group_values_by == 'year':
        df['date'] = pd.to_datetime(df[date_column]).dt.year
    elif group_values_by == 'month-year':
        df['date'] = pd.to_datetime(df[date_column]).dt.strftime('%m-%Y')
    
    # Select the data for the metric
    metric_df = df[df['type'] == metric]
    metric_df = metric_df.groupby(by='date', as_index=False)['value'].sum()
    
    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=metric_df['date'],
        y=metric_df['value'],
        mode='lines',
        name=metric
    ))

    # Add title and labels
    fig.update_layout(
        title=f"{metric} Over Time",
        xaxis_title="Date",
        yaxis_title=metric
    )

    return fig

if __name__=='__main__':
    df = pd.read_csv('/Users/ericcollins/healthdashboard_data/extract/apple_health_extract.csv')
    summed_metrics = ['ActiveEnergyBurned', 'AppleExerciseTime', 'DistanceWalkingRunning', 'StepCount']
    
    for metric in summed_metrics:
        create_time_series_plot(df, metric, group_values_by='date').write_image(f'graphs/linechart_{metric}.png')