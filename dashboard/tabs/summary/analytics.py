import pandas as pd

import sql
import utils

#All power data values in kWh / day
POWER_DATA = {"House": 29,
              "Lightbulb": 2.4} 

CAL_PER_KWH = 860.421
HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60

def calculate_total_calories(start_date: str, end_date: str, username: str, conn: object) -> int:
    """Calculates the total calories burned in time span.

    Queries database, using pre-written query to sum calories over the date
    The return dataframe will always be 1 record. Take that value and return it. 

    Args:
        start_date (str): Day to start sum, %Y-%m-%d
        end_date (str): Day to end sum, %Y-%m-%d
        username (str): User calc is for
        conn (object): psycopg2 connection

    Returns:
        int: Total calorioes (kCal)
    """
    df = utils.query_db(sql.GET_TOTAL_CALORIES, conn, params=(username,start_date, end_date,))
    return int(df.iloc[0, 0])

def convert_days_to_appropriate_unit(days_of_power: float) -> tuple[float, str]:
    """Convert days of power to appropriate time unit."""
    if days_of_power < 1:
        return days_of_power / HOURS_IN_DAY, "hours"
    elif days_of_power < 1 / HOURS_IN_DAY:
        return days_of_power / (HOURS_IN_DAY * MINUTES_IN_HOUR), "minutes"
    elif days_of_power < 1 / (HOURS_IN_DAY * MINUTES_IN_HOUR * SECONDS_IN_MINUTE):
        return days_of_power / (HOURS_IN_DAY * MINUTES_IN_HOUR * SECONDS_IN_MINUTE), "seconds"
    else:
        return days_of_power, "days"

def calculate_power_equivalent(total_calories: int, comparison_object: str) -> tuple[float, str]:
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