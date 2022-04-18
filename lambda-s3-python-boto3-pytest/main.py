import utils
import sys
import os
from dotenv import load_dotenv

load_dotenv()
BUCKET = os.getenv('BUCKET')

if sys.argv[1] == 'create':
    print('\r\nCreating the lambda function...')
    utils.create_lambda('lambda')
elif sys.argv[1] == 'invoke':
    print('\r\nInvoking the lambda function...')
    print(utils.invoke_function('lambda'))
elif sys.argv[1] == 'delete':
    print('\r\nDeleting the lambda function...')
    utils.delete_lambda('lambda')
elif sys.argv[1] == 'createbucket':
    print('\r\Creating bucket...')
    utils.create_bucket(BUCKET)
elif sys.argv[1] == 'deletebucket':
    print('\r\nDeleting bucket...')
    utils.delete_bucket(BUCKET)
elif sys.argv[1] == 'listbucket':
    print('\r\Listing bucket...')
    utils.list_s3_bucket_objects(BUCKET)
else: 
    print('Invalid command... "'+sys.argv[1]+'"')