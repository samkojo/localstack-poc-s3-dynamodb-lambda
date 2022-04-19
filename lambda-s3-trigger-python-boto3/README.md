# Lambda S3 Trigger Python Boto3

### Configurando variável de ambiente

Utilizando a porta padrão exposta pelo Localstack.

```bash
#Configure Environment Variables
export LOCALSTACK_ENDPOINT_URL="http://localhost:4566"
```

### Configurando AWS CLI

```bash
#Configure AWS CLI
aws configure --profile localstack

AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: us-east-1
Default output format [None]:
```

Criação de um AWS CLI profile chamado `localstack` com os padrões utilizados para uso local.

Para verificar se a configuração ficou correta podemos executar o seguinte comando abaixo para listar os buckets

```bash
#Verify LocalStack configuration
aws --profile localstack --endpoint-url=$LOCALSTACK_ENDPOINT_URL s3 ls
```

## Ambiente virtual e instalação de dependências Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install boto3
python3 -m pip install python-dotenv
```

## Lambda

Utilizamos como exemplo para executarmos na lambda o arquivo `lambda-notif-s3.py` 

### Criar lambda e bucket

```bash
python3 utils_lambda.py create
python3 utils_lambda.py createbucket
```

verificar se lista de lambdas criados

```bash
awslocal lambda list-functions
```

### Deletar lambda e bucket

```bash
python3 utils_lambda.py delete
python3 utils_lambda.py deletebucket
```

### Configurar lambda para ser executado ao adicionar um novo arquivo no Bucket S3

```bash
python3 utils_lambda.py addnotifbucket
# ou
awslocal s3api put-bucket-notification-configuration --bucket poc-s3-notif-lambda --notification-configuration file://s3-notif-config.json
```

Para verificar se foi inserido corretamente

```bash
awslocal s3api get-bucket-notification-configuration --bucket poc-s3-notif-lambda
```

Para remover a configuração

```bash
python3 utils_lambda.py delnotifbucket
# ou
awslocal s3api put-bucket-notification-configuration --bucket poc-s3-notif-lambda --notification-configuration="{}"
```

### Adicionar um arquivo ao S3

```bash
python3 utils_lambda.py addfilebucket
```

Ao adicionarmos um arquivo podemos verificar via logs Localstack a lambda ser executada e retornar o conteudo do arquivo

```bash
DEBUG:localstack.services.awslambda.lambda_executors: Lambda arn:aws:lambda:us-east-1:000000000000:function:lambda-notif-s3 result / log output:
"teste"
START RequestId: 9e7bf294-a07a-1594-acb8-10a71aafa307 Version: $LATEST
 Received event: {
   "Records": [
     {
       "eventVersion": "2.1",
       "eventSource": "aws:s3",
       "awsRegion": "us-east-1",
       "eventTime": "2022-04-19T18:56:10.097Z",
       "eventName": "ObjectCreated:Put",
       "userIdentity": {
         "principalId": "AIDAJDPLRKLG7UEXAMPLE"
       },
       "requestParameters": {
         "sourceIPAddress": "127.0.0.1"
       },
       "responseElements": {
         "x-amz-request-id": "da9cb5c9",
         "x-amz-id-2": "eftixk72aD6Ap51TnqcoF8eFidJG9Z/2"
       },
       "s3": {
         "s3SchemaVersion": "1.0",
         "configurationId": "testConfigRule",
         "bucket": {
           "name": "poc-s3-notif-lambda",
           "ownerIdentity": {
             "principalId": "A3NL1KOZZKExample"
           },
           "arn": "arn:aws:s3:::poc-s3-notif-lambda"
         },
         "object": {
           "key": "poc.txt",
           "size": 5,
           "eTag": "\"698dc19d489c4e4db73e28a713eab07b\"",
           "versionId": null,
           "sequencer": "0055AED6DCD90281E5"
         }
       }
     }
   ]
 }
 CONTENT TYPE: teste
 END RequestId: 9e7bf294-a07a-1594-acb8-10a71aafa307
 REPORT RequestId: 9e7bf294-a07a-1594-acb8-10a71aafa307	Init Duration: 1574.28 ms	Duration: 364.65 ms	Billed Duration: 365 ms	Memory Size: 1536 MB	Max Memory Used: 40 MB
```

Referencias:

[https://hands-on.cloud/testing-python-aws-applications-using-localstack/](https://hands-on.cloud/testing-python-aws-applications-using-localstack/)