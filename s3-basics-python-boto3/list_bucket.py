import logging
import boto3
from botocore.exceptions import ClientError
import json
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv('AWS_REGION')
AWS_PROFILE = os.getenv('AWS_PROFILE')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

boto3.setup_default_session(profile_name=AWS_PROFILE)

s3_resource = boto3.resource("s3", region_name=AWS_REGION,
                         endpoint_url=ENDPOINT_URL)

def list_buckets():
    """
    List S3 buckets.
    """
    try:
        response = s3_resource.buckets.all()
    except ClientError:
        logger.exception('Could not list S3 bucket from LocalStack.')
        raise
    else:
        return response


def main():
    """
    Main invocation function.
    """
    logger.info('Listing S3 buckets from LocalStack...')
    s3 = list_buckets()
    logger.info('S3 bucket names: ')
    for bucket in s3:
        logger.info(bucket.name)


if __name__ == '__main__':
    main()