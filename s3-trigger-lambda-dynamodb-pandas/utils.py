import os
import logging
import json
from unittest import expectedFailure
from zipfile import ZipFile
import sys
import boto3
from botocore.exceptions import ClientError
from datetime import date, datetime
import pandas as pd

def get_json_from_file(file):
    with open(file) as json_file:
        return json.load(json_file)

AWS_REGION = 'us-east-1'
AWS_PROFILE = 'localstack'
ENDPOINT_URL = 'http://localhost:4566'

CNPJ = '1234'
# Nome do bucket
BUCKET = 'client-data-sync-s3'
# Caminho do arquivo
FILE_PATH = '../assets/test.parquet'
FILE_NAME = CNPJ+'/'+'test.parquet'

# nome do lambda
LAMBDA_NAME = 'lambda-s3-dynamodb'

# tabela do dynamodb
TABLENAME = 'sum_notas_dia'

LAMBDA_ZIP = './function.zip'
AWS_CONFIG_FILE = '~/.aws/config'
NOTIF_CONFIG_BUCKET = get_json_from_file("s3-notif-config.json")

ROLE = 'arn:aws:iam::000000000000:role/lambda-s3-role'

# Specifies the Resource Tags (Optional)
TAGS = [
    {
        'Key': 'CNPJ,IDNFDET',
        'Value': 'notas'
    }
]
# Specifies the attributes that make up the primary key for a table or an index
KEYSCHEMA = [
    {
        'AttributeName': 'CNPJ',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': 'DATA',
        'KeyType': 'RANGE'
    }
]
# Specifies a list of attributes that describe the key schema for the table and indexes
ATTRIBUTEDEFINITIONS = [
    {
        'AttributeName': 'CNPJ',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'DATA',
        'AttributeType': 'S'
    }
]

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

# S3
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

def empty_bucket(bucket_name):
    """
    Deletes all objects in the bucket.
    """
    try:
        logger.info('Deleting all objects in the bucket...')
        s3_resource = get_boto3_resource('s3')
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
        s3_client = get_boto3_client('s3')
        # delete bucket
        response = s3_client.delete_bucket(
            Bucket=bucket_name)
    except ClientError:
        logger.exception('Could not delete S3 bucket locally.')
        raise
    else:
        return response

def list_buckets():
    """
    List S3 buckets.
    """
    try:
        s3_resource = get_boto3_resource('s3')
        response = s3_resource.buckets.all()
    except ClientError:
        logger.exception('Could not list S3 bucket from LocalStack.')
        raise
    else:
        return response

def upload_file(bucket, file_name, object_name=None):
    """
    Upload a file to a S3 bucket.
    """
    try:
        if object_name is None:
            object_name = os.path.basename(file_name)
        s3_client = get_boto3_client('s3')
        response = s3_client.upload_file(
            file_name, bucket, object_name)
    except ClientError:
        logger.exception('Could not upload file to S3 bucket.')
        raise
    else:
        return response

def cat_file(bucket, file_name):
    """
    Cat a file from S3 bucket.
    """
    try:
        s3_client = get_boto3_client('s3')
        response = s3_client.get_object(
            Bucket=bucket, Key=file_name)
    except ClientError:
        logger.exception('Could not cat file from S3 bucket.')
        raise
    else:
        return response

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

# LAMBDA

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

        # create zip file for lambda function.
        with open(LAMBDA_ZIP, 'rb') as f:
            zipped_code = f.read()

        lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.8',
            Role=ROLE,
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
        # os.remove(LAMBDA_ZIP)
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

# DYNAMODB

