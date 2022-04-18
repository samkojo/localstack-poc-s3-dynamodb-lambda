import utils
import sys

if sys.argv[1] == 'create':
    print('\r\nCreating the lambda function...')
    utils.create_lambda('lambda')
elif sys.argv[1] == 'invoke':
    print('\r\nInvoking the lambda function...')
    print(utils.invoke_function('lambda'))
elif sys.argv[1] == 'delete':
    print('\r\nDeleting the lambda function...')
    utils.delete_lambda('lambda')
else: 
    print('Invalid command... "'+sys.argv[1]+'"')