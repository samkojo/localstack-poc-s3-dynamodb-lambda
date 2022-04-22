import utils
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

LAMBDA_NAME = 'lambda-hello'

class Test(unittest.TestCase):
    def test_a_setup_class(self):
        print('\r\nCreating the lambda function...')
        utils.create_lambda('lambda-hello')

    def test_b_invoke_function_and_response(self):
        print('\r\nInvoking the lambda function...')
        payload = utils.invoke_function('lambda-hello')
        self.assertEqual(payload['message'], 'Hello User!')

    def test_c_teardown_class(self):
        print('\r\nDeleting the lambda function...')
        utils.delete_lambda('lambda-hello')