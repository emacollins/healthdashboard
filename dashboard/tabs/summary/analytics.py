import pandas as pd

import sql
import utils

def calculate_total_calories(start_date: str, end_date: str, username: str, conn: object) -> int:
    df = utils.query_db(sql.GET_TOTAL_CALORIES, conn, params=(username,start_date, end_date,))
    return int(df.iloc[0, 0])

def calculate_power_equivalent(total_calories: int, comparison_object: str) -> float:
    return .03