import pandas as pd
import constants
import argparse

import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

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
    record_df = pd.read_csv(record_input_path)
    workout_df = pd.read_csv(workout_input_path)
    summary_df = pd.read_csv(summary_input_path)
    logger.info("Data loaded successfully")

    # Fix sleep data in record_df
    record_df = process_sleep_data(record_df)
    logger.info("Sleep data processed successfully")

    # Transform and clean final fact table
    fact_table = pd.concat(
        [record_df, workout_df.rename(columns=constants.workout_column_rename_map)]
    )
    fact_table = transform_fact_table(fact_table)
    fact_table["username"] = username
    fact_table["email"] = email
    logger.info("Fact table transformed successfully")

    # Summary data is done separately, as it is a different process
    summary_df = transform_summary(summary_df)
    summary_df["username"] = username
    logger.info("Summary data transformed successfully")

    # Save the data
    if output_directory[-1]=="/":
        output_directory = output_directory[:-1]
    fact_table[constants.fact_table_final_columns].to_csv(f"{output_directory}/fact_table.csv.gz", index=False, compression="gzip")
    summary_df.to_csv(f"{output_directory}/summary_table.csv.gz", index=False, compression="gzip")
    logger.info("Data saved successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Health Dashboard Transform Process")
    parser.add_argument(
        "--record_input_path", type=str, help='Path to "exportRecord" CSV file'
    )
    parser.add_argument(
        "--workout_input_path", type=str, help='Path to "exportWorkout" CSV file'
    )
    parser.add_argument(
        "--summary_input_path",
        type=str,
        help='Path to "exportActivitySummary" CSV file',
    )
    # All files are expected to be output in the same directory
    parser.add_argument("--output_directory", type=str, help="Output directory path")

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
