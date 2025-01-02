import pandas as pd

def query_db(query: str, conn: object, params: tuple = None) -> pd.DataFrame:
    """Queries Postgres DB and returns dataframe

    Args:
        query (str): SQL query
        conn (object): psycopg2 connection object
        params (tuple, optional): Query parameters. Defaults to None.

    Returns:
        pd.DataFrame: Dataframe of returned table
    """
    with conn.cursor() as cur:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
    return df

def split_activity_name_string(text: str) -> str:
    """Splits text string for spaces between words

    Example: TraditionalStrengthTraining -> Traditional Strength Training

    Args:
        text (str): Activity name 

    Returns:
        str: Split name
    """
    index = 0
    new_text = text
    for char in text:
        if index == 0:
            index+=1
            continue
        if (char.isupper()):
            new_text = new_text[:index] + " " + new_text[index:]
            index = index + 2
        else:
            index+=1
    return new_text
            