def json_datetime_serializer(obj):
    """
    Helper method to serialize datetime fields
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

def create_dynamodb_table(table_name):
    """
    Creates a DynamoDB table.
    """
    try:
        dynamodb_client = get_boto3_client("dynamodb")
        response = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=KEYSCHEMA,
            AttributeDefinitions=ATTRIBUTEDEFINITIONS,
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            },
            Tags=TAGS)

    except ClientError:
        logger.exception('Could not create the table.')
        raise
    else:
        return response

def delete_dynamodb_table(table_name):
    """
    Creates a DynamoDB table.
    """
    try:
        dynamodb_client = get_boto3_client("dynamodb")
        response = dynamodb_client.delete_table(
            TableName=table_name
        )

    except ClientError:
        logger.exception('Could not delete the table.')
        raise
    else:
        return response

def read_dynamodb_table_item(table_name, cnpj, data):
    """
    Reads from a DynamoDB table.
    """
    try:
        dynamodb_resource = get_boto3_resource("dynamodb")
        table = dynamodb_resource.Table(table_name)
        response = table.get_item(
            Key={
                'CNPJ': cnpj,
                'DATA': data
            }
        )

    except ClientError:
        logger.exception('Could not read the item from table.')
        raise
    else:
        return response

def main():
    """
    Main invocation function.
    """

    if sys.argv[1] == 's3':
        if sys.argv[2] == 'create':
            print('\r\Creating bucket..."', BUCKET, '"')
            create_bucket(BUCKET)
        elif sys.argv[2] == 'delete':
            print('\r\Deleting bucket...', BUCKET, '"')
            delete_bucket(BUCKET)
        elif sys.argv[2] == 'listall':
            print('\r\Listing all buckets...')
            logger.info('Listing S3 buckets from LocalStack...')
            s3 = list_buckets()
            logger.info('S3 bucket names: ')
            for bucket in s3:
                logger.info(bucket.name)
        elif sys.argv[2] == 'list':
            print('\r\Listing bucket files...')
            list_s3_bucket_objects(BUCKET)
        elif sys.argv[2] == 'uploadfile':
            print('\r\Adding file to bucket...')
            upload_file(BUCKET, FILE_PATH, FILE_NAME)
        # elif sys.argv[2] == 'catfile':
        #     print('\r\Catting file from bucket...')
        #     result = cat_file(BUCKET, FILE_NAME)
        #     df = pd.read_parquet(result['Body'])
        #     for index, row in df.iterrows():
        #         print(row["IDNFDET"], row["VLRUNITARIO"])
        elif sys.argv[2] == 'addnotification':
            print('\r\Adding notification config for bucket...')
            add_notification_bucket(BUCKET, NOTIF_CONFIG_BUCKET)
        elif sys.argv[2] == 'deletenotification':
            print('\r\Adding notification config for bucket...')
            add_notification_bucket(BUCKET, {})
        else:
            print('Invalid command... "'+' '.join(sys.argv[1:])+'"')
    elif sys.argv[1] == 'lambda':
        if sys.argv[2] == 'create':
            print('\r\nCreating the lambda function...')
            create_lambda(LAMBDA_NAME)
        elif sys.argv[2] == 'invoke':
            print('\r\nInvoking the lambda function...')
            print(invoke_function(LAMBDA_NAME))
        elif sys.argv[2] == 'delete':
            print('\r\nDeleting the lambda function...')
            delete_lambda(LAMBDA_NAME)
        else:
            print('Invalid command... "'+' '.join(sys.argv[1:])+'"')
    elif sys.argv[1] == 'dynamodb':
        if sys.argv[2] == 'create':
            logger.info('Creating a DynamoDB table...')
            dynamodb = create_dynamodb_table(TABLENAME)
            logger.info(
            f'DynamoDB table created: {json.dumps(dynamodb, indent=4, default=json_datetime_serializer)}')
        elif sys.argv[2] == 'delete':
            logger.info('Deleteing DynamoDB table...')
            dynamodb = delete_dynamodb_table(TABLENAME)
            logger.info(
                f'Details: {json.dumps(dynamodb, indent=4, default=json_datetime_serializer)}')
        else: 
            print('Invalid command... "'+' '.join(sys.argv[1:])+'"')
    else:
        print('Invalid command... "'+' '.join(sys.argv[1:])+'"')


if __name__ == '__main__':
    main()