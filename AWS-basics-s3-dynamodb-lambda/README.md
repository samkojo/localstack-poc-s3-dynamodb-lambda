# AWS Basics S3 DynamoDB Lambda

## S3

- Criando novo bucket “poc-s3”

```bash
awslocal s3api create-bucket --bucket poc-s3
# ou
awslocal s3 mb s3://poc-s3
# ou
aws --profile localstack --endpoint $LOCALSTACK_ENDPOINT_URL s3api create-bucket --bucket poc-s3
```

- Listando todos buckets

```bash
awslocal s3api list-buckets
# ou
aws --profile localstack --endpoint $LOCALSTACK_ENDPOINT_URL s3api list-buckets
```

- Adicionando um arquivo texto “poc.txt” localizado na pasta local ao bucket “poc-s3”

```bash
awslocal s3api put-object --bucket poc-s3 --key poc.txt --body poc.txt
# ou 
awslocal s3 cp poc.txt s3://poc-s3
# ou 
aws --profile localstack --endpoint $LOCALSTACK_ENDPOINT_URL cp poc.txt s3://poc-s3
```

- Listar arquivos no bucket “poc-s3”

```bash
awslocal s3 ls s3://poc-s3
```

- Download do arquivo do bucket “poc.txt” para pasta local com nome “downloadPOC.txt”

```bash
awslocal s3 cp s3://poc-s3/poc.txt downloadPOC.txt
```

- Deletar objeto no S3

```bash
awslocal s3api delete-object --bucket poc-s3 --key poc.txt
# ou
awslocal s3 rm s3://poc-s3/poc.txt
```

Links:

[https://www.thegeekstuff.com/2019/04/aws-s3-cli-examples/](https://www.thegeekstuff.com/2019/04/aws-s3-cli-examples/)

[https://docs.aws.amazon.com/cli/latest/reference/s3/](https://docs.aws.amazon.com/cli/latest/reference/s3/)

[https://docs.aws.amazon.com/cli/latest/reference/s3api/index.html](https://docs.aws.amazon.com/cli/latest/reference/s3api/index.html)

## DynamoDB

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

Links:

[https://onexlab-io.medium.com/localstack-dynamodb-8befdaac802b](https://onexlab-io.medium.com/localstack-dynamodb-8befdaac802b)

## Lambda

- Criação de lambda
    
    Para esse exemplo temos um simples código python que retorna a mensagem `{"message": "Hello User!"}`
    
    `lambda.py`
    
    ```python
    import logging
    
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)
    
    def handler(event, context):
        logging.info('Hands-on-cloud')
        return {
            "message": "Hello User!"
        }
    ```
    
    Precisaremos ter esse arquivo zipado e para esse exemplo foi zipado com nome `lambda_hello.zip`
    
    - Com o arquivo na pasta local podemos criar nosso lambda `lambda-hello`
    
    ```bash
    awslocal lambda create-function --function-name lambda-hello --zip-file fileb://lambda_hello.zip --handler lambda.handler --runtime python3.8 --role role
    # obs: o parametro '--role' se refere as permissões e são de uso obrigatório no ambiente da AWS, porém para o uso do LocalStack é opcional por isso deixei pra explorarmos a parte
    ```
    
- Lista todos lambdas criados

```bash
awslocal lambda list-functions
```

- Executa lambda `lambda-hello` e exibe resultado no terminal

```bash
awslocal lambda invoke --function-name lambda-hello /dev/stdout
```

- Deleta lambda `lambda-hello`