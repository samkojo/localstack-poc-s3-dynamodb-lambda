# DynamoDB Basics Python Boto3

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
python3 -m pip install boto3
```

### Criação de tabela

Cria tabela com nome baseado na variavel `TABLENAME` com os campos chaves na estrutura baseado na variavel `ATTRIBUTEDEFINITIONS`

```bash
python3 utils_dynamodb.py createtable
```

- Retorna dados da tabela poc-python-dynamodb (CLI)

```bash
awslocal dynamodb describe-table --table-name poc-python-dynamodb
```

### Deleção de tabela

Deleta tabela com nome baseado na variavel `TABLENAME`

```bash
python3 utils_dynamodb.py deletetable
```

### Adição de registro em tabela

Adiciona novo registro na tabela `TABLENAME` com os dados contigos em variavel `name` e `email`

```bash
python3 utils_dynamodb.py addtableitem
```

### Leitura de registro em tabela

Le registro em tabela baseado nos campos chaves contidos em variavel `name` e `email`

```bash
python3 utils_dynamodb.py readtableitem
```

Se encontrado exibira as informações do registro

```bash
...
"Item": {
        "Name": "hands-on-cloud",
        "Email": "example@cloud.com"
    },
"ResponseMetadata": {
        "RequestId": "4US2YJLEW8WCGY5MSLRTTRK25P9PJS914YT157GBG2I1M96VOXF2",
        "HTTPStatusCode": 200,
...
```

### Atualização de registro em tabela

Atualiza registro com baseado nos campos chaves contidos em variavel `name` e `email` adicionando um novo campo `phone_number` preenchido com a informação contida na variável `phone_number` 

```bash
python3 utils_dynamodb.py updatetableitem
```

Executando novamente a leitura do registro `python3 utils_dynamodb.py readtableitem` deverá retornar também o novo campo inserido

```bash
...
"Item": {
        "phone_number": "123-456-1234",
        "Email": "example@cloud.com",
        "Name": "hands-on-cloud"
    },
    "ResponseMetadata": {
        "RequestId": "6HFEN8UIJJLK82QZK4TRZXPG83X2WJTDMQTMVM2IPFSRC0RIRUF4",
        "HTTPStatusCode": 200,
...
```

### Deleção de registro em tabela

Deleta registro com baseado nos campos chaves contidos em variavel `name` e `email`

```bash
python3 utils_dynamodb.py deletetableitem
```

Referencias:

[https://hands-on.cloud/testing-python-aws-applications-using-localstack/](https://hands-on.cloud/testing-python-aws-applications-using-localstack/)