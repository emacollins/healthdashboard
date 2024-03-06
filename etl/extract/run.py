import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import argparse

def get_activity_data():
    # create element tree object
    tree = ET.parse(ACTIVITY_HARVEST_FILE) 
    # for every health record, extract the attributes
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]

    record_data = pd.DataFrame(record_list)

    # proper type to dates
    for col in ['creationDate', 'startDate', 'endDate']:
        record_data[col] = pd.to_datetime(record_data[col])

    # value is numeric, NaN if fails
    record_data['value'] = pd.to_numeric(record_data['value'], errors='coerce')

    # some records do not measure anything, just count occurences
    # filling with 1.0 (= one time) makes it easier to aggregate
    record_data['value'] = record_data['value'].fillna(1.0)

    # shorter observation names
    record_data['type'] = record_data['type'].str.replace('HKQuantityTypeIdentifier', '')
    record_data['type'] = record_data['type'].str.replace('HKCategoryTypeIdentifier', '')
    return record_data


def main(harvest_zip_file: str) -> None:
    """Main function to run extract process

    The extract process takes the zip file exported from Apple
    Health and process the XML file to get tabular health data.

    Args:
        harvest_zip_file (str): Path to zip file (can be S3 URI)
    """
    activity_data = get_activity_data()
    activity_data.to_csv("test.csv", index=False)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Health Dashboard Extract Process')
    parser.add_argument('--harvest_zip_file', type=str, help='Path to activity harvest file')
    args = parser.parse_args()
    main(args.harvest_zip_file)