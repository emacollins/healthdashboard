import pandas as pd

import sql
import utils

# All power data values in kWh / day
POWER_DATA = {"House": 29, "Lightbulb": 2.4}

# kcals
FOOD_DATA = {"Burger": 354, "Cheezeits": (150 / 27)}

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

def calculate_total_calories(
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
        int: Total calories (kCal)
    """
    df = utils.query_db(
        sql.GET_TOTAL_CALORIES,
        conn,
        params=(
            username,
            start_date,
            end_date,
        ),
    )
    return int(df.iloc[0, 0])


def convert_days_to_appropriate_unit(days_of_power: float) -> tuple[float, str]:
    """Convert days of power to appropriate time unit."""
    if days_of_power < 1:
        return days_of_power / HOURS_IN_DAY, "hours"
    elif days_of_power < 1 / HOURS_IN_DAY:
        return days_of_power / (HOURS_IN_DAY * MINUTES_IN_HOUR), "minutes"
    elif days_of_power < 1 / (HOURS_IN_DAY * MINUTES_IN_HOUR * SECONDS_IN_MINUTE):
        return (
            days_of_power / (HOURS_IN_DAY * MINUTES_IN_HOUR * SECONDS_IN_MINUTE),
            "seconds",
        )
    else:
        return days_of_power, "days"


def calculate_power_equivalent(
    total_calories: int, comparison_object: str
) -> tuple[float, str]:
    """Compares calories burned to everyday items power consumption

    Args:
        total_calories (int): Total calories burned by the user
        comparison_object (str): Item selected by user

    Returns:
        tuple[float, str]: (power time, units)
    """

    total_calories_kwh = total_calories / CAL_PER_KWH
    try:
        days_of_power = total_calories_kwh / POWER_DATA.get(comparison_object, 0)
    except ZeroDivisionError:
        return 0, "days"

    return convert_days_to_appropriate_unit(days_of_power)


def get_power_equivalent_dropdown_values():
    values = list(POWER_DATA.keys())
    return values

def calculate_food_equivalent(total_calories: int) -> tuple[float]:
    """Calculates food item equivalents consumed

    Args:
        total_calories (int): Total calories in time period
    """

    burgers = total_calories / FOOD_DATA.get("Burger")
    cheezeits = total_calories / FOOD_DATA.get("Cheezeits")
    return burgers, cheezeits

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
