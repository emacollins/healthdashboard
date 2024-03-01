import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt

ACTIVITY_HARVEST_FILE = '/Users/ericcollins/healthdashboard_data/harvest/2024-02-29/apple_health/apple_health_export/export.xml'
SLEEP_HARVEST_FILE = '/Users/ericcollins/healthdashboard_data/harvest/2023-05-13/PillowData.csv'
EXTRACT_FILE = '/Users/ericcollins/healthdashboard_data/extract/apple_health_extract.csv'


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


def run():
    activity_data = get_activity_data()
    activity_data.to_csv("test.csv", index=False)
    

if __name__ == '__main__':
    run()