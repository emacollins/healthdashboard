import pandas as pd

import sql
import utils

CAL_PER_KWH = 860.421
HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60

def calculate_total_exercise(start_date: str, end_date: str, username: str, conn: object) -> int:
    """Calculates and returns total exercise and average exercise per day

    Args:
        start_date (str): _description_
        end_date (str): _description_
        username (str): _description_
        conn (object): _description_

    Returns:
        int: _description_
    """
    df = utils.query_db(
        sql.GET_TOTAL_EXERCISE_MINUTES,
        conn,
        params=(
            username,
            start_date,
            end_date,
        ),
    )
    return int(df.iloc[0, 0])



def calculate_average_sleep(start_date: str, end_date: str, username: str, conn: object) -> float:
    """Calculatees average sleep duration of timeframe

    Args:
        start_date (str): Starting date
        end_date (str): Ending date
        username (str): User
        conn (object): psycopg2 connection to database

    Returns:
        float: average nightly sleep in hours
    """
    df = utils.query_db(
        sql.GET_AVG_SLEEP,
        conn,
        params=(
            username,
            start_date,
            end_date,
        ),
    )
    df = df[df['hours_slept'] > 2] # Remove anamolies

    return df['hours_slept'].mean()


def calculate_average_calories(
    start_date: str, end_date: str, username: str, conn: object
) -> int:
    """Calculates the total calories burned in time span.

    Queries database, using pre-written query to sum calories over the date
    The return dataframe will always be 1 record. Take that value and return it.

    Args:
        start_date (str): Day to start sum, %Y-%m-%d
        end_date (str): Day to end sum, %Y-%m-%d
        username (str): User calc is for
        conn (object): psycopg2 connection

    Returns:
        int: Average calories per day (kCal)
    """
    df = utils.query_db(
        sql.GET_AVG_CALORIES,
        conn,
        params=(
            username,
            start_date,
            end_date,
        ),
    )
    return int(df.iloc[0, 0])