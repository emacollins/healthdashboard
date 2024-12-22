import pandas as pd
import constants
import argparse
import boto3

import logging
import re

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter("Transform - %(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Add formatter to handler
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)


def parse_category(activity_type: str) -> str:
    """Assigns category for the activity type

    Args:
        activity_type (str): Activity type in raw data

    Returns:
        str: category of the activity
    """
    for key in constants.type_prefixes:
        if key in activity_type:
            return key


def parse_device_string(device_string: str) -> dict:
    """Used on the 'device' column to convert the string to a dictionary

    Incoming string example:
     '<<HKDevice: 0x2832c9130>, name:Apple Watch, manufacturer:Apple Inc.,
     model:Watch, hardware:Watch6,6, software:8.3>'

    Args:
        device_string (str): _description_

    Returns:
        dict: dictionary of device information
    """
    if pd.isnull(device_string):
        return {}
    device_string = device_string[1:-1]  # remove the angle brackets
    device_string = device_string.split(", ")
    device_dict = {}
    for item in device_string:
        key, value = item.split(":", 1)  # only split on the first colon
        device_dict[key] = value
    return device_dict


def process_sleep_data(record_df: pd.DataFrame) -> pd.DataFrame:
    """Process sleep data

    The sleep data provided is categorical and needs to be
    converted to quantify the duration of sleep.

    Args:
        record_df (pd.DataFrame): Record data

    Returns:
        pd.DataFrame: Processed record data to fix sleep
    """
    df = record_df.copy()

    # Split the data into sleep and other records, to combine at the end
    df_record = df.loc[df["type"] != "HKCategoryTypeIdentifierSleepAnalysis"]
    df_sleep = df.loc[df["type"] == "HKCategoryTypeIdentifierSleepAnalysis"]

    df_sleep = df_sleep.drop(columns=["type"]).rename(columns={"value": "type"})
    df_sleep["startDate"] = pd.to_datetime(df_sleep["startDate"])
    df_sleep["endDate"] = pd.to_datetime(df_sleep["endDate"])

    # The value of sleep records is calculated as duration in minutes
    df_sleep["value"] = (
        df_sleep["endDate"] - df_sleep["startDate"]
    ).dt.total_seconds() / 60
    df_sleep["unit"] = "min"

    df = pd.concat([df_record, df_sleep])

    return df


