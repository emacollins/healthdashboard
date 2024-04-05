import pandas as pd
import plotly.graph_objects as go
import sql

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

def generate_summary_charts(start_date: str, end_date: str, username: str, conn: object) -> tuple:
    """Generate summary charts for the given date range and username

    Args:
        start_date (str): Start date for the summary
        end_date (str): End date for the summary
        username (str): Username for the summary
        conn (object): Connection object to the database

    Returns:
        _type_: _description_
    """
    data = query_db(sql.GET_SUMMARY, conn, (username, start_date, end_date))


    
    # Generate the summary charts
    fig_active_energy = go.Figure(data=go.Scatter(x=data["date"], y=data["active_energy_burned"], mode="lines+markers")).update_layout(title="Active Energy Burned")
    fig_exercise_minutes = go.Figure(data=go.Scatter(x=data["date"], y=data["exercise_minutes"], mode="lines+markers")).update_layout(title="Exercise Minutes")
    fig_stand_hours = go.Figure(data=go.Scatter(x=data["date"], y=data["stand_hours"], mode="lines+markers")).update_layout(title="Stand Hours")
    
    return fig_active_energy, fig_exercise_minutes, fig_stand_hours