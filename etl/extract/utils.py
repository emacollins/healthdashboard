import boto3
from urllib.parse import urlparse

def is_s3_uri(path) -> bool:
    parsed_url = urlparse(path)
    return parsed_url.scheme == 's3'

def parse_s3_uri(path):
    parsed_url = urlparse(path)
    if parsed_url.scheme != 's3':
        raise ValueError("Not a valid S3 URI")
    bucket = parsed_url.netloc
    key = parsed_url.path.lstrip('/')
    return bucket, key