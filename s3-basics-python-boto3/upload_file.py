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

s3_client = boto3.client("s3", region_name=AWS_REGION,
                         endpoint_url=ENDPOINT_URL)

def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to a S3 bucket.
    """
    try:
        if object_name is None:
            object_name = os.path.basename(file_name)
        response = s3_client.upload_file(
            file_name, bucket, object_name)
    except ClientError:
        logger.exception('Could not upload file to S3 bucket.')
        raise
    else:
        return response


def main():
    """
    Main invocation function.
    """
    file_name = os.getenv('FILEPATH')
    object_name = os.getenv('FILENAME')
    bucket = os.getenv('BUCKET')
    logger.info('Uploading file to S3 bucket in LocalStack...')
    s3 = upload_file(file_name, bucket, object_name)
    logger.info('File uploaded to S3 bucket successfully.')


if __name__ == '__main__':
    main()