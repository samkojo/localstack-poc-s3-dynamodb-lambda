import os
import logging
import json
from unittest import expectedFailure
from zipfile import ZipFile
from dotenv import load_dotenv
import sys
import boto3
from botocore.exceptions import ClientError

def get_json_from_file(file):
    with open(file) as json_file:
        return json.load(json_file)

load_dotenv()

AWS_REGION = os.getenv('AWS_REGION')
AWS_PROFILE = os.getenv('AWS_PROFILE')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')
LAMBDA_ZIP = './function.zip'
AWS_CONFIG_FILE = '~/.aws/config'
BUCKET = os.getenv('BUCKET')
LAMBDA_NAME = os.getenv('LAMBDA_NAME')
NOTIF_CONFIG_BUCKET = get_json_from_file("s3-notif-config.json")

FILE_NAME = os.getenv('FILEPATH')
OBJECT_NAME = os.getenv('FILENAME')
boto3.setup_default_session(profile_name=AWS_PROFILE)

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def get_boto3_client(service):
    """
    Initialize Boto3 client.
    """
    try:
        lambda_client = boto3.client(
            service,
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL
        )
    except Exception as e:
        logger.exception('Error while connecting to LocalStack.')
        raise e
    else:
        return lambda_client

def get_boto3_resource(service):
    """
    Initialize Boto3 resource.
    """
    try:
        resource = boto3.resource(
            service,
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL
        )
    except Exception as e:
        logger.exception('Error while connecting to LocalStack.')
        raise e
    else:
        return resource

def create_lambda_zip(function_name):
    """
    Generate ZIP file for lambda function.
    """
    try:
        with ZipFile(LAMBDA_ZIP, 'w') as zip:
            zip.write(function_name + '.py')
    except Exception as e:
        logger.exception('Error while creating ZIP file.')
        raise e


def create_lambda(function_name):
    """
    Creates a Lambda function in LocalStack.
    """
    try:
        lambda_client = get_boto3_client('lambda')
        _ = create_lambda_zip(function_name)

        # create zip file for lambda function.
        with open(LAMBDA_ZIP, 'rb') as f:
            zipped_code = f.read()

        lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.8',
            Role='role',
            Handler=function_name + '.handler',
            Code=dict(ZipFile=zipped_code)
        )
    except Exception as e:
        logger.exception('Error while creating function.')
        raise e


def delete_lambda(function_name):
    """
    Deletes the specified lambda function.
    """
    try:
        lambda_client = get_boto3_client('lambda')
        lambda_client.delete_function(
            FunctionName=function_name
        )
        # remove the lambda function zip file
        os.remove(LAMBDA_ZIP)
    except Exception as e:
        logger.exception('Error while deleting lambda function')
        raise e


def invoke_function(function_name):
    """
    Invokes the specified function and returns the result.
    """
    try:
        lambda_client = get_boto3_client('lambda')
        response = lambda_client.invoke(
            FunctionName=function_name)
        return (response['Payload']
                .read()
                .decode('utf-8')
                )
    except Exception as e:
        logger.exception('Error while invoking function')
        raise e


def create_bucket(bucket_name):
    """
    Create a S3 bucket.
    """
    try:
        s3_client = get_boto3_client('s3')
        s3_client.create_bucket(
            Bucket=bucket_name
        )
    except Exception as e:
        logger.exception('Error while creating s3 bucket')
        raise e


def list_s3_bucket_objects(bucket_name):
    """
    List S3 buckets.
    """
    try:
        s3_client = get_boto3_client('s3')
        return s3_client.list_objects_v2(
            Bucket=bucket_name
        )['Contents']
    except Exception as e:
        logger.exception('Error while listing s3 bucket objects')
        raise e


def delete_bucket(bucket_name):
    """
    Delete a S3 bucket.
    """
    try:
        s3_client = get_boto3_client('s3')
        objects = list_s3_bucket_objects(bucket_name)
        # empty the bucket before deleting
        [s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
         for obj in objects]
        s3_client.delete_bucket(
            Bucket=bucket_name
        )
    except Exception as e:
        logger.exception('Error while deleting s3 bucket')
        raise e

def add_notification_bucket(bucket_name, notif_config):
    """
    Add put notification for a S3 Bucket.
    """
    try:
        s3_resource = get_boto3_resource('s3')
        bucket_notif = s3_resource.BucketNotification(bucket_name)
        response = bucket_notif.put(
            NotificationConfiguration = notif_config
        )
    except Exception as e:
        logger.exception('Error while adding put notification for S3 bucket.')
        raise e

def add_file_bucket(bucket_name, file_name, object_name=None):
    """
    Add file to S3 Bucket.
    """
    try:
        s3_client = get_boto3_client('s3')
        if object_name is None:
            object_name = os.path.basename(file_name)
        response = s3_client.upload_file(
            file_name, bucket_name, object_name)
    except ClientError:
        logger.exception('Could not upload file to S3 bucket.')
        raise
    else:
        return response

def main():
    """
    Main invocation function.
    """

if sys.argv[1] == 'create':
    print('\r\nCreating the lambda function...')
    create_lambda(LAMBDA_NAME)
elif sys.argv[1] == 'invoke':
    print('\r\nInvoking the lambda function...')
    print(invoke_function(LAMBDA_NAME))
elif sys.argv[1] == 'delete':
    print('\r\nDeleting the lambda function...')
    delete_lambda(LAMBDA_NAME)
elif sys.argv[1] == 'createbucket':
    print('\r\Creating bucket...')
    create_bucket(BUCKET)
elif sys.argv[1] == 'deletebucket':
    print('\r\nDeleting bucket...')
    delete_bucket(BUCKET)
elif sys.argv[1] == 'listbucket':
    print('\r\Listing bucket...')
    list_s3_bucket_objects(BUCKET)
elif sys.argv[1] == 'addnotifbucket':
    print('\r\Adding notification config for bucket...')
    add_notification_bucket(BUCKET, NOTIF_CONFIG_BUCKET)
elif sys.argv[1] == 'delnotifbucket':
    print('\r\Adding notification config for bucket...')
    add_notification_bucket(BUCKET, {})
elif sys.argv[1] == 'addfilebucket':
    print('\r\Adding file to bucket...')
    add_file_bucket(BUCKET, FILE_NAME, OBJECT_NAME)
else: 
    print('Invalid command... "'+sys.argv[1]+'"')

if __name__ == '__main__':
    main()