# LocalStack

## **Requirements**

- `python` (Python 3.6 up to 3.9 supported)
- `pip` (Python package manager)
- `Docker`

## Ambiente Testado

- Python 3.9.4
- pip 20.2.3 (python 3.9)
- Docker version 20.10.10, build b485636

## Instalação

[https://docs.localstack.cloud/integrations/aws-cli/](https://docs.localstack.cloud/integrations/aws-cli/)

```bash
python3 -m pip install localstack
```

## Iniciando serviços com LocalStack

[https://docs.localstack.cloud/localstack/configuration/](https://docs.localstack.cloud/localstack/configuration/)

```bash
SERVICES=s3,lambda,logs,dynamodb localstack start
```

Debug ativo

```bash
SERVICES=s3,lambda,dynamodb,logs DEBUG=1 localstack start
```

## Acessando serviços AWS

[https://docs.localstack.cloud/integrations/aws-cli/](https://docs.localstack.cloud/integrations/aws-cli/)

Utilizei a versão local que facilita utilização dos comandos via terminal

```bash
pip3 install awscli-local
```

## Testando uso dos serviços (via terminal)

### S3

[https://docs.localstack.cloud/aws/s3/](https://docs.localstack.cloud/aws/s3/)

- Criando novo bucket “sample-bucket”

```bash
awslocal s3api create-bucket --bucket sample-bucket
```

- Listando todos buckets

```bash
awslocal s3api list-buckets
```

- Adicionando um objeto ao bucket “sample-bucket”

```bash
awslocal s3api put-object --bucket sample-bucket --key index.html --body index.html
```

### DynamoDB

[https://onexlab-io.medium.com/localstack-dynamodb-8befdaac802b](https://onexlab-io.medium.com/localstack-dynamodb-8befdaac802b)

- Criação de tabela Music

```bash
awslocal dynamodb create-table \
    --table-name Music \
    --attribute-definitions \
        AttributeName=Artist,AttributeType=S \
        AttributeName=SongTitle,AttributeType=S \
    --key-schema \
        AttributeName=Artist,KeyType=HASH \
        AttributeName=SongTitle,KeyType=RANGE \
--provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5
```

- Verificar tabela

```bash
awslocal dynamodb describe-table --table-name Music
```

- Deleta tabela

```bash
awslocal dynamodb delete-table --table-name Music
```

- Insere registro na tabela

```bash
awslocal dynamodb put-item \
    --table-name Music  \
    --item \
        '{"Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Call Me Today"}, "AlbumTitle": {"S": "Somewhat Famous"}, "Awards": {"N": "1"}}'
```

- Le registros tabela

```bash
awslocal dynamodb scan --table-name Music
```

DynamoDB GUI - AWS NoSQL Workbench

[https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html)

![https://miro.medium.com/max/700/1*8byp3ux_Z6oP0Ro6Jds3EA.png](https://miro.medium.com/max/700/1*8byp3ux_Z6oP0Ro6Jds3EA.png)

![https://miro.medium.com/max/700/1*aiN5bsgXu3qt2Lk3IgZjjA.png](https://miro.medium.com/max/700/1*aiN5bsgXu3qt2Lk3IgZjjA.png)

![https://miro.medium.com/max/700/1*WhXH8bHOotWr9cItkw5aOg.png](https://miro.medium.com/max/700/1*WhXH8bHOotWr9cItkw5aOg.png)

![https://miro.medium.com/max/700/1*_Gz8OL35lME0jYiyfNc3GA.png](https://miro.medium.com/max/700/1*_Gz8OL35lME0jYiyfNc3GA.png)

![https://miro.medium.com/max/700/1*w-9LRgzFcGRVmXRqZbjmCw.png](https://miro.medium.com/max/700/1*w-9LRgzFcGRVmXRqZbjmCw.png)

Alternativa: [https://www.npmjs.com/package/dynamodb-admin](https://www.npmjs.com/package/dynamodb-admin)

### Lambda Functions

[https://github.com/serverless/serverless](https://github.com/serverless/serverless)

[https://github.com/localstack/serverless-examples](https://github.com/localstack/serverless-examples)

[S3 Upload Download](https://www.notion.so/S3-Upload-Download-abb02bbf88064b36bc623c99975ec08c)

[S3 Basics Python](https://www.notion.so/S3-Basics-Python-1cf6d48dbef64ac488e0c655cb65976b)

[DynamoDB Basics Python Boto3](https://www.notion.so/DynamoDB-Basics-Python-Boto3-afc2c2fd44924a64808553829c33db2a)

[Lambda Python Boto3 PyTest](https://www.notion.so/Lambda-Python-Boto3-PyTest-9062e6a2a80d4bd19f17eb3e262b43f9)

[Lambda S3 Python Boto3 PyTest](https://www.notion.so/Lambda-S3-Python-Boto3-PyTest-f7daef9c6d8540578a902dcf3ac7c441)

[Lambda S3 Trigger Python Boto3 PyTest](https://www.notion.so/Lambda-S3-Trigger-Python-Boto3-PyTest-0d36fcb96b1142379e92e7d2b0ee3acc)