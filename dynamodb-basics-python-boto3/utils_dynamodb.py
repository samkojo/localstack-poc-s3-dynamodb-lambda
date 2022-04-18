import json
import logging
from datetime import date, datetime
import os
from dotenv import load_dotenv
import sys

import boto3
from botocore.exceptions import ClientError

load_dotenv()

AWS_REGION = os.getenv('AWS_REGION')
AWS_PROFILE = os.getenv('AWS_PROFILE')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')
TABLENAME = os.getenv('TABLENAME')

# Specifies the Resource Tags (Optional)
TAGS = [
    {
        'Key': 'Name',
        'Value': 'hands-on-cloud-dynamodb-table'
    }
]
# Specifies the attributes that make up the primary key for a table or an index
KEYSCHEMA = [
    {
        'AttributeName': 'Name',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': 'Email',
        'KeyType': 'RANGE'
    }
]
# Specifies a list of attributes that describe the key schema for the table and indexes
ATTRIBUTEDEFINITIONS = [
    {
        'AttributeName': 'Name',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'Email',
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
        client = boto3.client(
            service,
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL
        )
    except Exception as e:
        logger.exception('Error while connecting to LocalStack.')
        raise e
    else:
        return client

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

def main():
    """
    Main invocation function.
    """

    if sys.argv[1] == 'createtable':
        logger.info('Creating a DynamoDB table...')
        dynamodb = create_dynamodb_table(TABLENAME)
        logger.info(
        f'DynamoDB table created: {json.dumps(dynamodb, indent=4, default=json_datetime_serializer)}')
    elif sys.argv[1] == 'deletetable':
        logger.info('Deleteing DynamoDB table...')
        dynamodb = delete_dynamodb_table(TABLENAME)
        logger.info(
            f'Details: {json.dumps(dynamodb, indent=4, default=json_datetime_serializer)}')
    else: 
        print('Invalid command... "'+sys.argv[1]+'"')

if __name__ == '__main__':
    main()