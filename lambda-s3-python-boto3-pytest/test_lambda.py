import utils
import unittest
import os
from dotenv import load_dotenv

load_dotenv()
BUCKET = os.getenv('BUCKET')

unittest.TestLoader.sortTestMethodsUsing = None


class Test(unittest.TestCase):
    def test_a_setup_class(self):
        print('\r\nCreating the lambda function...')
        utils.create_lambda('lambda')
        utils.create_bucket(BUCKET)

    def test_b_invoke_function_and_response(self):
        print('\r\nInvoking the lambda function...')
        payload = utils.invoke_function('lambda')
        bucket_objects = utils.list_s3_bucket_objects(BUCKET)

    def test_c_teardown_class(self):
        print('\r\nDeleting the lambda function...')
        utils.delete_lambda('lambda')
        utils.delete_bucket(BUCKET)