def transform_summary(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Transform the summary data

    Args:
        summary_df (pd.DataFrame): Summary data
        username (str): Username of data owner

    Returns:
        pd.DataFrame: Transformed summary data
    """
    df = summary_df.copy()
    column_rename_map = constants.summary_column_rename_map
    df = df[list(column_rename_map.keys())]
    df = df.rename(columns=column_rename_map)

    # Exported data may have been done midday, thus the latest date will not contian all information
    df["creation_date"] = pd.to_datetime(df["creation_date"])
    df = df.sort_values("creation_date")
    df = df.iloc[:-1]

    return df


def transform_fact_table(fact_table: pd.DataFrame) -> pd.DataFrame:
    """Transform the fact table

    This goes through a series of data cleaning and parsing

    Args:
        fact_table (pd.DataFrame): Fact table

    Returns:
        pd.DataFrame: Transformed fact table
    """
    df = fact_table.copy()

    # Apply function to the 'device' column to unpack key value pairs
    df = df.join(pd.json_normalize(df["device"].apply(parse_device_string)))

    # Rename columns to match database table columnn names
    df = df[list(constants.fact_table_column_rename_map.keys())].rename(
        columns=constants.fact_table_column_rename_map
    )

    # These steps clean up the activity_type_name and create a new column
    # to indicate the category of the activity

    df["category_prefix"] = df["activity_type_name"].apply(parse_category)
    df["activity_category"] = df["category_prefix"].apply(
        lambda x: constants.type_prefixes.get(x, "other")
    )
    df["activity_type_name"] = df["activity_type_name"].str.replace(
        "|".join(list(constants.type_prefixes.keys())), "", regex=True
    )

    # Filter out records that are not useful
    df = df.loc[df["category_prefix"].isin(constants.type_prefixes.keys())]
    df = df.loc[df["activity_category"] != "other"]
    df = df.loc[~df["activity_type_name"].isin(constants.activity_types_to_drop)]

    # *Edge case, each hour of standing is a separate record*
    df.loc[df["activity_type_name"] == "AppleStandHour", "value"] = 1.0
    df.loc[df["activity_type_name"] == "AppleStandHour", "unit_name"] = "hr"

    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.loc[~df["value"].isna()]
    return df


def process_fact_table(
    record_df: pd.DataFrame, workout_df: pd.DataFrame, username, email
) -> pd.DataFrame:
    """Process the fact table

    Args:
        record_df (pd.DataFrame): Data from the "exportRecord" CSV file
        workout_df (pd.DataFrame): Data from the "exportWorkout" CSV file
        username (_type_): username of data owner
        email (_type_): email of data owner

    Returns:
        pd.DataFrame: Final fact table
    """
    df = pd.concat(
        [record_df, workout_df.rename(columns=constants.workout_column_rename_map)]
    )
    df = transform_fact_table(df)
    df["username"] = username
    df["email"] = email
    return df[constants.fact_table_final_columns]


def process_summary_table(summary_df: pd.DataFrame, username: str) -> pd.DataFrame:
    """Process the summary table

    Args:
        summary_df (pd.DataFrame): Data from the "exportActivitySummary" CSV file
        username (str): username of data owner

    Returns:
        pd.DataFrame: Final summary table
    """
    df = summary_df.copy()
    df = transform_summary(df)
    df["username"] = username
    return df


def parse_s3_uri(s3_uri: str) -> tuple:
    """Parse S3 URI to bucket and key

    Args:
        s3_uri (str): S3 URI

    Returns:
        tuple: Bucket and key
    """
    pattern = r"s3://([^/]+)/(.+)"
    match = re.match(pattern, s3_uri)
    if match:
        bucket = match.group(1)
        key = match.group(2)
        return bucket, key
    else:
        raise ValueError(f"Invalid S3 URI format: {s3_uri}")


def load_data(
    record_input_path: str, workout_input_path: str, summary_input_path: str
) -> pd.DataFrame:
    """Load the data from the input path

    Args:
        input_path (str): Path to the input file

    Returns:
        (pd.DataFrame, pd.DataFrame, pd.Datafrane): record_data, workout_data, summary_data
    """
    if record_input_path.startswith("s3://"):
        s3 = boto3.client("s3")
        bucket, key = parse_s3_uri(record_input_path)
        record_df = pd.read_csv(
            s3.get_object(Bucket=bucket, Key=key)["Body"], compression="gzip"
        )
    else:
        record_df = pd.read_csv(record_input_path, compression="gzip")

    if workout_input_path.startswith("s3://"):
        s3 = boto3.client("s3")
        bucket, key = parse_s3_uri(workout_input_path)
        workout_df = pd.read_csv(
            s3.get_object(Bucket=bucket, Key=key)["Body"], compression="gzip"
        )
    else:
        workout_df = pd.read_csv(workout_input_path, compression="gzip")

    if summary_input_path.startswith("s3://"):
        s3 = boto3.client("s3")
        bucket, key = parse_s3_uri(summary_input_path)
        summary_df = pd.read_csv(
            s3.get_object(Bucket=bucket, Key=key)["Body"], compression="gzip"
        )
    else:
        summary_df = pd.read_csv(summary_input_path, compression="gzip")

    return record_df, workout_df, summary_df


def output_data(
    fact_table: pd.DataFrame,
    summary_table: pd.DataFrame,
    output_directory: str,
    username: str,
) -> None:
    """Outputs compressed CSVs to the output path

    Args:
        fact_table (pd.DataFrame): DF of the fact table
        summary_table (pd.DataFrame): DF of the summary table
        output_directory (str): Directory to output both tables to
        username (str): Username of data owner
    """
    if output_directory[-1] == "/":
        output_directory = output_directory[:-1]
    try:
        fact_table.to_csv(
            f"{output_directory}/{constants.FACT_TABLE_FILENAME}",
            index=False,
            compression="gzip",
        )
        summary_table.to_csv(
            f"{output_directory}/{constants.SUMMARY_TABLE_FILENAME}",
            index=False,
            compression="gzip",
        )
        logger.info("Data saved successfully")
    except Exception as e:
        logger.error(f"Failed to save data for user {username}: {str(e)}")


def fill_missing_device_columns(fact_table: pd.DataFrame) -> pd.DataFrame:
    """Fill missing device columns with empty strings

    Args:
        df (pd.DataFrame): DataFrame to fill missing columns

    Returns:
        pd.DataFrame: DataFrame with missing columns filled
    """

    fact_table.sort_values(
        by=["source_name", "start_ts", "activity_type_name", "device_name"],
        ascending=True,
        inplace=True,
    )
    fact_table.reset_index(drop=True, inplace=True)
    fact_table[constants.device_columns] = fact_table[constants.device_columns].fillna(
        method="ffill"
    )
    return fact_table


def main(
    record_input_path: str,
    workout_input_path: str,
    summary_input_path: str,
    output_directory: str,
    username: str,
    email: str,
) -> None:
    """Main function to run the transform process"""

    # Load the data
    record_df, workout_df, summary_df = load_data(
        record_input_path, workout_input_path, summary_input_path
    )
    logger.info("Data loaded successfully")

    # Fix sleep data in record_df
    record_df = process_sleep_data(record_df)
    logger.info("Sleep data processed successfully")

    # Transform and clean final fact table
    fact_table = process_fact_table(record_df, workout_df, username, email)
    fact_table = fill_missing_device_columns(fact_table)
    logger.info("Fact table transformed successfully")

    # Summary data is done separately, as it is a different process
    summary_table = process_summary_table(summary_df, username)
    logger.info("Summary data transformed successfully")

    # Save the data
    output_data(fact_table, summary_table, output_directory, username)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Health Dashboard Transform Process")
    parser.add_argument(
        "--record_input_path",
        type=str,
        help='Path to "exportRecord" CSV file. Can be s3 URI or local path.',
    )
    parser.add_argument(
        "--workout_input_path",
        type=str,
        help='Path to "exportWorkout" CSV file. Can be s3 URI or local path.',
    )
    parser.add_argument(
        "--summary_input_path",
        type=str,
        help='Path to "exportActivitySummary" CSV file. Can be S3 URI or local path.',
    )
    # All files are expected to be output in the same directory
    parser.add_argument(
        "--output_directory",
        type=str,
        help="Output directory path. Can be S3 URI or local path.",
    )

    parser.add_argument("--username", type=str, help="Username of data owner")
    parser.add_argument("--email", type=str, help="Data owner email")
    args = parser.parse_args()
    main(
        args.record_input_path,
        args.workout_input_path,
        args.summary_input_path,
        args.output_directory,
        args.username,
        args.email,
    )
