import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import argparse
import zipfile
import boto3
import os

import utils
import shutil

import constants

from typing import Dict
import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to handler
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)

def unzip_harvest_file(input_path: str) -> str:
    """Unzip the harvest file and return the path to the XML file

    Args:
        input_path (str): Path to zip file (can be S3 URI)

    Returns:
        str: Path to the XML file
    """
    logger.info(f"Unzipping harvest file: {input_path}")

    tmp_dir = os.path.dirname(os.path.realpath(__file__)) + "/tmp/"
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_file_path = os.path.join(tmp_dir, 'zipfile.zip')

    if utils.is_s3_uri(input_path):
        bucket, key = utils.parse_s3_uri(input_path)
        logger.info(f"Downloading file from S3: bucket={bucket}, key={key}")
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, tmp_file_path)
    else:
        logger.info(f"Copying file locally: {input_path}")
        shutil.copy(input_path, tmp_file_path)

    with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
        logger.info("Extracting zip file")
        zip_ref.extractall(tmp_dir)
    extracted_file_path = os.path.join(tmp_dir, 'apple_health_export/export.xml')

    logger.info(f"Extracted file path: {extracted_file_path}")

    return extracted_file_path

def get_data(data_file_path: str) -> Dict[str, pd.DataFrame]:
    # create element tree object
    logger.info(f"Reading data from XML file: {data_file_path}")
    tree = ET.parse(data_file_path) 
    # for every health record, extract the attributes
    root = tree.getroot()
    data = {}
    for tag in constants.tags_of_interest:
        logger.info(f"Extracting data for tag: {tag}")
        record_list = [x.attrib for x in root.iter(tag)]
        data[tag] = pd.DataFrame(record_list)
    logger.info("Data extraction completed")
    return data


def main(input_path: str) -> None:
    """Main function to run extract process

    The extract process takes the zip file exported from Apple
    Health and process the XML file to get tabular health data.
    The output file is a gzip compressed CSV file.

    Args:
        input_path (str): Path to zip file (can be S3 URI)
    """

    try:
        data_file_path = unzip_harvest_file(input_path)
        data = get_data(data_file_path)
        for tag, df in data.items():
            output_path = input_path.replace('harvest', 'extract')
            output_path = os.path.splitext(output_path)[0] + tag + '.csv.gz'
            df.to_csv(output_path, index=False, compression='gzip')
            logger.info(f"Data written to: {output_path}")
        logger.info("Extract process completed")
    finally:
        shutil.rmtree("tmp/")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Health Dashboard Extract Process')
    parser.add_argument('--input_path', type=str, help='Path to activity harvested zip file')
    args = parser.parse_args()
    main(args.input_path)