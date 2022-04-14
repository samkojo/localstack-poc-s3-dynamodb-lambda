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
s3_resource = boto3.resource("s3", region_name=AWS_REGION,
                         endpoint_url=ENDPOINT_URL)

def empty_bucket(bucket_name):
    """
    Deletes all objects in the bucket.
    """
    try:
        logger.info('Deleting all objects in the bucket...')
        bucket = s3_resource.Bucket(bucket_name)
        response = bucket.objects.all().delete()
    except:
        logger.exception('Could not delete all S3 bucket objects.')
        raise
    else:
        return response


def delete_bucket(bucket_name):
    """
    Deletes a S3 bucket.
    """
    try:
        # remove all objects from the bucket before deleting the bucket
        empty_bucket(bucket_name)
        # delete bucket
        response = s3_client.delete_bucket(
            Bucket=bucket_name)
    except ClientError:
        logger.exception('Could not delete S3 bucket locally.')
        raise
    else:
        return response


def main():
    """
    Main invocation function.
    """
    bucket_name = os.getenv('BUCKET')
    logger.info('Deleting S3 bucket...')
    s3 = delete_bucket(bucket_name)
    logger.info('S3 bucket deleted.')
    logger.info(json.dumps(s3, indent=4) + '\n')


if __name__ == '__main__':
    main()