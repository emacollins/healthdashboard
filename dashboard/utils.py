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