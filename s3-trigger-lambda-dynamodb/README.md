# S3 Trigger Lambda DynamoDB Python Boto3

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

## Ambiente virtual e instalação de dependências Python

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Lambda

Utilizamos como exemplo para executarmos na lambda o arquivo `[lambda-s3-dynamodb.py](http://lambda-s3-dynamodb.py)` que sera executado ao carregarmos um arquivo ao S3, o nome do arquivo e o conteudo dele (importar somente arquivo de texto) serao armazenados em uma tabela do DynamoDB com o nome `files`

### Criar lambda e bucket

```bash
python3 utils.py s3 create
python3 utils.py lambda create
```

verificar se lista de lambdas criados

```bash
awslocal lambda list-functions
```

### Deletar lambda e bucket

```bash
python3 utils.py s3 delete
python3 utils.py lambda delete
```

### Gatilho lambda em bucket S3

Configuramos um gatilho para a função lambda ao adicionarmos novo objeto no bucket S3 com base no `s3-notif-config.json`

```json
{
    "LambdaFunctionConfigurations": [
        {
            "Id": "s3eventtriggerslambda",
            "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:lambda-s3-dynamodb",
            "Events": ["s3:ObjectCreated:*"]
        }
    ]
}
```

- Cria gatilho para o bucket `poc-s3-lambda-dynamodb`

```bash
python3 utils.py s3 addnotification
# ou
awslocal s3api put-bucket-notification-configuration --bucket poc-s3-notif-lambda --notification-configuration file://s3-notif-config.json
```

Para verificar se foi inserido corretamente

```bash
awslocal s3api get-bucket-notification-configuration --bucket poc-s3-lambda-dynamodb
```

- Para remover o gatilho do bucket `poc-s3-lambda-dynamodb`

```bash
python3 utils.py s3 deletenotification
# ou
awslocal s3api put-bucket-notification-configuration --bucket poc-s3-notif-lambda --notification-configuration="{}"
```

### Criar tabela no DynamoDB

```bash
python3 utils.py dynamodb create
```

### Adicionar um arquivo ao S3

O arquivo que sera carregado será com base na variável `FILEPATH` do arquivo `.env` para fins de teste podem ir alterando e colocando outros arquivos de texto na pasta `/tmp` e executando a função de upload.

```bash
python3 utils.py s3 uploadfile
```

Ao adicionarmos um arquivo podemos verificar via logs Localstack a lambda ser executada 

```bash
localstack.services.awslambda.lambda_executors: Lambda arn:aws:lambda:us-east-1:000000000000:function:lambda-s3-dynamodb result / log output:
"Registro adicionado [poc.txt - teste] a tabela files com sucesso!"
>START RequestId: a876006d-9174-19ee-6e3f-6f01c265fbdf Version: $LATEST
> END RequestId: a876006d-9174-19ee-6e3f-6f01c265fbdf
> REPORT RequestId: a876006d-9174-19ee-6e3f-6f01c265fbdf	Init Duration: 891.92 ms	Duration: 671.54 ms	Billed Duration: 672 ms	Memory Size: 1536 MB	Max Memory Used: 42 MB
```

Para verificar o registro salvo no DynamoDB

```bash
python3 utils.py dynamodb read [nome do arquivo]
# exemplo:
python3 utils.py dynamodb read poc.txt
```

O retorno será o resultado da busca no DynamoDB com o item contendo o nome e o conteudo do arquivo