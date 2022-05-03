import os
import logging
import boto3
from botocore.exceptions import ClientError
import urllib.parse
import pandas as pd
from decimal import Decimal, Context
import io
from datetime import date

ctx = Context(prec=38)
today = date.today()

AWS_REGION = 'us-east-1'
LOCALSTACK_INTERNAL_ENDPOINT_URL = 'http://host.docker.internal:4566'
TABLENAME = 'sum_notas_dia'

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

def get_boto3_client(service):
    """
    Initialize Boto3 client.
    """
    try:
        boto3_client = boto3.client(
            service,
            region_name=AWS_REGION,
            endpoint_url=LOCALSTACK_INTERNAL_ENDPOINT_URL
        )
    except Exception as e:
        logger.exception('Error while connecting to LocalStack.')
        raise e
    else:
        return boto3_client

def get_boto3_resource(service):
    """
    Initialize Boto3 client.
    """
    try:
        resource = boto3.resource(
            service,
            region_name=AWS_REGION,
            endpoint_url=LOCALSTACK_INTERNAL_ENDPOINT_URL
        )
    except Exception as e:
        logger.exception('Error while connecting to LocalStack.')
        raise e
    else:
        return resource

def add_dynamodb_table_item(table_name, cnpj:str, data: str, total: Decimal):
    """
    adds a DynamoDB table.
    """
    try:
        dynamodb_resource = get_boto3_resource("dynamodb")
        table = dynamodb_resource.Table(table_name)
        response = table.put_item(
            Item={
                'CNPJ': cnpj,
                'DATA': data,
                'TOTAL': total
            }
        )

    except ClientError:
        logger.exception('Could not add the item to table.')
        raise
    else:
        return response

def handler(event, context):

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    folder = os.path.dirname(key)
    try:
        s3_client = get_boto3_client('s3')
        response = s3_client.get_object(Bucket=bucket, Key=key)
        df = pd.read_parquet(io.BytesIO(response['Body'].read()))
        add_dynamodb_table_item(TABLENAME, folder, str(today.strftime("%d/%m/%Y")), ctx.create_decimal_from_float(df["VLRUNITARIO"].sum()))
        
        return "Registro adicionado a tabela " + TABLENAME + " com sucesso!"
    except Exception as e:
        print(e)
        print('Erro ao carregar e sumarizar arquivo {} do bucket {}.'.format(key, bucket))
        raise e