# S3 Trigger Lambda DynamoDB Python Boto3 Pandas
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

Utilizamos como exemplo para executarmos na lambda o arquivo `lambda/lambda-s3-dynamodb.py` que sera executado ao carregarmos um arquivo ao S3, com base na pasta (organizaremos por CNPJ) que o arquivo for carregado sera alimentado a chave CNPJ e com base no nome do arquivo a tabela correspondente. Para esse exemplo sumarizaremos o campo `VLRUNITARIO`e adicionaremos junto como CNPJ e Data atual na tabela DynamoDB.

### Instala dependencias e cria pacote zip de lambda e dependencias

```bash
# Instala dependencias no projeto local
docker run --rm -v $(pwd)/lambda:/lambda -w /lambda lambci/lambda:build-python3.8 pip install -r requirements.txt -t .

# Zip Lambda + Dependencias (Layer)
cd lambda && zip -qr ../function.zip . && cd ..
```

### Criar bucket e lambda

```bash
python3 utils.py s3 create
python3 utils.py lambda create
```

Editar as configuracoes do lambda aumentando o tempo de timeout 

```bash
awslocal lambda update-function-configuration --function-name lambda-s3-dynamodb --timeout 900
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

- Cria gatilho para o bucket `client-data-sync-s3`

```bash
python3 utils.py s3 addnotification
# ou
awslocal s3api put-bucket-notification-configuration --bucket poc-s3-notif-lambda --notification-configuration file://s3-notif-config.json
```

Para verificar se foi inserido corretamente

```bash
awslocal s3api get-bucket-notification-configuration --bucket client-data-sync-s3
```

- Para remover o gatilho do bucket `client-data-sync-s3`

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

O arquivo que sera carregado será com base na variável `FILEPATH` .

```bash
python3 utils.py s3 uploadfile
```

Ao adicionarmos um arquivo podemos verificar via logs Localstack a lambda ser executada 

```bash
2022-05-03T20:29:15.223:DEBUG:localstack.services.awslambda.lambda_executors: Lambda arn:aws:lambda:us-east-1:000000000000:function:lambda-s3-dynamodb result / log output:
"Registro adicionado a tabela sum_notas_dia com sucesso!"
>START RequestId: c652c7e2-9ea8-1193-19fa-48b5e2ba1bdf Version: $LATEST
> END RequestId: c652c7e2-9ea8-1193-19fa-48b5e2ba1bdf
> REPORT RequestId: c652c7e2-9ea8-1193-19fa-48b5e2ba1bdf	Init Duration: 1546.07 ms	Duration: 712.63 ms	Billed Duration: 713 ms	Memory Size: 1536 MB	Max Memory Used: 90 MB
```

Para verificar o registro salvo no DynamoDB

```bash
awslocal dynamodb scan --table-name sum_notas_dia

# Devera retornar
{
    "Items": [
        {
            "TOTAL": {
                "N": "37769.585000000006402842700481414794922"
            },
            "DATA": {
                "S": "03/05/2022"
            },
            "CNPJ": {
                "S": "1234"
            }
        }
    ],
    "Count": 1,
    "ScannedCount": 1,
    "ConsumedCapacity": null
}
```